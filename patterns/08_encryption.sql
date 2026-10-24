-- Pattern 08: Encryption
-- Write encrypted GeoParquet using Parquet modular encryption
-- import pyarrow.parquet as pq
-- pq.write_table(table, "enc.parquet", encryption_config=...)

-- Read with decryption key
-- pq.read_table("enc.parquet", decryption_config=...)
