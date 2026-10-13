# GeoParquet Patterns

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

## License

MIT — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
