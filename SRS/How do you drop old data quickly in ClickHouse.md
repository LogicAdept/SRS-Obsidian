<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Partitioning #SRS

# How do you drop old data quickly in ClickHouse?

> [!abstract] Short answer
> The fast path is partition-level: `ALTER TABLE ... DROP PARTITION` is a metadata operation that completes in milliseconds regardless of data volume, because it removes whole part directories without rewriting anything. Design for it — partition by the time unit you want to drop (day or month) — and let [[What is TTL in ClickHouse]] automate the same operation on a schedule.

## The mechanics

`DROP PARTITION <expr>` detaches and deletes every part of that partition immediately; `DETACH PARTITION` moves it to the `detached/` directory instead, keeping the files recoverable until removed. This is the asymmetry with row-level removal: a mutation DELETE rewrites all parts containing matched rows ([[What are mutations in ClickHouse]]), and a lightweight delete only masks rows while storage is reclaimed at the next merge — both are orders of magnitude slower for "delete everything older than N days". The FAQ's recommended lifecycle: TTL for automatic removal (which, with `ttl_only_drop_parts = 1` and partition-aligned expiry, literally executes as partition drops during merges), DROP PARTITION for manual ops.

```sql
-- monthly-partitioned table
ALTER TABLE hits DROP PARTITION '202603';      -- instant, whole partition
ALTER TABLE hits DETACH PARTITION '202603';    -- keep files in detached/ first

-- with ttl_only_drop_parts = 1, TTL drops whole parts, no rewrite
ALTER TABLE hits MODIFY SETTING ttl_only_drop_parts = 1;
```

**Listing 1.** Partition drop, the careful detach variant, and the setting that makes TTL expire as partition drops.

## Designing for fast expiry

The partition key must match the retention boundary: day partitions for day-scale retention (`toYYYYMMDD(date)`), month partitions for months (`toYYYYMM(date)`) — the TTL guide's explicit recommendation. Finer than a day and you are back in over-partitioning territory ([[Why do too many partitions hurt ClickHouse]]); coarser than your retention granularity and DROP PARTITION deletes data you still need, forcing row-level paths. The same alignment pays across engines: for the Kafka-ingested tables in [[What is the Kafka to ClickHouse materialized view pattern]], retention-by-partition keeps consumer-side replay and server-side expiry consistent.

> [!warning] DROP PARTITION has no WHERE and no undo
> It deletes the *whole* partition by definition — there is no "drop rows older than X *within* the partition" fast path; if the boundary falls inside a partition, you are down to mutations or lightweight deletes, which are the slow paths by construction. And an accidental DROP PARTITION is a real data-loss incident: DETACH PARTITION first when the delete is operational (archival, migrations), since detached files can be ATTACHed back until physically removed.

> [!tip] Interview answer
> Retention in ClickHouse is a partitioning decision: DROP PARTITION is metadata-fast and volume-independent, so I partition at the retention boundary — days or months — and either drop manually or set TTL with ttl_only_drop_parts so merges expire whole partitions. Row-level deletes are mutations or masks — fine for corrections, never for bulk expiry.
