<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# How do stale statistics hurt a query plan

> [!abstract] Short answer
> The planner chooses plans from estimates, and estimates come from statistics: row counts, distinct values, most common values, histograms. If those numbers are stale — after bulk loads, mass deletes, or skewed growth — the planner misestimates matching rows and picks structurally wrong plans, like a nested loop over millions of rows where a hash join was right.

## Where the numbers live and how they age

PostgreSQL keeps table and index sizes in pg_class (reltuples, relpages) and column distributions in pg_statistic, exposed readably through pg_stats; ANALYZE fills them, autoanalyze triggers on the fraction of changed rows, and the values are deliberately approximate — the docs note reltuples is not updated on the fly and is scaled to the current table size. Per-column detail is bounded by the statistics target (default 100 entries in most_common_vals and the histogram), and correlated columns fool per-column independence assumptions until you add extended statistics (CREATE STATISTICS with dependencies, mcv lists, or ndistinct). MySQL 8 keeps persistent InnoDB statistics (innodb_stats_persistent) and refreshes via ANALYZE TABLE, with automatic recomputation after a fraction of rows change.

```sql
ANALYZE orders;                       -- refresh column stats
ALTER TABLE orders ALTER COLUMN customer_id SET STATISTICS 500;
CREATE STATISTICS stts (dependencies) ON city, zip FROM addresses;
ANALYZE addresses;
SELECT attname, n_distinct, most_common_vals FROM pg_stats
WHERE tablename = 'orders' AND attname = 'customer_id';
```

**Listing 1.** Refresh, raise the target on skewed columns, and teach the planner about correlated columns.

## The failure mode and the repair loop

A misestimate flips join strategy and scan choice: a predicate estimated at 10 rows when it matches 2 million turns into a nested loop with per-row index seeks, the disaster combination described in [[What is the difference between Nested Loop Hash Join and Merge Join]]; the inverse mistake buries a good index under a needless hash build. In an interview, demonstrate the loop rather than the blame: read the plan against actuals with EXPLAIN ANALYZE ([[How do you read EXPLAIN ANALYZE in PostgreSQL]]), compare estimated versus actual rows, then refresh or refine statistics ([[How does the PostgreSQL query planner choose a plan]] walks the decision inputs). Bulk operations deserve a manual ANALYZE precisely because autoanalyze lags on the changed-fraction trigger.

> [!warning] "Vacuum full fixes bad plans" — wrong tool
> VACUUM reclaims dead tuples; ANALYZE refreshes planner statistics. Running VACUUM after a load and expecting estimate-driven plans to change confuses the two; only ANALYZE (or autoanalyze catching up) updates pg_statistic. The second half-myth: fresh statistics do not fix everything — misestimates from correlated columns need extended statistics or query restructuring, not just a newer ANALYZE.

> [!tip] Interview answer
> Plans are costed from estimates, and estimates come from statistics that age with the data. Stale or too-coarse statistics make the planner misjudge selectivity and pick the wrong join or scan — a 10-row estimate against 2 million actuals turns into a nested loop catastrophe. Diagnose with EXPLAIN ANALYZE comparing estimated and actual rows, then ANALYZE, raise the statistics target on skewed columns, and add extended statistics for correlated columns.
