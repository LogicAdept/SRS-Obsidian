<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What causes Too many parts in ClickHouse?

> [!abstract] Short answer
> The "Too many parts" error fires when inserts create parts faster than background merges can retire them — typically row-at-a-time INSERTs or an over-partitioned table. Limits are `parts_to_delay_insert` (default 1000: inserts start being deliberately slowed), `parts_to_throw_insert` (default 3000: inserts rejected), and `max_parts_in_total` (100000 across all partitions).

## Why small parts are poison

Every part is a directory of files with its own sparse index, marks, and metadata held in memory; each merge must read, rewrite, and re-index all of them. The docs' troubleshooting list: poor query performance (more files to open and read), increased memory (per-part metadata), reduced compression (small blocks compress worse), higher I/O (more seeks), and slower merges (the scheduler drowns). Merges retire parts asymptotically — big parts merge rarely — so a writer emitting hundreds of parts per second per partition outruns any merge budget, and the engine first applies backpressure (delay), then refuses inserts.

```sql
-- watch part pressure per partition
SELECT partition, count() AS parts, avg(rows) AS avg_rows
FROM system.parts
WHERE database = 'default' AND table = 'hits' AND active
GROUP BY partition ORDER BY parts DESC;
```

**Listing 1.** The standard monitoring query: parts per partition and their average size — `avg_rows` in the hundreds is the red flag.

## The fixes

Insert batches of thousands-tens of thousands of rows; where clients cannot batch, [[What are async inserts in ClickHouse]] buffer server-side. Check the partition key — one part per partition value per insert means over-partitioning multiplies parts ([[Why do too many partitions hurt ClickHouse]]); monthly `toYYYYMM` is the default recommendation. The error is a protection mechanism, not a bug: it protects the table (and neighbors on the same node) from merge collapse, so the correct response is fixing the writer, not raising the limit.

```d2
writers: "Many small INSERTs\nor too many partitions" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}
parts: "Parts accumulate\nfaster than merges" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
delay: "> parts_to_delay_insert (1000)\ninserts slowed" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
throw: "> parts_to_throw_insert (3000)\n'Too many parts' - inserts fail" {
  width: 340
  height: 80
  style.fill: "#ffebee"
}
fix: "Batch / async inserts /\ncoarser partitioning" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
writers -> parts
parts -> delay
delay -> throw
delay -> fix
```

**Fig. 1.** Part pressure ladder: slow down at 1000 parts per partition, reject at 3000 — fix the write pattern instead of the limits.

> [!warning] Raising the limits is not a fix
> The thresholds protect the merge scheduler's finite budget; pushing them up converts an insert-time error into cluster-wide merge starvation, slow queries, and eventually unmanageable part explosions — including on replicas that must replay your parts. The operational answer is always at the writer: batching, async inserts, or a buffer/Kafka stage that absorbs bursts ([[How do you ingest Kafka into ClickHouse]]).

> [!tip] Interview answer
> Too many parts means insert rate beats merge rate: each tiny INSERT builds a directory with indexes and metadata, merges can't keep up, and the engine delays inserts at 1000 parts per partition and rejects at 3000. Fix by batching rows into tens of thousands, enabling async inserts for small writers, and avoiding over-partitioning — not by raising limits.
