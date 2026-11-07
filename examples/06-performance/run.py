#!/usr/bin/env python3
"""Example 06: reproducible GeoParquet versus GeoJSON smoke benchmark.

Timings are a single local run, not a statistically controlled performance claim.
Use representative data and repeated trials before comparing production systems.
"""

import json
import platform
from pathlib import Path
from time import perf_counter

import geopandas as gpd
import numpy as np

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# A fixed generator makes row counts and filters reproducible across runs.
rng = np.random.default_rng(42)
n = 10_000
points = gpd.GeoDataFrame(
    {
        "site_id": np.arange(1, n + 1),
        "category": rng.choice(["A", "B", "C"], n),
        "value": rng.integers(1, 100, n),
    },
    geometry=gpd.points_from_xy(
        rng.uniform(-80.95, -80.90, n),
        rng.uniform(28.95, 29.05, n),
    ),
    crs="EPSG:4326",
)

parquet_path = OUTPUT_DIR / "benchmark.parquet"
geojson_path = OUTPUT_DIR / "benchmark.geojson"

# Write GeoParquet and record the artifact size.
start = perf_counter()
points.to_parquet(parquet_path, index=False)
write_time = perf_counter() - start
write_size = parquet_path.stat().st_size / (1024 * 1024)
assert parquet_path.is_file() and write_size > 0
print(f"GeoParquet write: {write_time:.3f}s ({write_size:.2f} MiB)")

# Read the complete dataset and validate round-trip semantics.
start = perf_counter()
loaded = gpd.read_parquet(parquet_path)
read_time = perf_counter() - start
assert len(loaded) == n
assert loaded.crs.to_epsg() == 4326
assert loaded.geometry.name == points.geometry.name
assert loaded["site_id"].equals(points["site_id"])
assert loaded.geometry.equals(points.geometry)
print(f"GeoParquet full read: {read_time:.3f}s ({len(loaded)} rows)")

# Attribute filtering must return exactly the expected subset.
expected_filtered = int((points["category"] == "A").sum())
start = perf_counter()
filtered = gpd.read_parquet(parquet_path, filters=[("category", "=", "A")])
filter_time = perf_counter() - start
assert len(filtered) == expected_filtered
assert filtered["category"].eq("A").all()
assert filtered["site_id"].isin(points["site_id"]).all()
print(f"GeoParquet filtered read: {filter_time:.3f}s ({len(filtered)} rows)")

# GeoJSON is a comparison format here; validate the round trip before comparing.
start = perf_counter()
points.to_file(geojson_path, driver="GeoJSON")
json_write_time = perf_counter() - start
start = perf_counter()
loaded_json = gpd.read_file(geojson_path)
json_read_time = perf_counter() - start
json_size = geojson_path.stat().st_size / (1024 * 1024)
assert len(loaded_json) == n
assert loaded_json.crs.to_epsg() == 4326
assert np.array_equal(loaded_json["site_id"].to_numpy(dtype=np.int64), points["site_id"].to_numpy())
assert loaded_json.geometry.geom_equals(points.geometry).all()
assert json_size > 0
print(
    f"GeoJSON write/read: {json_write_time:.3f}s / {json_read_time:.3f}s "
    f"({len(loaded_json)} rows; {json_size:.2f} MiB)"
)

# Ratios are descriptive for this one run only, not universal speed claims.
if read_time > 0:
    print(f"Single-run read-time ratio (GeoJSON / GeoParquet): {json_read_time / read_time:.2f}x")
print(f"File-size ratio (GeoJSON / GeoParquet): {json_size / write_size:.2f}x")

# Preserve exact bytes, environment and validated semantics for shareable claims.
# Never substitute a benchmark from a different dataset or cite these as
# Shapefile conversion results: this example compares GeoJSON and GeoParquet.
report = {
    "schema_version": 1,
    "status": "single_local_smoke_run_not_statistically_controlled",
    "dataset": "synthetic_random_points_seed_42",
    "rows": n,
    "formats": ["GeoParquet", "GeoJSON"],
    "reference_crs": "EPSG:4326",
    "roundtrip_verified": True,
    "filtered_category_A_rows": expected_filtered,
    "sizes_bytes": {
        "geoparquet": parquet_path.stat().st_size,
        "geojson": geojson_path.stat().st_size,
    },
    "times_seconds": {
        "geoparquet_write": write_time,
        "geoparquet_full_read": read_time,
        "geoparquet_filtered_read": filter_time,
        "geojson_write": json_write_time,
        "geojson_full_read": json_read_time,
    },
    "size_ratio_geojson_over_geoparquet": (
        geojson_path.stat().st_size / parquet_path.stat().st_size
    ),
    "environment": {"python": platform.python_version(), "geopandas": gpd.__version__,
                    "numpy": np.__version__},
    "limitations": [
        "One run only; timings are not universal speed claims.",
        "Synthetic point geometries, not 1.1M production polygons.",
        "Shapefile was not tested; no Shapefile size or speed inference.",
        "File sizes include only the direct GeoJSON and GeoParquet outputs.",
    ],
}
(OUTPUT_DIR / "format-story.metrics.json").write_text(
    json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
    encoding="utf-8",
)
print("Evidence: output/format-story.metrics.json (measured in this process)")

