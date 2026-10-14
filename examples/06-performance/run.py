#!/usr/bin/env python3
"""Example 06: GeoParquet performance benchmarks."""

import os
import time

import geopandas as gpd
import numpy as np

# Create synthetic data
np.random.seed(42)
n = 10000
points = gpd.GeoDataFrame(
    {"category": np.random.choice(["A", "B", "C"], n), "value": np.random.randint(1, 100, n)},
    geometry=gpd.points_from_xy(
        np.random.uniform(-80.95, -80.90, n), np.random.uniform(28.95, 29.05, n)
    ),
    crs="EPSG:4326",
)

# Write GeoParquet
start = time.time()
points.to_parquet("output/benchmark.parquet", index=False)
write_time = time.time() - start
write_size = os.path.getsize("output/benchmark.parquet") / 1024 / 1024
print(f"Write: {write_time:.3f}s ({write_size:.2f} MB)")

# Read full GeoParquet
start = time.time()
loaded = gpd.read_parquet("output/benchmark.parquet")
read_time = time.time() - start
print(f"Read full: {read_time:.3f}s ({len(loaded)} rows)")

# Read with filter
start = time.time()
filtered = gpd.read_parquet("output/benchmark.parquet", filters=[("category", "=", "A")])
filter_time = time.time() - start
print(f"Read filtered: {filter_time:.3f}s ({len(filtered)} rows)")

# Compare with GeoJSON
points.to_file("output/benchmark.geojson", driver="GeoJSON")
start = time.time()
loaded_json = gpd.read_file("output/benchmark.geojson")
json_time = time.time() - start
json_size = os.path.getsize("output/benchmark.geojson") / 1024 / 1024
print(f"\nGeoJSON: {json_time:.3f}s ({json_size:.2f} MB)")
print(f"\nGeoParquet is {json_time / read_time:.1f}x faster to read")
print(f"GeoParquet is {json_size / write_size:.1f}x smaller")
