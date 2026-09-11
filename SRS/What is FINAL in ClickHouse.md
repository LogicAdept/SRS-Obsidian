<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SystemDesign/Performance #SRS

# What is FINAL in ClickHouse?

> [!abstract] Short answer
> `SELECT ... FROM t FINAL` fully merges the queried data before returning it: it applies all merge-time transformations of the table engine — ReplacingMergeTree dedup, Summing/Collapsing folding — at query time, in memory. It guarantees engine-consistent results without waiting for background merges, at the cost of extra compute, memory, and primary-key column reads.

## Semantics and cost

The reference is blunt: FINAL is "slightly slower" because the work that normally happens in background merges must happen at query time; it can read primary-key columns beyond those in the SELECT; execution is parallel, bounded by `max_final_threads`; and it is still cheaper than forcing merges with OPTIMIZE for query correctness. You can also flip it session-wide with the `final = 1` setting, which applies FINAL to all tables in queries — convenient for CDC-fed tables, expensive as a habit. FINAL composes with WHERE; the merge scope is effectively restricted by the key columns in the filter, which is why filtering by key alongside FINAL matters for latency.

```sql
-- correct single row per key, whether or not merges have run
SELECT id, name, updated_at
FROM users FINAL
WHERE id IN (101, 102);

-- the common alternative: dedup by aggregation, no FINAL
SELECT id, argMax(name, updated_at) AS name, max(updated_at)
FROM users
WHERE id IN (101, 102)
GROUP BY id;
```

**Listing 1.** FINAL versus the argMax aggregation pattern — both return the newest version per key.

## When to use it

On tables fed by CDC upserts ([[What is the Kafka to ClickHouse materialized view pattern]], [[What is ReplacingMergeTree]]), FINAL is the honest read contract: "give me current state per key now". For heavy aggregate dashboards, re-deriving state with GROUP BY/argMax or pre-merging through a materialized view is usually cheaper. Note the interplay with projections — the docs state projections do not support SELECT with FINAL — so a FINAL-read table cannot lean on that optimization for its point-read patterns.

> [!warning] FINAL is not a transaction isolation level
> It does not make ClickHouse transactional, does not lock anything, and does not wait for in-flight inserts: a row inserted *after* your query starts is still invisible, and its guarantee is "all data present at query start, engine-merged". Calling FINAL "strong consistency" in an interview confuses a read-time merge with ACID — ClickHouse has no full-fledged transactions ([[When should you not use ClickHouse]]).

> [!tip] Interview answer
> FINAL forces query-time merging: the engine applies Replacing/Summing/Collapsing transformations in memory so the answer reflects all merges as if they had happened. It costs compute and extra key-column reads, is parallelized up to max_final_threads, and is the standard read pattern for upsert-fed tables — with argMax aggregation as the cheaper alternative when the query shape allows it.
