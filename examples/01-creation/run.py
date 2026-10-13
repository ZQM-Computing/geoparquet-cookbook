#!/usr/bin/env python3
"""Example 01: Create GeoParquet files."""
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

# Create synthetic data
points = gpd.GeoDataFrame(
    {"name": ["A", "B", "C", "D", "E"], "value": [10, 20, 30, 40, 50]},
    geometry=[Point(-80.93, 29.02), Point(-80.92, 29.03), Point(-80.91, 29.01),
              Point(-80.90, 29.00), Point(-80.89, 28.99)],
    crs="EPSG:4326"
)

# Write to GeoParquet
points.to_parquet("output/points.parquet", index=False)
print("Written to output/points.parquet")

# Read back
loaded = gpd.read_parquet("output/points.parquet")
print("Read back:")
print(loaded)
print()

# Check metadata
import pyarrow.parquet as pq
table = pq.read_table("output/points.parquet")
print(f"Schema: {table.schema}")
print(f"Rows: {table.num_rows}")
