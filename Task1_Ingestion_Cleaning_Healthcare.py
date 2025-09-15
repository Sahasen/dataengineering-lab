# Databricks notebook source
from pyspark.sql.functions import col, to_date
df_raw = spark.table("healthcare_orders")
# 2. Clean & transform
df_cleaned = (
   df_raw
 .withColumn("order_date", to_date(col("order_date"), "yyyy-MM-dd"))
 .withColumn("total_bill", col("quantity") * col("price"))
)
# 3. Save as managed Silver table
df_cleaned.createOrReplaceTempView("tmp_healthcare_orders_cleaned")
spark.sql("""
CREATE OR REPLACE TABLE silver_healthcare_orders AS
SELECT * FROM tmp_healthcare_orders_cleaned
""")
display(spark.table("silver_healthcare_orders").limit(10))