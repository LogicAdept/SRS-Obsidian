<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How do you identify slow or non-performant SQL queries?

> [!abstract] Short answer
> A layering of signals, from cheap to deep: (1) **symptoms** — latency metrics, top-N by time (pg_stat_statements, slow query log); (2) **plans** — EXPLAIN for the shape, EXPLAIN ANALYZE for actual rows and loops; (3) **counts** — row counts fetched versus returned, sort nodes, scans; (4) **runtime** — I/O, waits, lock contention. The query that "is slow" is the one whose dominant plan node does work no one asked for ([[What is a query plan in a relational database]]).

The demo teaches the first two layers with a constructed pathology: an unindexed join with automatic index building disabled plans as two full scans — `SCAN nums_a` and `SCAN nums_b` — a nested loop doing N times M predicate evaluations (5 matches from 10x10 rows). Timings grow with the product of sizes: 40 outer rows cost 0.03 ms, 160 cost 0.08 ms, 640 cost 0.34 ms — the quadratic signature, visible in per-request latency graphs as "slower than data growth". The generic detection loop: find the statement (top-by-time list, not by eyeball), read its plan for scan/scan joins, sorts under LIMITs, or filters removing most fetched rows ([[What is Index Cond versus Filter in EXPLAIN]]), then compare estimated versus actual rows to test statistics freshness ([[How do stale statistics hurt a query plan]]). Runtime layer distinguishes CPU-bound plans (quadratic shapes) from I/O-bound (huge scans) and lock-bound (waits in pg_stat_activity / InnoDB lock waits) — three diseases with different doctors ([[What is the N plus 1 problem in SQL]]).

```sql
CREATE TABLE nums_a (x INTEGER);
CREATE TABLE nums_b (y INTEGER);
INSERT INTO nums_a VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);
INSERT INTO nums_b VALUES (6),(7),(8),(9),(10),(11),(12),(13),(14),(15);

EXPLAIN QUERY PLAN
SELECT COUNT(*) FROM nums_a, nums_b WHERE nums_a.x = nums_b.y;
-- QUERY PLAN
-- |--SCAN nums_a
-- `--SCAN nums_b
-- (nested full scans: N x M evaluations for the 5 matching rows)
-- measured growth of the same shape:
--   outer rows=40:   0.03 ms
--   outer rows=160:  0.08 ms
--   outer rows=640:  0.34 ms
```

**Listing 1.** Verified on SQLite 3.53.1 (automatic indexes off to expose the pathology). Two scans nested means work grows with the product of table sizes — the plan is the diagnosis before any timing is taken.

```d2
direction: right
s1: "symptom
latency, top-by-time" {width: 190; height: 80}
s2: "plan
EXPLAIN shape, ANALYZE actuals" {width: 230; height: 80}
s3: "node
dominant scan / sort / filter" {width: 210; height: 80}
s4: "cause
missing index, stale stats, contention" {width: 240; height: 80}
s1 -> s2 -> s3 -> s4
```

**Fig. 1.** Diagnosis descends one layer at a time: find the statement, read its plan, name the dominant node, and only then name the cause.

> [!warning] "It is slow" without a plan is a guess with a deadline
> Jumping from symptom to fix ("add an index") fixes the guessed disease; the plan names the actual one — sometimes it is contention, or statistics, or an ORM emitting thousands of small queries, none of which an index on the guessed column touches ([[How do you systematically diagnose a slow SQL query]]).

> [!tip] Interview answer
> I layer the diagnosis: first find the statement with top-by-time tooling like pg_stat_statements or the slow log; then read its EXPLAIN for shape and EXPLAIN ANALYZE for actual rows and loops; then name the dominant node — a scan that should be a seek, a sort feeding a LIMIT, a filter removing most fetched rows; then check estimates against actuals for stale statistics. The runtime layer separates CPU-bound shapes, I/O-bound scans and lock waits. The demo pathology is the scan-scan join whose cost grows with the product of sizes.
