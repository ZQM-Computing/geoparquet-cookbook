#!/usr/bin/env python3
"""Tests for geoparquet-cookbook."""

import subprocess
import sys
from pathlib import Path

import geopandas as gpd
import pyarrow.parquet as pq

REPO_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
EXPECTED_EXAMPLES = {
    "01-creation",
    "01-cog-creation",
    "02-partitioning",
    "03-predicate-pushdown",
    "04-duckdb-integration",
    "05-spark-integration",
    "06-performance",
}


def test_exact_example_inventory():
    """The documented example tree cannot silently drift from its seven entry points."""
    actual = {path.parent.name for path in EXAMPLES_DIR.glob("*/run.py")}
    assert actual == EXPECTED_EXAMPLES, (
        f"Example inventory mismatch. Missing: {sorted(EXPECTED_EXAMPLES - actual)}; "
        f"unexpected: {sorted(actual - EXPECTED_EXAMPLES)}"
    )


def test_basic_creation_round_trip(tmp_path):
    """The base GeoParquet example writes a readable synthetic point dataset."""
    script = EXAMPLES_DIR / "01-creation" / "run.py"
    result = subprocess.run(
        [sys.executable, str(script)], cwd=tmp_path, capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Written to output/points.parquet" in result.stdout
    output = tmp_path / "output" / "points.parquet"
    assert output.is_file()
    points = gpd.read_parquet(output)
    assert len(points) == 5
    assert points.crs.to_epsg() == 4326
    assert points["name"].tolist() == ["A", "B", "C", "D", "E"]


def test_python_syntax():
    """All Python examples have valid syntax."""
    for py_file in sorted(EXAMPLES_DIR.glob("*/run.py")):
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(py_file)], capture_output=True, text=True
        )
        assert result.returncode == 0, f"Syntax error in {py_file}: {result.stderr}"



def test_cog_example_reports_optional_dependencies_or_runs(tmp_path):
    """The COG example either runs end-to-end or explains its optional extra."""
    script = EXAMPLES_DIR / "01-cog-creation" / "run.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        assert "COG created and validated" in result.stdout
        assert (tmp_path / "output" / "synthetic-dem-cog.tif").is_file()
        assert (tmp_path / "output" / "raster-footprint.parquet").is_file()
    else:
        assert 'pip install -e ".[cog]"' in result.stdout + result.stderr


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



def test_performance_example_is_self_contained(tmp_path):
    """The benchmark creates its own output and validates both format round trips."""
    script = EXAMPLES_DIR / "06-performance" / "run.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "GeoParquet full read: " in result.stdout
    assert "GeoParquet filtered read: " in result.stdout
    assert "GeoJSON write/read: " in result.stdout

    output_dir = tmp_path / "output"
    assert (output_dir / "benchmark.parquet").is_file()
    assert (output_dir / "benchmark.geojson").is_file()

def test_readme_optional_cog_commands_are_separate_shell_lines():
    """Optional example commands must be copy/pasteable, not literal escaped newlines."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert r"python examples/01-creation/run.py\n\n# Optional" not in readme
    assert "python examples/01-creation/run.py\n\n# Optional: create a COG" in readme


def test_readme_distinguishes_ci_handoff_from_production_dependency():
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "pinned synthetic GeoParquet/DuckDB handoff in CI" in readme
    assert "no other repository or deployment depends on it" not in readme


def test_readme_exists():
    """README.md exists."""
    assert (REPO_ROOT / "README.md").exists()


def test_license_exists():
    """LICENSE file exists."""
    assert (REPO_ROOT / "LICENSE").exists()
