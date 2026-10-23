-- Pattern 02: Partitioning
-- Partition by column
-- gdf.to_parquet("output/", partition_cols=["region"])

-- Read partitioned
-- pd.read_parquet("output/", filters=[("region", "==", "north")])
