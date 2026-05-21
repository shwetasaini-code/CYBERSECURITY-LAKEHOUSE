from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, to_date, hour, when

spark = SparkSession.builder.appName('SilverSecurityLog_Cleaning').getOrCreate()

df = spark.read.parquet("data/bronze/security_logs")

silver_df = df\
    .withColumn("event_type", upper(trim(col("event_type"))))\
    .withColumn("event_date", to_date(col("event_timestamp")))\
    .withColumn("event_hour", hour(col("event_timestamp")))\
    .withColumn("risk_score",
                when(col("severity") == "HIGH", 90)
                .when(col("severity") == "MEDIUM", 50)
                .when(col("severity") == "LOW", 20)
                .otherwise(10)
                )\
    .withColumn("is_suspicious",
                when(col("event_type")
                     .isin(
                    "FAILED_LOGIN",
                    "MALWARE_ALERT",
                    "FIREWALL_bLOCK",
                    "SUSPICIOUS_IP"
                ), True).otherwise(False))

silver_df = silver_df.drop_duplicates()

silver_df = silver_df.filter(
    col("user_id").isNotNull() &
    col("event_type").isNotNull() &
    col("ip_address").isNotNull()
)
silver_df.show(10)
silver_df.write.mode("overwrite")\
    .partitionBy("year", "month", "day")\
    .parquet("data/silver/security_logs")

print("Silver cleaning completed successfully..✅")

spark.stop()
