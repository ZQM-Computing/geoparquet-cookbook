#!/usr/bin/env python3
"""Example 02: Partitioning strategies for GeoParquet."""

from pathlib import Path

import geopandas as gpd
import numpy as np
import pyarrow as pa
import pyarrow.dataset as ds

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Fixed seed makes the example reproducible and its assertions meaningful.
rng = np.random.default_rng(42)
n = 1000
categories = rng.choice(["residential", "commercial", "industrial"], n)
lats = rng.uniform(28.95, 29.05, n)
lngs = rng.uniform(-80.95, -80.90, n)
values = rng.integers(1, 100, n)

points = gpd.GeoDataFrame(
    {"site_id": np.arange(1, n + 1), "name": [f"Site {i:04d}" for i in range(1, n + 1)], "category": categories, "value": values},
    geometry=gpd.points_from_xy(lngs, lats),
    crs="EPSG:4326",
).rename_geometry("geom")

# Write a single-file dataset for examples that query the complete point set.
points_path = OUTPUT_DIR / "points.parquet"
points.to_parquet(points_path, index=False)

# GeoDataFrame.to_parquet writes one Parquet file; partitioned datasets must be
# written with PyArrow's dataset API. Keep the GeoParquet schema metadata intact.
table = pa.table(points.to_arrow(index=False))
partition_schema = pa.schema([("category", table.schema.field("category").type)])
ds.write_dataset(
    table,
    base_dir=OUTPUT_DIR / "partitioned.parquet",
    format="parquet",
    partitioning=ds.partitioning(partition_schema, flavor="hive"),
    existing_data_behavior="delete_matching",
)

print(f"Wrote {len(points)} points to {points_path}")
print("Written partitioned GeoParquet dataset:")
for partition in sorted((OUTPUT_DIR / "partitioned.parquet").glob("category=*")):
    print(f"  {partition.name}")

residential = gpd.read_parquet(
    OUTPUT_DIR / "partitioned.parquet" / "category=residential"
)
assert len(residential) == int((points["category"] == "residential").sum())
assert set(residential["category"]) == {"residential"}
assert residential.crs.to_epsg() == 4326
print(f"\nResidential partition: {len(residential)} rows")
