<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# How do you verify a ClickHouse index is used?

> [!abstract] Short answer
> Run the query with `EXPLAIN indexes = 1`: the ReadFromMergeTree step reports the primary-key analysis — parts and granules selected of total — and lists every applied data-skipping index with its filtered granule count. In recent versions (v25.9+) a clean reading also needs `SETTINGS use_skip_indexes_on_data_read = 0, use_query_condition_cache = 0`.

## Reading the plan

The primary index line shows `"Granules": 11/12` — eleven of twelve granules survive after the key analysis; a good sort key on a selective predicate leaves a small fraction. Below it, each skipping index reports how many granules it filtered at its stage, so an index that prunes zero granules across your hot queries is a candidate for removal ([[Why might a ClickHouse skip index not help]]). `EXPLAIN ESTIMATE` gives a cheap parts/rows/granules estimate without executing, and the same numbers appear post-execution in `system.query_log` profiles ([[How do you debug a slow ClickHouse query]]).

```sql
EXPLAIN indexes = 1
SELECT count()
FROM logs
WHERE user_id = 7432 AND ts >= '2026-09-01';

-- ReadFromMergeTree
--   Indexes:
--     PrimaryKey
--       Keys: user_id
--       Granules: 3/120          <- sparse primary index pruning
--     Skip
--       Name: user_ix, Description: Bloom, Granules: 3/3 -> 2/3
```

**Listing 1.** Annotated EXPLAIN shape: primary key granules selected, then each skip index's before/after granule counts.

## What "used" does and doesn't mean

An index appearing in the plan proves application, not usefulness — compare the granule counts and the actual timing (`EXPLAIN ANALYZE`) to see whether it moved the needle. Conversely, absence of a skip index from the plan means the predicate didn't match the index expression or the setting disabled it, not that the data was fine. For sort-key sanity the two granule numbers are the whole story: if `selected/total` stays near 1.0 for your key filters, the [[What is a sparse primary index in ClickHouse]] layout is wrong and [[How do you choose ORDER BY in ClickHouse]] needs revisiting — or the access pattern belongs in [[What are projections in ClickHouse]].

> [!warning] Version-dependent flags around v25.9
> From v25.9, plain `EXPLAIN indexes = 1` can overstate skip-index effects because of the skip-indexes-on-read and query-condition-cache features; the documentation pins the reproducible form to `SETTINGS use_query_condition_cache = 0, use_skip_indexes_on_data_read = 0`. If numbers look implausible between versions, check these settings before rewriting your schema.

> [!tip] Interview answer
> EXPLAIN indexes = 1 prints per-index pruning: the primary key shows granules selected out of total, and every skip index shows its before/after granule counts. I compare those numbers across hot queries — an index filtering nothing is removed, a key filtering almost nothing is redesigned — and EXPLAIN ANALYZE adds the timing to prove real impact.
