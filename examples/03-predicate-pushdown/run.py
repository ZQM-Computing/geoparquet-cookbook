#!/usr/bin/env python3
"""Example 03: Predicate pushdown with DuckDB."""
import duckdb

con = duckdb.connect()

# Query GeoParquet directly with DuckDB
# Predicate pushdown: only reads matching rows
result = con.execute("""
    SELECT category, COUNT(*) as cnt, AVG(value) as avg_value
    FROM 'output/partitioned.parquet'
    WHERE category = 'residential'
    GROUP BY category
""").fetchdf()
print("Predicate pushdown (single partition):")
print(result)

# Spatial filter with bounding box
result2 = con.execute("""
    SELECT COUNT(*) as cnt
    FROM 'output/points.parquet'
    WHERE ST_Within(
        geom,
        ST_MakeEnvelope(-80.95, 28.95, -80.90, 29.05, 4326)
    )
""").fetchdf()
print("\nSpatial filter (bounding box):")
print(result2)

con.close()
