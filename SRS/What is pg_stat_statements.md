<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is pg_stat_statements?

> [!abstract] Short answer
> The standard extension for SQL workload statistics: it tracks planning and execution numbers — calls, total and mean time, rows, shared block hits and reads, temp block usage — per normalized query fingerprint across the whole server. It is the "which queries actually hurt" view, and the input for most slow-query triage.

## Setup and mechanics

The module must be preloaded (it needs shared memory): `shared_preload_libraries = 'pg_stat_statements'` in postgresql.conf plus a server restart, then `CREATE EXTENSION pg_stat_statements` in the database where you want the view. Query identity comes from the compute_query_id fingerprint: similar statements with different literals collapse into one row, so 10,000 calls of the same query with different IDs are one entry with `calls = 10000`.

```sql
SELECT calls, mean_exec_time, total_exec_time, rows,
       shared_blks_read, temp_blks_written, query
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;
```

**Listing 1.** The classic top-ten by total time; the same view ordered by mean time or by `temp_blks_written` (sort spills) answers different questions.

```d2
norm: "Normalize SQL\nliterals -> fingerprint" {width: 300; height: 70}
acc: "Accumulate per fingerprint\ncalls, time, rows, blocks" {width: 320; height: 80}
view: "pg_stat_statements view\none row per query shape" {width: 300; height: 70}
reset: "pg_stat_statements_reset\nfor measurement windows" {width: 310; height: 70}
norm -> acc -> view
reset -> acc
```

**Fig. 1.** Statistics are cumulative since the last reset; deliberate resets give clean measurement windows.

## What to look for

- `total_exec_time` dominance — the workhorses worth tuning first ([[How do you debug a slow PostgreSQL query]]).
- High `mean_exec_time` with low calls — the batch monsters.
- `shared_blks_read` high relative to hit — I/O bound queries; missing indexes or cache pressure ([[What are shared_buffers and work_mem in PostgreSQL]]).
- `temp_blks_written` — sorts and hashes spilling to disk.
- Planning time anomalies on high-frequency statements.

It pairs with `pg_stat_activity` for the "right now" picture ([[How would you explain pg_stat_activity pg_stat_statements]]), and with `pg_stat_user_indexes` when you decide what to drop ([[How do you find unused indexes in PostgreSQL]]).

> [!warning] Track limits and normalization traps
> The module keeps a bounded number of distinct fingerprints; under extreme query-shape churn least-used entries are deallocated, so numbers can surprise. Long literals are normalized, but parameters inside `IN (...)` lists of varying length create separate entries. And per-statement timing is sampled — mean_exec_time is a good guide, not a stopwatch.

> [!tip] Interview answer
> pg_stat_statements is a preload extension that aggregates execution stats per normalized query fingerprint: calls, total and mean time, rows, block hits and reads, temp spills. I use it to rank the workload by total time and to spot I/O-bound or spilling queries; it is cumulative since reset, so I combine it with pg_stat_activity for the live picture.
