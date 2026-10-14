# GeoParquet Patterns

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

```
geoparquet-patterns/
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
import geopandas as gpd
import polars as pl

# Write GeoParquet
gdf = gpd.read_file("data/buildings.geojson")
gdf.to_parquet("data/buildings.parquet", layer="buildings")

# Read with Polars (metadata-aware)
df = pl.scan_parquet("data/buildings.parquet")
print(df.collect_schema())

# Query with DuckDB
import duckdb
duckdb.sql("""
    SELECT * FROM 'data/buildings.parquet'
    WHERE ST_Intersects(geom, ST_MakeEnvelope(-122.5, 37.7, -122.4, 37.8))
""").show()
```

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

## More from this series

- [postgis-patterns](https://github.com/ZQM-Computing/postgis-patterns) — Production PostGIS patterns: spatial indexing, joins & KNN, SRID management, vector tiles, data quality, partitioning
- [duckdb-spatial-patterns](https://github.com/ZQM-Computing/duckdb-spatial-patterns) — DuckDB Spatial patterns for analytical geospatial SQL: GeoParquet, spatial joins, KNN, H3 aggregation — no server required
- [pgrouting-patterns](https://github.com/ZQM-Computing/pgrouting-patterns) — pgRouting network analysis on PostGIS: shortest path, driving distance, isochrones, turn restrictions, traffic-aware routing
- [geopandas-patterns](https://github.com/ZQM-Computing/geopandas-patterns) — GeoPandas/Shapely patterns for Python geospatial workflows: spatial joins, CRS handling, overlays, interpolation, performance
- [gdal-patterns](https://github.com/ZQM-Computing/gdal-patterns) — GDAL/OGR command-line patterns: conversion, reprojection, clipping, mosaicking — production-tested, runnable examples
- [stac-patterns](https://github.com/ZQM-Computing/stac-patterns) — STAC patterns for geospatial data discovery: catalogs, item validation, search API, bulk operations, cloud deployment
- [maplibre-patterns](https://github.com/ZQM-Computing/maplibre-patterns) — MapLibre GL JS patterns for frontend vector tile rendering: custom layers, 3D terrain, performance tuning, interactive maps
- [cog-patterns](https://github.com/ZQM-Computing/cog-patterns) — Cloud Optimized GeoTIFF patterns: creation, validation, TiTiler serving, xarray integration, performance benchmarking
- [h3-patterns](https://github.com/ZQM-Computing/h3-patterns) — H3 hexagonal grid patterns: indexing, aggregation, visualization, grid comparisons, performance benchmarks
- [qgis-resources](https://github.com/ZQM-Computing/qgis-resources) — QGIS expressions, PyQGIS snippets, Processing scripts, styles, and QField field-collection guides
- [geospatial-api-reference](https://github.com/ZQM-Computing/geospatial-api-reference) — OGC API – Features reference implementation with FastAPI and PostGIS backends
- [ollama-fleet-patterns](https://github.com/ZQM-Computing/ollama-fleet-patterns) — Ollama fleet operations: model management, health checks, load-spreading, VRAM budgeting, dependency-light RAG
- [proxmox-ceph-operations](https://github.com/ZQM-Computing/proxmox-ceph-operations) — Proxmox VE + Ceph operations runbooks: health checks, backup discipline, OSD replacement, upgrade checklists
- [geospatial-patterns](https://github.com/ZQM-Computing/geospatial-patterns) — Umbrella index for all ZQM geospatial pattern repos

## License

MIT — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Related repositories

- [ZQM Geospatial Patterns](https://github.com/ZQM-Computing/geospatial-patterns) — umbrella index of all geospatial pattern repos
- [postgis-patterns](https://github.com/ZQM-Computing/postgis-patterns) — production PostGIS patterns & best practices
- [duckdb-spatial-patterns](https://github.com/ZQM-Computing/duckdb-spatial-patterns) — DuckDB Spatial patterns for analytical geospatial SQL
- [geospatial-api-reference](https://github.com/ZQM-Computing/geospatial-api-reference) — OGC API - Features with FastAPI + PostGIS
- [qgis-resources](https://github.com/ZQM-Computing/qgis-resources) — QGIS expressions, PyQGIS, styles, and QField guides
- [proxmox-ceph-operations](https://github.com/ZQM-Computing/proxmox-ceph-operations) — Proxmox VE + Ceph operations runbooks
- [ollama-fleet-patterns](https://github.com/ZQM-Computing/ollama-fleet-patterns) — Ollama fleet operations & a minimal RAG reference

*Part of [ZQM Labs](https://github.com/ZQM-Computing) — games, gear & a little mischief.*

