from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder.appName("SimpleSparkApp").getOrCreate()
    data = [("Alice", 1), ("Bob", 2), ("Cathy", 3)]
    df = spark.createDataFrame(data, ["Name", "Id"])
    df.show()
    spark.stop()
