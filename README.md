# GeoParquet Cookbook

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![GitHub](https://img.shields.io/github/stars/ZQM-Computing/geoparquet-cookbook?style=social)
![CI](https://github.com/ZQM-Computing/geoparquet-cookbook/actions/workflows/ci.yml/badge.svg)

<!-- ZQM-START -->
<!-- markdownlint-disable MD033 -->
<p align="center">
  <strong>ZQM Computing — Geospatial Engineering & Scientific Computing</strong><br>
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a> •
  <a href="https://github.com/ZQM-Labs">ZQM Labs</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-END -->

Production-tested GeoParquet patterns — partitioning, predicate pushdown, standardized metadata, and interoperability with DuckDB, Spark, Polars, and GeoPandas, with performance benchmarks.

## Repository role and status

**Status:** Active, public.

**What this repository is:** GeoParquet patterns — a practical guide and reference implementation for the open columnar geospatial format: partitioning, predicate pushdown, standardized metadata, and interoperability with DuckDB, Spark, Polars, and GeoPandas.

**What it contributes:** Part of the ZQM Computing public geospatial portfolio — production-grade pattern and reference repositories that document geospatial engineering practice across the stack. This repository is the reusable pattern library for its layer: working code and runbooks that practitioners can lift into their own pipelines, and portfolio evidence of the engineering practice behind ZQM Computing. The umbrella index for the series is [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks).

**Standing:** The portfolio program was completed and Tier-1 hardened on 2026-10-15, with prose CI enforced as required status checks. This repository is standalone — no other repository or deployment depends on it.

## Who this is for

Data engineers, data scientists, and analytics engineers who work with large-scale geospatial data in columnar formats.

A practical guide and reference implementation for working with [GeoParquet](https://geoparquet.org/) — an open, columnar format for geospatial data built on Apache Parquet.

Built for **data engineers** and **data scientists** who need fast, interoperable geospatial analytics at scale.

## Why GeoParquet?

- **Columnar storage** — Read only the columns you need; skip geometry when you only need attributes.
- **Compression** — Parquet's encoding + snappy/zstd dramatically reduces file sizes vs. GeoJSON/Shapefile.
- **Interoperability** — Works natively with DuckDB, Polars, Spark, GeoPandas, and dask-geopandas.
- **Cloud-native** — S3 / GCS / Azure Blob with partition pruning and predicate pushdown.
- **Standardized metadata** — GeoParquet 1.1 metadata embeds CRS, geometry types, and encoding.

## Repository Structure

```text
geoparquet-cookbook/
├── examples/
│   ├── 01-cog-creation/          # Create Cloud-Optimized GeoTIFFs + GeoParquet
│   ├── 02-partitioning/          # Hive partitioning strategies for spatial data
│   ├── 03-predicate-pushdown/    # Row-group and page-level filtering
│   ├── 04-duckdb-integration/    # DuckDB for local & serverless analytics
│   ├── 05-spark-integration/     # PySpark + Sedona/GeoMesa at scale
│   └── 06-performance/           # Benchmarks: Parquet vs GeoParquet vs GeoPackage
├── tests/
│   └── test_patterns.py          # Core pattern validation tests
├── pyproject.toml
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Installation

```bash
pip install -e .
# or with dev dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
from pathlib import Path

import duckdb
import geopandas as gpd
import polars as pl

output = Path("data/buildings.parquet")
output.parent.mkdir(parents=True, exist_ok=True)

# Write GeoParquet. Rename the active geometry column so the query below
# uses the explicit, stable column name "geom".
gdf = gpd.read_file("data/buildings.geojson").rename_geometry("geom")
gdf.to_parquet(output, index=False)

# Inspect the Parquet schema with Polars.
df = pl.scan_parquet(output)
print(df.collect_schema())

# Query the WKB geometry with DuckDB Spatial.
con = duckdb.connect()
try:
    con.execute("INSTALL spatial; LOAD spatial;")
    con.execute(
        """
        SELECT *
        FROM read_parquet(?)
        WHERE ST_Intersects(
            ST_GeomFromWKB(geom),
            ST_MakeEnvelope(-122.5, 37.7, -122.4, 37.8)
        )
        """,
        [output.as_posix()],
    ).show()
finally:
    con.close()
```

## Usage

After [Installation](#installation), work through the
[Quick Start](#quick-start) and the [Examples](#examples): each example
reads or writes real GeoParquet files, so you can lift the code straight
into your own pipeline and point it at your data.

## Examples

| # | Topic | Engine | Key Concepts |
|---|-------|--------|--------------|
| 01 | COG Creation | rasterio / rio-cogeo | Cloud-Optimized GeoTIFF, tiling, overview |
| 02 | Partitioning | GeoPandas / Polars | Hive partitioning, spatial index |
| 03 | Predicate Pushdown | DuckDB / Polars | Row-group filtering, bloom filters |
| 04 | DuckDB Integration | DuckDB + geoparquet extension | In-process analytics, httpfs, spatial index |
| 05 | Spark Integration | PySpark + Apache Sedona | Distributed GeoParquet, spatial joins |
| 06 | Performance | Polars / DuckDB / GeoPandas | Benchmarks, file size, query latency |

## Dependencies

- Python >= 3.10
- `duckdb` >= 1.0
- `polars` >= 1.0
- `geopandas` >= 1.0
- `pyarrow` >= 15.0
- `rasterio` (for COG example)

## Optional integrations

### COG creation and footprint indexing

The COG example generates a deterministic sample GeoTIFF, translates it to a
Cloud-Optimized GeoTIFF, validates the COG layout, and writes the raster
footprint and asset name to GeoParquet. It does not require external data.

```bash
pip install -e ".[cog]"
python examples/01-cog-creation/run.py
```

The `cog` extra supplies Rasterio and rio-cogeo. The script exits with an
installation hint when these optional packages are unavailable.

### PySpark

The Spark example is an executable Parquet/Hive-partitioning integration check.
It validates that all 1,000 fixture rows are accounted for and reports the
residential partition summary. Spark reads the geometry column as stored
Parquet data; geometry operations require a spatial engine such as Apache
Sedona and are intentionally not presented as native Spark SQL behavior.

Run the producer before the Spark consumer:

```bash
pip install -e ".[spark]"
python examples/02-partitioning/run.py
spark-submit examples/05-spark-integration/run.py
```

The example requires a working Java runtime and Spark installation. It is not
part of the default dependency set because PySpark is an optional extra.

## More from this series

- [postgis-cookbook](https://github.com/ZQM-Computing/postgis-cookbook) — Production PostGIS patterns: spatial indexing, joins & KNN, SRID management, vector tiles, data quality, partitioning
- [duckdb-spatial-cookbook](https://github.com/ZQM-Computing/duckdb-spatial-cookbook) — DuckDB Spatial patterns for analytical geospatial SQL: GeoParquet, spatial joins, KNN, H3 aggregation — no server required
- [pgrouting-cookbook](https://github.com/ZQM-Computing/pgrouting-cookbook) — pgRouting network analysis on PostGIS: shortest path, driving distance, isochrones, turn restrictions, traffic-aware routing
- [geopandas-cookbook](https://github.com/ZQM-Computing/geopandas-cookbook) — GeoPandas/Shapely patterns for Python geospatial workflows: spatial joins, CRS handling, overlays, interpolation, performance
- [gdal-cookbook](https://github.com/ZQM-Computing/gdal-cookbook) — GDAL/OGR command-line patterns: conversion, reprojection, clipping, mosaicking — production-tested, runnable examples
- [stac-cookbook](https://github.com/ZQM-Computing/stac-cookbook) — STAC patterns for geospatial data discovery: catalogs, item validation, search API, bulk operations, cloud deployment
- [maplibre-cookbook](https://github.com/ZQM-Computing/maplibre-cookbook) — MapLibre GL JS patterns for frontend vector tile rendering: custom layers, 3D terrain, performance tuning, interactive maps
- [cog-cookbook](https://github.com/ZQM-Computing/cog-cookbook) — Cloud Optimized GeoTIFF patterns: creation, validation, TiTiler serving, xarray integration, performance benchmarking
- [h3-cookbook](https://github.com/ZQM-Computing/h3-cookbook) — H3 hexagonal grid patterns: indexing, aggregation, visualization, grid comparisons, performance benchmarks
- [qgis-resources](https://github.com/ZQM-Computing/qgis-resources) — QGIS expressions, PyQGIS snippets, Processing scripts, styles, and QField field-collection guides
- [geospatial-api-reference](https://github.com/ZQM-Computing/geospatial-api-reference) — OGC API – Features reference implementation with FastAPI and PostGIS backends
- [ollama-fleet-cookbook](https://github.com/ZQM-Computing/ollama-fleet-cookbook) — Ollama fleet operations: model management, health checks, load-spreading, VRAM budgeting, dependency-light RAG
- [proxmox-ceph-operations](https://github.com/ZQM-Computing/proxmox-ceph-operations) — Proxmox VE + Ceph operations runbooks: health checks, backup discipline, OSD replacement, upgrade checklists
- [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks) — Umbrella index for all ZQM geospatial pattern repos

## Documentation and validation

For setup instructions, reproducible examples, data provenance, CRS/SRID assumptions, security guidance, and dependency labels, follow the [ZQM geospatial repository documentation standard](https://github.com/ZQM-Computing/geospatial-cookbooks/blob/main/docs/repository-documentation-standard.md).

The configured CI workflow is the source of truth for automated checks. A passing workflow establishes only that its checks passed for that commit; it does not certify production deployment or prove that every dependency and operating environment was covered.

## License

MIT — see [LICENSE](https://github.com/ZQM-Computing/geoparquet-cookbook/blob/main/LICENSE).

## Contributing

See [CONTRIBUTING.md](https://github.com/ZQM-Computing/geoparquet-cookbook/blob/main/CONTRIBUTING.md).

*Part of [ZQM Computing](https://github.com/ZQM-Computing) — geospatial engineering, scientific computing, and infrastructure patterns; the geospatial arm of [ZQM Labs](https://zqmlabs.com), makers of Z's Quests & Mischief location games.*

<!-- ZQM-FOOTER-START -->
<!-- markdownlint-disable MD033 -->
---

<p align="center">
  <em>Geospatial engineering · Scientific computing · Reproducible patterns</em><br>
  <a href="https://github.com/ZQM-Labs">ZQM Labs</a> •
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-FOOTER-END -->
