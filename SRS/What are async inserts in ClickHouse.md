<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What are async inserts in ClickHouse?

> [!abstract] Short answer
> Asynchronous inserts (`async_insert = 1`) move batching server-side: small INSERTs are buffered on the server and flushed into one data part when a size, time, or query-count threshold is hit — so many clients can write tiny batches without creating a part per INSERT. With `wait_for_async_insert = 1` (the documented recommendation) the INSERT still acks only when the data is durably written.

## Mechanics

The client keeps sending ordinary small INSERTs; the server appends each to an in-memory buffer per table and creates a real [[What is a data part in ClickHouse]] only on a flush trigger: data size reaches `async_insert_max_data_size` (default 100 MiB), the busy timeout fires (`async_insert_busy_timeout_ms`, 200 ms by default, 1000 ms on Cloud), or `async_insert_max_query_number` (450) queries accumulated. Since 24.2 the timeout is adaptive by default (`async_insert_use_adaptive_busy_timeout`), flexing between 50 ms and the max based on the incoming data rate — short waits at high rates, longer batching at low ones. The ack semantics are the sharp edge: `wait_for_async_insert = 1` blocks the client until its data is flushed to storage; `wait_for_async_insert = 0` is fire-and-forget — the docs call it very risky, because the client never learns about errors and no backpressure is applied to an overloading writer.

```sql
-- per-user/profile setting or INSERT-level
INSERT INTO hits SETTINGS async_insert = 1, wait_for_async_insert = 1
VALUES ('2026-09-11', 42, 'purchase');

-- check what the server accumulated
SELECT * FROM system.async_inserts LIMIT 5;
```

**Listing 1.** The recommended combination, and `system.async_inserts` for inspection of queued inserts.

> [!warning] Async inserts are not a license to never batch
> The buffer merges rows into *a* part, but per-query overhead, per-column serialization, and monitoring granularity still punish pathological writers; and deduplication of retries needs `async_insert_deduplicate` — identical blocks only, which fire-and-forget clients undermine by design. The docs' own insert-strategy guidance still targets batches of at least ~1000+ rows; async inserts are the safety net for unavoidable small writers ([[What causes Too many parts in ClickHouse]] explains the cost they prevent).

> [!tip] Interview answer
> Async inserts buffer small INSERTs server-side and flush one part per size/time/count thresholds — 100 MiB, ~200 ms adaptive, 450 queries by default. With wait_for_async_insert=1 the write still acks on durability, which is the recommended setting; wait_for_async_insert=0 trades guaranteed delivery for latency. It's how you let many tiny producers write a MergeTree table without killing it with parts.
