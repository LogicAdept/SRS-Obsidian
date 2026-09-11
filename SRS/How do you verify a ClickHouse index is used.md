<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# How do you verify a ClickHouse index is used

> [!abstract] Short answer
> Run the query with EXPLAIN indexes = 1: the ReadFromMergeTree node gains an Indexes array showing every applied index — Partition, Partition Min-Max, PrimaryKey, Skip — each with Parts and Granules before and after. If granules selected equal granules total, the index did nothing; trace logs show the same per-index drop counts.

## EXPLAIN indexes = 1

The EXPLAIN statement's indexes = 1 mode attaches per-index JSON: Type (Partition Min-Max, Partition, Statistics, PrimaryKey, or Skip), Keys, Condition, and the decisive Parts and Granules counters in selected/total form, plus the search algorithm for the primary key (for example generic exclusion search). Reading it is a comparison: PrimaryKey selecting 6 of 10 granules means the ORDER BY prefix pruned 40%; a Skip index selecting 2 of 6 means the bloom or minmax structure dropped the rest. If every stage shows no reduction, the WHERE does not match the key shape — the diagnosis continues in [[Why might a ClickHouse skip index not help]].

```sql
EXPLAIN indexes = 1
SELECT count() FROM events
WHERE user_id = 42 AND event_date >= '2026-01-01';
-- "Indexes": [
--   {"Type": "Partition", "Parts": "3/10", "Granules": "40/120"},
--   {"Type": "PrimaryKey", "Keys": ["user_id", "event_date"],
--    "Granules": "2/40", "Search Algorithm": "generic exclusion search"},
--   {"Type": "Skip", "Name": "idx_url", "Granules": "1/2"}
-- ]
```

**Listing 1.** Each index reports how many parts and granules it eliminated; the plan is the source of truth, not the DDL.

## The trace log and the sanity checks

Setting send_logs_level = 'trace' in clickhouse-client emits per-index lines like `Index vix has dropped 6102/6104 granules` during execution — the same information without the plan JSON, useful for quick checks. Two cheap sanity checks accompany it: query system.parts to confirm how many parts and granules exist (a freshly added skip index may simply not be materialized on old parts yet, per [[How do you materialize a skip index on existing ClickHouse data]]), and compare rows processed before and after (the skip-index guide's example drops a query from 100 million rows to about 33 thousand). The distinction between index types and their counters maps to [[What is a sparse primary index in ClickHouse]] for the primary key and to [[What data skipping indexes exist in ClickHouse]] for the skip family.

> [!warning] "The index exists in SHOW CREATE TABLE, so it works" is false in two ways
> First, skip indexes added via ALTER affect only newly written parts until MATERIALIZE INDEX runs, so old data never gets filtered. Second, a skip index can be applied and still be useless — one matching value in a granule forces reading the whole granule, so selected/total near 1.0 is the real failure signature. Also, PARTITION BY pruning shows up as its own stage; do not credit the primary key for partition elimination.

> [!tip] Interview answer
> I use EXPLAIN indexes = 1 and read the Indexes array on ReadFromMergeTree: each Partition, PrimaryKey, or Skip entry reports Parts and Granules selected versus total, so I can see exactly what each index eliminated. The trace log shows the same as per-index drop counts. If granules selected equal total, the index is either not materialized or the predicate does not match the key, and I fix the key or the query.
