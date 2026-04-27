import os
import sys

from pyspark.sql.functions import from_json, col, avg, current_timestamp, \
    session_window, to_json, struct
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spark_utils.config import SCHEMA, spark_kafka_config
from spark_utils.spark_client import get_spark_client

alerts_schema = StructType([
    StructField("id", IntegerType()),
    StructField("humidity_min", IntegerType()),
    StructField("humidity_max", IntegerType()),
    StructField("temperature_min", IntegerType()),
    StructField("temperature_max", IntegerType()),
    StructField("code", StringType()),
    StructField("message", StringType()),
])


def start_alerts_stream():
    spark = get_spark_client()

    raw_stream = (
        spark.readStream
        .format("kafka")
        .options(**spark_kafka_config)
        .load()
    )

    # Static read — enables stream-static join without stream-stream join limitations
    alerts_conditions = (
        spark.read
        .option("sep", ",")
        .option("header", True)
        .schema(alerts_schema)
        .csv("/app/spark_utils/alerts_conditions.csv")
    )

    sensor_df = (
        raw_stream
        .select(from_json(col("value").cast("string"), SCHEMA).alias("data"))
        .select("data.*")
        .withColumn("timestamp", current_timestamp())
    )

    stats = (
        sensor_df
        .withWatermark("timestamp", "10 seconds")
        .groupBy(
            session_window(col("timestamp"), "30 seconds"),
            col("sensor_id"),
        )
        .agg(
            avg("temperature").alias("t_avg"),
            avg("humidity").alias("h_avg"),
        )
        .withColumn("timestamp", current_timestamp())
    )

    join_condition = (
        (col("t_avg") >= col("temperature_min")) &
        (col("t_avg") <= col("temperature_max")) &
        (col("temperature_min") != -999)
    ) | (
        (col("h_avg") >= col("humidity_min")) &
        (col("h_avg") <= col("humidity_max")) &
        (col("humidity_min") != -999)
    )

    alerts = stats.join(alerts_conditions, join_condition, "inner")

    alerts_kafka = alerts.select(
        to_json(struct(
            col("session_window").alias("window"),
            col("t_avg"),
            col("h_avg"),
            col("code"),
            col("message"),
            col("timestamp"),
        )).alias("value")
    )

    query = (
        alerts_kafka
        .writeStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("topic", "alerts")
        .option("checkpointLocation", "/checkpoints/alerts")
        .outputMode("append")
        .start()
    )

    spark.streams.awaitAnyTermination()


if __name__ == "__main__":
    start_alerts_stream()
