#!/usr/bin/env python3
"""Example 04: DuckDB integration with GeoParquet."""
import duckdb

con = duckdb.connect()

# Load spatial extension
con.execute("INSTALL spatial; LOAD spatial;")

# Query GeoParquet with spatial functions
result = con.execute("""
    SELECT
        name,
        ST_AsText(geom) as geometry_wkt,
        value
    FROM 'output/points.parquet'
    WHERE value > 25
    ORDER BY value DESC
    LIMIT 5
""").fetchdf()
print("Top 5 points by value:")
print(result)

# Aggregate by grid cell
result2 = con.execute("""
    SELECT
        ST_H3(geom, 8) as h3_cell,
        COUNT(*) as cnt,
        AVG(value) as avg_value
    FROM 'output/points.parquet'
    GROUP BY h3_cell
    ORDER BY cnt DESC
    LIMIT 5
""").fetchdf()
print("\nTop 5 H3 cells by count:")
print(result2)

con.close()
