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


def test_partitioning_and_predicate_pushdown_examples(tmp_path):
    """The documented producer/consumer sequence creates valid, queryable GeoParquet."""
    partitioning_script = EXAMPLES_DIR / "02-partitioning" / "run.py"
    pushdown_script = EXAMPLES_DIR / "03-predicate-pushdown" / "run.py"

    produced = subprocess.run(
        [sys.executable, str(partitioning_script)],
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
    assert points["category"].notna().all()
    assert points["value"].between(1, 99).all()

    # Validate GeoParquet metadata rather than merely trusting a successful read.
    schema = pq.read_schema(points_path)
    assert b"geo" in schema.metadata
    assert len(points.geometry) == 1000

    partitioned_path = tmp_path / "output" / "partitioned.parquet"
    partitions = sorted(partitioned_path.glob("category=*"))
    assert {p.name for p in partitions} == {
        "category=residential",
        "category=commercial",
        "category=industrial",
    }
    partition_rows = sum(
        len(gpd.read_parquet(partition)) for partition in partitions
    )
    assert partition_rows == len(points)

    consumed = subprocess.run(
        [sys.executable, str(pushdown_script)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert consumed.returncode == 0, consumed.stdout + consumed.stderr
    assert "Predicate pushdown" in consumed.stdout
    assert "Spatial filter" in consumed.stdout


def test_readme_exists():
    """README.md exists."""
    assert (REPO_ROOT / "README.md").exists()


def test_license_exists():
    """LICENSE file exists."""
    assert (REPO_ROOT / "LICENSE").exists()
