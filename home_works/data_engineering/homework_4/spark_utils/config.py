from pyspark.sql.types import StructType, StructField, StringType, FloatType

SCHEMA = StructType([
    StructField("sensor_id", StringType()),
    StructField("temperature", FloatType()),
    StructField("humidity", FloatType()),
])

spark_kafka_config = {
    "kafka.bootstrap.servers": "kafka:9092",
    "subscribe": "building_sensors",
    "startingOffsets": "earliest",
}