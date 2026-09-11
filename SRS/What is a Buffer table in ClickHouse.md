<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is a Buffer table in ClickHouse?

> [!abstract] Short answer
> A Buffer table holds inserts in RAM — per layer — and periodically flushes accumulated blocks into a real target table, flushing when every `min_*` condition or any `max_*` condition is met. It smooths many small inserts into fewer, bigger writes; reads see buffer and target simultaneously, but data can be reordered and is vulnerable to node crashes.

## Mechanics

`ENGINE = Buffer(database, table, num_layers, min_time, max_time, min_rows, max_rows, min_bytes, max_bytes[, flush_time, flush_rows, flush_bytes])`. Each of the `num_layers` buffers is an independent in-RAM staging area chosen randomly per insert; flush rules are evaluated per layer — flush when all `min_*` thresholds (time in seconds, rows, bytes) are satisfied, or immediately when any `max_*` is exceeded. Inserts larger than `max_rows`/`max_bytes` bypass the buffer and go straight to the target. SELECTs transparently read both the buffer contents and the target table, so freshness is immediate — with the caveat that buffered data evaporates on server crash, since nothing was written to the target yet.

```sql
CREATE TABLE hits_buffer AS hits
ENGINE = Buffer(merge, hits, 1, 10, 100, 10000, 1000000, 10000000, 100000000);
-- num_layers=1, flush when time>=10s (and rows>=10k) or any max is hit

INSERT INTO hits_buffer VALUES (...);   -- lands in RAM first
SELECT count() FROM hits_buffer;        -- buffer + target, combined view
```

**Listing 1.** The documented example configuration: bounded to 100 MB per layer, at-least-10-seconds micro-batching.

## Where it fits

Buffer is a pre-[[What are async inserts in ClickHouse]] tool for absorbing insert storms — agents writing rows individually, chatty services — by turning them into batched part creations. It is single-node (the buffer lives on one server), so it does not add durability: the crash window is real data loss. The docs also warn it misbehaves with CollapsingMergeTree, since buffered rows may flush in a different order and different blocks than they arrived ([[What is CollapsingMergeTree]] pairs on row order semantics). Today async inserts usually replace Buffer tables, because they batch server-side without an extra table and integrate deduplication.

> [!warning] Buffered rows are unacknowledged rows
> The INSERT reports success while the data sits in RAM; a crash loses everything not yet flushed, and the flush window (seconds) is exactly when most crashes happen under load. If the requirement is "never lose an event", the answer is batching on the client side with retry, Kafka ingestion ([[How do you ingest Kafka into ClickHouse]]), or async inserts with durability — not a Buffer table, which optimizes for target-table part hygiene at the expense of durability.

> [!tip] Interview answer
> Buffer is an in-RAM staging table over a real target: N independent layers, flushed when min-thresholds all pass or any max threshold trips, with reads spanning buffer plus target. It absorbs small-insert storms into proper parts, but data sits unflushed in memory — crash losses and row reordering are real, which is why async inserts mostly superseded it.
