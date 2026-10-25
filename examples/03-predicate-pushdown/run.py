#!/usr/bin/env python3
"""Example 03: Predicate pushdown with DuckDB."""

from pathlib import Path

import duckdb

partitioned_path = (Path("output/partitioned.parquet")).as_posix()
points_path = (Path("output/points.parquet")).as_posix()
if not Path(partitioned_path).exists() or not Path(points_path).is_file():
    raise SystemExit("Run examples/02-partitioning/run.py first to generate the fixtures.")

con = duckdb.connect()
try:
    con.execute("INSTALL spatial; LOAD spatial;")

    # Hive partition pruning: only residential records contribute to the result.
    result = con.execute(
        """
        SELECT category, COUNT(*) AS cnt, AVG(value) AS avg_value
        FROM read_parquet(?, hive_partitioning = true)
        WHERE category = 'residential'
        GROUP BY category
        """,
        [f"{partitioned_path}/**/*.parquet"],
    ).fetchdf()
    assert len(result) == 1 and result.loc[0, "category"] == "residential"
    assert int(result.loc[0, "cnt"]) > 0
    print("Predicate pushdown (single partition):")
    print(result)

    # Geometry is stored as WKB in GeoParquet and decoded by the Spatial extension.
    result2 = con.execute(
        """
        SELECT COUNT(*) AS cnt
        FROM read_parquet(?)
        WHERE ST_Within(
            geom,
            ST_MakeEnvelope(-80.95, 28.95, -80.90, 29.05)
        )
        """,
        [points_path],
    ).fetchdf()
    assert int(result2.loc[0, "cnt"]) == 1000
    print("\nSpatial filter (bounding box):")
    print(result2)
finally:
    con.close()
