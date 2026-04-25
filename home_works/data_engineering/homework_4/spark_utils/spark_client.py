from pyspark.sql import SparkSession


def get_spark_client():
    spark = SparkSession.builder.appName("SensorStream").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark