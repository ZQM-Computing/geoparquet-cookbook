-- Pattern 10: Compaction
-- Compact small Parquet files into larger row groups
-- import pyarrow.parquet as pq
-- pq.write_table(pq.read_table("small/*.parquet"), "compacted.parquet", row_group_size=100000)

-- Optimize with DuckDB COPY
-- COPY (SELECT * FROM read_parquet('small/*.parquet')) TO 'compacted.parquet' (FORMAT PARQUET)
