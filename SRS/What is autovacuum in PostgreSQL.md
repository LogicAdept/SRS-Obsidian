<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is autovacuum in PostgreSQL?

> [!abstract] Short answer
> Autovacuum is the background subsystem that runs VACUUM and ANALYZE automatically: a launcher wakes every `autovacuum_naptime` (1 minute by default) and up to `autovacuum_max_workers` (3) workers vacuum tables whose dead-tuple or insert counts crossed their thresholds. It also force-vacuums tables as they approach transaction ID wraparound — even if you disabled it.

## Trigger conditions

For each table, autovacuum compares statistics counters against a threshold:

- vacuum threshold: `autovacuum_vacuum_threshold` (50) `+ autovacuum_vacuum_scale_factor` (0.2) `* reltuples`, capped by `autovacuum_vacuum_max_threshold` (100 million tuples);
- insert-only vacuum: `autovacuum_vacuum_insert_threshold` (1000) `+ autovacuum_vacuum_insert_scale_factor` (0.2) — added so append-only tables still get visibility-map maintenance;
- analyze threshold: 50 + 0.1 * reltuples.

A table whose `relfrozenxid` age exceeds `autovacuum_freeze_max_age` (200 million transactions) is vacuumed regardless of these thresholds.

```d2
launcher: "Autovacuum launcher\nwakes every naptime (1min)" {width: 320; height: 80}
w1: "Worker 1" {width: 160; height: 60}
w2: "Worker 2" {width: 160; height: 60}
w3: "Worker 3\n(max_workers)" {width: 170; height: 60}
db: "Databases / tables\nordered by need" {width: 280; height: 70}
launcher -> w1: "assigns table"
launcher -> w2
launcher -> w3
w1 -> db
```

**Fig. 1.** The launcher is a scheduler; the workers do the vacuuming, at most `autovacuum_max_workers` concurrently across the whole cluster.

## Cost throttling

Workers vacuum with a cost budget: `vacuum_cost_limit` (200) delay points, with a delay of `autovacuum_vacuum_cost_delay` (2 ms) so background vacuuming does not saturate I/O. This is why a huge table can take a long time to vacuum — the throttle is intentional, and per-table storage parameters (`autovacuum_vacuum_scale_factor` on the table) let you tune hot big tables individually.

## What to watch

- `pg_stat_user_tables`: `n_dead_tup`, `last_autovacuum`, `autovacuum_count`.
- Server log with `log_autovacuum_min_duration` (default 10 min in recent versions).
- Workers are also blocked by the snapshot horizon: a long transaction can make every worker run uselessly ([[Why do long-running transactions hurt PostgreSQL]]).

> [!warning] Disabling autovacuum is not a tuning strategy
> Setting `autovacuum = off` on a hot table only postpones the problem and leaves wraparound vacuums intact — they run anyway. The real fix is per-table scale factors, more workers, or a manual schedule. Also remember statistics: without ANALYZE (autovacuum does it too) the planner flies blind ([[How do stale statistics hurt a query plan]]).

> [!tip] Interview answer
> Autovacuum is a launcher plus a few workers that VACUUM and ANALYZE tables when dead tuples exceed roughly 20 percent of the table (plus a base threshold), keeping statistics fresh and pushing wraparound protection. Tuning means per-table scale factors and cost limits, not turning it off — anti-wraparound vacuums run even when it is disabled.
