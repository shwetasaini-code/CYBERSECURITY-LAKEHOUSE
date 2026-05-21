from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, max, avg

spark = SparkSession.builder.appName(
    'GoldSecurityLog_Analyticds').getOrCreate()

df = spark.read.parquet("data/silver/security_logs")


# -------------------------
# Threat event summary
# -------------------------

event_summary = df.groupBy("event_type")\
    .count().alias("event_count")

print("\n=== Threat Event Summary ===")
event_summary.show()

# -------------------------
# Severity summary
# -------------------------

severity_summary = df.groupBy("severity")\
    .agg(count('*').alias("event_count"))

print("\n=== Severity Event Summary ===")
severity_summary.show()


# -------------------------
# Aggregated Gold Table
# -------------------------
daily_security_summary = df.groupBy(
    "event_date",
    "country",
    "event_type",
    "severity").agg(
        count("*").alias("total_events"),
        sum(col("is_suspicious").cast("int").alias("suspicious_events")),
        avg("risk_score").alias("avg_risk_score"),
        max("risk_score").alias("max_risk_score")
)

daily_security_summary.show()

# -------------------------
# Write Gold Tables
# -------------------------

event_summary.write.mode("overwrite")\
    .parquet("data/gold/event_summary")

severity_summary.write.mode("overwrite")\
    .parquet("data/gold/severity_summary")

daily_security_summary.write.mode("overwrite").\
    partitionBy("event_date")\
    .parquet("data/gold/daily_security_summary")

print("Gold analytics layer completed successfully..✅")

spark.stop()
