#!/usr/bin/env python3
"""Example 02: Partitioning strategies for GeoParquet."""
import os

import geopandas as gpd
import numpy as np

# Create synthetic data with categories
np.random.seed(42)
n = 1000
categories = np.random.choice(["residential", "commercial", "industrial"], n)
lats = np.random.uniform(28.95, 29.05, n)
lngs = np.random.uniform(-80.95, -80.90, n)
values = np.random.randint(1, 100, n)

points = gpd.GeoDataFrame(
    {"category": categories, "value": values},
    geometry=gpd.points_from_xy(lngs, lats),
    crs="EPSG:4326"
)

# Write partitioned by category
points.to_parquet("output/partitioned.parquet", partition_cols=["category"], index=False)
print("Written partitioned parquet")

# List partitions

for root, dirs, files in os.walk("output/partitioned.parquet"):
    for d in dirs:
        print(f"  Partition: {d}")

# Read single partition
residential = gpd.read_parquet("output/partitioned.parquet/category=residential")
print(f"\nResidential partition: {len(residential)} rows")
