# Evidence-first geospatial format performance stories

**Scope:** ZQM Computing geospatial engineering. This is reproducible
benchmark methodology, not an assertion that GeoParquet or GeoPolars is
universally faster than any other format or engine.

## Run and preserve evidence

After installing the cookbook's dependencies:

```bash
python examples/06-performance/run.py
python -m pytest -q tests/test_patterns.py
```

The 10,000-feature example writes **synthetic points** to GeoJSON and
GeoParquet, validates both round trips and a filtered GeoParquet query, then
writes `output/format-story.metrics.json`. That JSON contains actual bytes,
single-run timing measurements, row count, category filter count, CRS,
software versions and limitations.

Publish a numerical "size changed by X" statement only with the matching
artifact and source commit. Do not copy a third party's benchmark ratio as a
ZQM result, and never imply the example tested 1.1 million polygons or
Shapefile. It did neither.

## Conversion benchmark comparability rules

For a **new, reviewed** Shapefile-to-GeoParquet study, separately establish:

1. Authoritative source/license, fixture hash, feature count, geometry types,
   columns, null handling, encoding, CRS and extent. Use synthetic data or
   material that permits redistribution.
2. Count a Shapefile as **all component files** (at least SHP, SHX, DBF and PRJ
   where provided, plus relevant metadata), not just the SHP geometry file.
3. Check field-name truncation, character encodings, date/null conversion,
   geometry validity, attribute fidelity and CRS after the round trip. Do
   not compare schemas silently changed by the source format's limits.
4. Fix compression, row-group size, geometry encoding and versions, then
   record cold/warm cache, feature counts, wall-clock read/write, memory and
   repetition count. The current smoke test does not control caches.
5. Report median and dispersion across repeated runs and confidence or
   uncertainty where justified. Do not derive a universal speedup from one
   environment or a small synthetic point fixture.
6. Keep unfiltered full reads separate from selective predicate-pushdown
   queries. Check result equivalence and record explain/scan evidence.

A shareable result card should name the datasets, date, measured bytes,
selected query, verified geometry/attribute semantics, runtime versions,
and a GitHub source link. A small preview image is optional; the JSON is
the primary test evidence.

## GeoPolars: discovery, not deployment

The [official GeoPolars repository](https://github.com/pola-rs/geopolars)
states that Arrow extension-type support unblocked renewed development,
but describes the project as **prototype/alpha**, not production-ready.
Benchmark only on matched fixtures against GeoPandas, DuckDB or Polars
after the exact library version, geometry API, CRS semantics and supported
operations have been verified. GeoPolars is *not* an installed dependency of
this cookbook, and no "faster GeoPandas" claim follows from its architecture.

## Commercial use

ZQM Computing can use measurement-led case studies to demonstrate a scoped
GIS data optimization or workflow diagnostic service. Include the actual
dataset constraints, methodology and limitations. A synthetic demo is not a
verified buyer result or a completed engineering certification.
