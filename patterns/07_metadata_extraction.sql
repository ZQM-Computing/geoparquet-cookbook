-- Pattern 07: Metadata Extraction
-- Read GeoParquet file-level metadata (CRS, geometry types, bbox)
-- import pyarrow.parquet as pq
-- md = pq.read_metadata("data.parquet")
-- print(md.metadata)

-- Extract GeoParquet 1.1 geo metadata from Parquet key-value metadata
-- import json
-- geo = json.loads(md.metadata[b"geo"].decode())
-- print(geo["columns"]["geometry"]["crs"])
