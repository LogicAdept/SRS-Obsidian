<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS

# How do you find unused indexes in PostgreSQL?

> [!abstract] Short answer
> Query `pg_stat_user_indexes` and look for indexes whose `idx_scan` is zero or tiny over a representative period, then cross-check their size with `pg_relation_size` and their write burden with `pg_stat_user_tables`. Every index is pure cost if no plan uses it — maintenance on each write with no reads in return.

## The core query

```sql
SELECT s.schemaname, s.relname AS table, s.indexrelname AS index,
       s.idx_scan, pg_size_pretty(pg_relation_size(s.indexrelid)) AS size
FROM pg_stat_user_indexes s
JOIN pg_index i ON i.indexrelid = s.indexrelid
WHERE NOT i.indisunique AND NOT i.indisprimary
  AND s.idx_scan < 10
ORDER BY pg_relation_size(s.indexrelid) DESC;
```

**Listing 1.** Candidate list: non-unique, non-primary indexes with almost no scans, biggest first. Unique and primary-key indexes are exempt — they enforce constraints, not just speed.

## Doing it honestly

- Counters reset at restart: `stats_reset` in `pg_stat_database` tells you the window; a week covering month-end is better than two quiet days.
- Exclusions matter: indexes backing constraints (unique, exclusion [[What is an exclusion constraint in PostgreSQL]]), partial indexes for rare jobs ([[What is a partial index in PostgreSQL]]), and indexes used only by infrequent reports or batch jobs.
- Cross-check with `pg_stat_user_tables`: `n_tup_ins/upd/del` shows what dropping saves. A small unused index on a table with millions of updates is a good early drop.

```d2
collect: "pg_stat_user_indexes\nidx_scan over weeks" {width: 300; height: 80}
filter: "Drop candidates\nno scans + not a constraint\n+ meaningful size" {width: 320; height: 90}
drop: "DROP INDEX CONCURRENTLY\nin a quiet window" {width: 300; height: 80}
monitor: "Keep the DDL; watch plans\nre-create if a plan regresses" {width: 340; height: 80}
collect -> filter -> drop -> monitor
```

**Fig. 1.** The safe loop: measure, filter, drop non-blockingly, keep the DDL to roll back.

## The removal itself

Drop with `DROP INDEX CONCURRENTLY` so writes never block ([[How do you create an index without blocking writes in PostgreSQL]]). If some plan then regresses, recreating is cheap and non-blocking. Benefits are immediate: fewer write amplification paths, smaller cache footprint, faster HOT-less updates ([[What is a HOT update in PostgreSQL]]).

> [!warning] idx_scan counts uses, not usefulness
> An index scanned 50 times a day by a nightly batch looks "used"; one scanned twice a year looks unused. Counters also do not tell you the plan's quality. Correlate with actual workloads (pg_stat_statements' query mix) before dropping — [[What is pg_stat_statements]].

> [!tip] Interview answer
> I look at pg_stat_user_indexes joined with pg_index: non-unique, non-PK indexes with near-zero idx_scan over a representative window, sorted by size, cross-checked against table write volume. Drops go out with DROP INDEX CONCURRENTLY, and the DDL is kept for rollback. Every removed index is less write amplification for free.
