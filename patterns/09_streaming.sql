-- Pattern 09: Streaming
-- Stream large GeoParquet via row groups
-- import pyarrow.parquet as pq
-- pf = pq.ParquetFile("data.parquet")
-- for batch in pf.iter_batches(batch_size=10000):
--     process(batch)

-- Stream with DuckDB
-- con.execute("SELECT * FROM read_parquet('data.parquet')").fetch_arrow_table()
