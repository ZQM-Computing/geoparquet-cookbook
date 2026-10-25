#!/usr/bin/env python3
"""Example 05: query a partitioned GeoParquet dataset with PySpark.

Prerequisites:
    pip install -e ".[spark]"
    python examples/02-partitioning/run.py
    spark-submit examples/05-spark-integration/run.py

Spark reads the Parquet columns and Hive partition values here. It does not
interpret the GeoParquet geometry column as a native spatial type; use Apache
Sedona or another compatible spatial extension for geometry operations.
"""

from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, count

DATASET_PATH = Path("output/partitioned.parquet")


def main() -> None:
    if not DATASET_PATH.is_dir():
        raise SystemExit(
            "Missing output/partitioned.parquet. Run "
            "examples/02-partitioning/run.py first."
        )

    spark = (
        SparkSession.builder.appName("GeoParquetCookbook")
        .config("spark.sql.parquet.enableVectorizedReader", "true")
        .getOrCreate()
    )
    try:
        dataset = spark.read.parquet(str(DATASET_PATH))
        required_columns = {"category", "value", "site_id", "name", "geom"}
        missing = required_columns.difference(dataset.columns)
        if missing:
            raise ValueError(f"Partitioned GeoParquet dataset missing columns: {sorted(missing)}")

        # The category value is recovered from the Hive partition path.
        summary = (
            dataset.filter(col("category") == "residential")
            .groupBy("category")
            .agg(
                count("*").alias("row_count"),
                avg("value").alias("average_value"),
            )
            .collect()
        )
        if len(summary) != 1:
            raise AssertionError("Expected one non-empty residential partition result")

        row = summary[0]
        if row["row_count"] <= 0:
            raise AssertionError("Residential partition must contain rows")
        if not 1 <= row["average_value"] <= 99:
            raise AssertionError("Average value fell outside the generated fixture range")

        # Cross-check partitioned read totals against the source dataset.
        source_count = dataset.count()
        grouped_count = sum(
            item["row_count"]
            for item in dataset.groupBy("category").agg(count("*").alias("row_count")).collect()
        )
        if grouped_count != source_count or source_count != 1000:
            raise AssertionError(
                f"Partition row conservation failed: grouped={grouped_count}, "
                f"source={source_count}"
            )

        print("Residential partition summary:")
        print(f"  rows: {row['row_count']}")
        print(f"  average value: {row['average_value']:.3f}")
        print(f"Partition row conservation: {grouped_count}/{source_count}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
