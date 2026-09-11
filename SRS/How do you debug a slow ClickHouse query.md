<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SystemDesign/Performance #SRS

# How do you debug a slow ClickHouse query?

> [!abstract] Short answer
> The loop: find the query in `system.query_log` (`query_duration_ms`, `read_rows`, `ProfileEvents`), read its plan with `EXPLAIN indexes = 1` to see granule pruning per index, check the read pipeline (`EXPLAIN ANALYZE` / the analyzer) for the expensive stage, then fix the layout — sort key, skip indexes, projections, PREWHERE — or the data volume, not the hardware.

## Step by step

`system.query_log` records one or two rows per query (types `QueryStart`/`QueryFinish`/`ExceptionBeforeStart`/`ExceptionWhileProcessing`): `query_duration_ms`, `read_rows` (including subqueries and JOINs, summed across replicas for distributed queries), `result_rows`, memory (`memory_usage`), and `ProfileEvents` counters that localize the pain (disk I/O, decompression, network). Sort by duration over your window, take the worst offenders, and reproduce with `EXPLAIN indexes = 1`: the primary key line shows granules selected of total — near-1.0 means the sort key is not pruning ([[How do you verify a ClickHouse index is used]]) — and each skipping index reports its filtered granules ([[Why might a ClickHouse skip index not help]]). `EXPLAIN ANALYZE` adds per-stage timings over the analyzer pipeline ([[What are projections in ClickHouse]] when a projection could replace a big aggregation).

```sql
SELECT query_duration_ms, read_rows, memory_usage, substring(query, 1, 120) AS q
FROM system.query_log
WHERE event_date >= today() - 1 AND type = 'QueryFinish'
ORDER BY query_duration_ms DESC
LIMIT 10;

EXPLAIN indexes = 1
SELECT count() FROM hits WHERE user_id = 7432 AND ts >= '2026-09-01';
```

**Listing 1.** Top slow queries from `query_log`, then the index-by-index pruning breakdown of the culprit.

## The usual fixes, in order of leverage

Granule pruning first: wrong or unselective ORDER BY dominates slow scans ([[How do you choose ORDER BY in ClickHouse]]). Then read volume: PREWHERE/automatic condition ordering ([[What is PREWHERE in ClickHouse]]), skip indexes for non-key filters, projections for fixed heavy aggregations. Then shape: avoid GLOBAL JOINs on sharded tables, unnest only what you aggregate, and pre-aggregate hot dashboards into MV targets ([[How do materialized views work in ClickHouse]]). Data-layout problems — tiny parts, too many partitions — show up as generic slowness across all queries ([[What causes Too many parts in ClickHouse]]); that pattern, not one bad query, is the signal to fix ingestion.

> [!warning] EXPLAIN without ANALYZE can lie about cost
> Plan-level granule counts estimate pruning, not runtime — decompression, thread allocation, and network transfers appear only in actual execution; and `query_log`'s `read_rows` counts rows *before* filtering, so a query reading 10 billion rows can legitimately return 10. Anchor every optimization in before/after `query_duration_ms` and ProfileEvents, not in how the plan looks.

> [!tip] Interview answer
> I find the offender in system.query_log — duration, read_rows, memory, ProfileEvents — then EXPLAIN indexes = 1 to see whether the primary key and skip indexes prune granules, and EXPLAIN ANALYZE to find the slow pipeline stage. Fixes follow the diagnosis: sort key first, then read-volume tools like PREWHERE and projections, and ingestion-side fixes when everything is uniformly slow.
