#!/usr/bin/env python3
"""Example 04: DuckDB integration with GeoParquet and H3."""

from pathlib import Path

import duckdb

points_path = Path("output/points.parquet")
if not points_path.is_file():
    raise SystemExit("Run examples/02-partitioning/run.py first to generate the point fixture.")

con = duckdb.connect()
try:
    con.execute("INSTALL spatial; LOAD spatial;")
    con.execute("INSTALL h3 FROM community; LOAD h3;")

    # GeoParquet stores geometry as WKB; decode it before using Spatial functions.
    result = con.execute(
        """
        SELECT
            name,
            ST_AsText(ST_GeomFromWKB(geom)) AS geometry_wkt,
            value
        FROM read_parquet(?)
        WHERE value > 25
        ORDER BY value DESC, site_id
        LIMIT 5
        """,
        [points_path.as_posix()],
    ).fetchdf()
    assert len(result) == 5
    assert result["name"].notna().all()
    assert result["geometry_wkt"].str.startswith("POINT").all()
    print("Top 5 points by value:")
    print(result)

    result2 = con.execute(
        """
        SELECT
            h3_latlng_to_cell(
                ST_Y(ST_GeomFromWKB(geom)),
                ST_X(ST_GeomFromWKB(geom)),
                8
            ) AS h3_cell,
            COUNT(*) AS cnt,
            AVG(value) AS avg_value
        FROM read_parquet(?)
        GROUP BY h3_cell
        ORDER BY cnt DESC, h3_cell
        LIMIT 5
        """,
        [points_path.as_posix()],
    ).fetchdf()
    assert not result2.empty
    assert result2["h3_cell"].notna().all()
    assert result2["h3_cell"].is_unique
    assert int(result2["cnt"].sum()) == 1000
    assert (result2["cnt"] > 0).all()
    print("\nTop 5 H3 cells by count:")
    print(result2.head(5))
finally:
    con.close()
