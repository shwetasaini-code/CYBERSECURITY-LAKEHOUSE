from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, current_timestamp, year, month, day

spark = SparkSession.builder.appName('BronzeSecurityLog_Ingestion').getOrCreate()

df = spark.read.csv("data/raw/security_logs.csv",
                    header=True, inferSchema=True)

# df.show()
bronze_df = df\
    .withColumn("event_timestamp", to_timestamp(col("event_time"))) \
    .withColumn("ingestion_timestamp", current_timestamp())\
    .withColumn("year", year(col("event_time")))\
    .withColumn("month", month(col("event_time")))\
    .withColumn("day", day(col("event_time")))

bronze_df.write.mode("overwrite")\
    .partitionBy("year", "month", "day")\
    .parquet("data/bronze/security_logs")

# bronze_df = spark.read.parquet("data/bronze/security_logs")

# bronze_df.show()
print("Bronze Ingestion completed successfully.. ✅")

spark.stop()
