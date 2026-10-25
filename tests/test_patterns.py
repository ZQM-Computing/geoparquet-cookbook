#!/usr/bin/env python3
"""Tests for geoparquet-cookbook."""

import subprocess
import sys
from pathlib import Path

import geopandas as gpd
import pyarrow.parquet as pq

REPO_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"


def test_python_syntax():
    """All Python examples have valid syntax."""
    for py_file in sorted(EXAMPLES_DIR.glob("*/run.py")):
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(py_file)], capture_output=True, text=True
        )
        assert result.returncode == 0, f"Syntax error in {py_file}: {result.stderr}"


def test_partitioning_and_duckdb_examples(tmp_path):
    """Producer and DuckDB consumers preserve GeoParquet data semantics."""
    scripts = [
        EXAMPLES_DIR / "02-partitioning" / "run.py",
        EXAMPLES_DIR / "03-predicate-pushdown" / "run.py",
        EXAMPLES_DIR / "04-duckdb-integration" / "run.py",
    ]

    produced = subprocess.run(
        [sys.executable, str(scripts[0])],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert produced.returncode == 0, produced.stdout + produced.stderr

    points_path = tmp_path / "output" / "points.parquet"
    assert points_path.is_file()
    points = gpd.read_parquet(points_path)
    assert len(points) == 1000
    assert points.crs.to_epsg() == 4326
    assert points.geometry.name == "geom"
    assert points["site_id"].is_unique
    assert points["name"].is_unique
    assert points["category"].notna().all()
    assert points["value"].between(1, 99).all()

    schema = pq.read_schema(points_path)
    assert b"geo" in schema.metadata

    partitioned_path = tmp_path / "output" / "partitioned.parquet"
    partitions = sorted(partitioned_path.glob("category=*"))
    assert {p.name for p in partitions} == {
        "category=residential",
        "category=commercial",
        "category=industrial",
    }
    assert sum(len(gpd.read_parquet(partition)) for partition in partitions) == len(points)

    for script, expected_output in [
        (scripts[1], "Spatial filter"),
        (scripts[2], "Top 5 H3 cells by count"),
    ]:
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        assert expected_output in result.stdout


def test_readme_exists():
    """README.md exists."""
    assert (REPO_ROOT / "README.md").exists()


def test_license_exists():
    """LICENSE file exists."""
    assert (REPO_ROOT / "LICENSE").exists()
