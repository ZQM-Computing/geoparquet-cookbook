#!/usr/bin/env python3
"""Example 05: Spark integration with GeoParquet."""
# This example shows the PySpark code pattern.
# Run with: spark-submit examples/05-spark-integration/run.py

"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count

spark = SparkSession.builder \
    .appName("GeoParquetExample") \
    .config("spark.sql.parquet.enableVectorizedReader", "true") \
    .getOrCreate()

# Read GeoParquet
df = spark.read.parquet("output/partitioned.parquet")

# Query with predicate pushdown
result = df.filter(col("category") == "residential") \
    .groupBy("category") \
    .agg(count("*").alias("cnt"), avg("value").alias("avg_value"))

result.show()

# Spatial query (requires Sedona or GeoSpark)
# from sedona.spark import SedonaContext
# sedona = SedonaContext.builder().getOrCreate()
# spatial_df = sedona.read.format("geoparquet").load("output/points.parquet")
# spatial_df.filter(ST_Within(col("geom"), ST_MakeEnvelope(...))).show()

spark.stop()
"""

print("PySpark code pattern (run with spark-submit)")
print("See the docstring in this file for the full Spark code")
