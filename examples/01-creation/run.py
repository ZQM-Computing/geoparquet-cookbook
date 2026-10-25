#!/usr/bin/env python3
"""Example 01: Create GeoParquet files."""

from pathlib import Path

import geopandas as gpd
import pyarrow.parquet as pq
from shapely.geometry import Point

# Create synthetic data
points = gpd.GeoDataFrame(
    {"name": ["A", "B", "C", "D", "E"], "value": [10, 20, 30, 40, 50]},
    geometry=[
        Point(-80.93, 29.02),
        Point(-80.92, 29.03),
        Point(-80.91, 29.01),
        Point(-80.90, 29.00),
        Point(-80.89, 28.99),
    ],
    crs="EPSG:4326",
)

# Write to GeoParquet (create the output directory first: pyarrow does not
# create missing parent directories, so a fresh checkout fails without this).
Path("output").mkdir(parents=True, exist_ok=True)
points.to_parquet("output/points.parquet", index=False)
print("Written to output/points.parquet")

# Read back
loaded = gpd.read_parquet("output/points.parquet")
print("Read back:")
print(loaded)
print()

# Check metadata

table = pq.read_table("output/points.parquet")
print(f"Schema: {table.schema}")
print(f"Rows: {table.num_rows}")
