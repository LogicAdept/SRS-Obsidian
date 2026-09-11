<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is table bloat in PostgreSQL?

> [!abstract] Short answer
> Bloat is wasted space inside table or index files: pages full of dead tuples and reusable free space that the file never shrinks. MVCC leaves garbage behind on every update and delete; VACUUM marks the space reusable inside the file, but the file only stops growing — it does not get smaller. Bloat slows sequential scans and index range scans, and inflates cache pressure.

## Where it comes from

1. Dead tuples not yet vacuumed ([[What is a dead tuple in PostgreSQL]]) — transient bloat.
2. Vacuumed-but-not-shrunk space: after VACUUM the pages are reusable but the file keeps its high-water mark — persistent bloat.
3. Update-heavy workloads with low HOT ratio that also fatten indexes ([[What is a HOT update in PostgreSQL]]).
4. Long transactions pinning the horizon so autovacuum cannot keep up ([[Why do long-running transactions hurt PostgreSQL]]).

```d2
src: "UPDATE / DELETE churn" {width: 240; height: 60}
b1: "Transient bloat\ndead tuples await VACUUM" {width: 300; height: 80}
b2: "Persistent bloat\nfile keeps high-water mark" {width: 300; height: 80}
fix1: "VACUUM / autovacuum\ntuned per table" {width: 280; height: 70}
fix2: "Rewrite: VACUUM FULL\nor pg_repack, or drop partitions" {width: 340; height: 80}
src -> b1 -> fix1
b1 -> b2: "vacuum only marks space"
b2 -> fix2
```

**Fig. 1.** Two layers of bloat need different tools: garbage removal fixes the first, a physical rewrite fixes the second.

## Measuring it

- Cheap estimate: `pg_stat_user_tables`.`n_dead_tup` versus `n_live_tup`, plus table size from `pg_total_relation_size`.
- Precise: the `pgstattuple` extension reports the exact percentage of dead tuples and free space per table.
- Index bloat: repeated index scans reading few rows, or `pgstattuple` on the index; a freshly REINDEXed copy is often several times smaller.

## Fixing it

Prevention is autovacuum tuning: per-table `autovacuum_vacuum_scale_factor` on big tables (a flat 0.2 on a 500 GB table means vacuum triggers only after 100 GB of churn), plus cost limits. The cure for persistent bloat is a rewrite: VACUUM FULL under an exclusive lock ([[What is the difference between VACUUM and VACUUM FULL]]), online pg_repack ([[What is pg_repack]]), or dropping/reattaching partitions when the schema allows ([[How does PostgreSQL declarative partitioning work]]).

> [!warning] Bloat is not "rows deleted but disk full" only at file level
> Index bloat often matters more than heap bloat: index scans touch far more pages, and the planner's cost model inflates. "I ran VACUUM, why is the table still 100 GB?" — VACUUM never shrinks files; asking for VACUUM FULL on production during business hours is the next popular mistake ([[What is ACCESS EXCLUSIVE in PostgreSQL]]).

> [!tip] Interview answer
> Bloat is wasted file space from MVCC churn: dead tuples, then reusable-but-unreturned pages after vacuum, plus fat indexes. You measure it with n_dead_tup and pgstattuple, prevent it with autovacuum tuning and HOT-friendly design, and cure persistent bloat with VACUUM FULL, pg_repack, or partition drops — plain VACUUM never shrinks a file.
