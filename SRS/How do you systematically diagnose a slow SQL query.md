<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> The systematic loop: (1) **reproduce with numbers** — identify the statement and its frequency (top-by-time, not one-off latency); (2) **read the plan** — EXPLAIN for the shape, ANALYZE for actual rows/loops; (3) **name the dominant node** — the one doing the most work; (4) **test the hypothesis** — index, rewrite, or statistics fix; (5) **verify by plan and by measurement**, then re-check after data growth. The discipline is evidence-first: no change before the plan names the cause ([[How do you identify slow or non-performant SQL queries]]).

Steps three to five are where the discipline pays. Naming the dominant node forces a mechanism claim — "this index seek runs once per row of a 10M-row outer scan" — which is falsifiable; the verified demo shows the fix completing the loop: after an index on the join column, the plan flips from scan/scan to scan/SEARCH (`SEARCH big_a USING COVERING INDEX (x=?)`) and the measured time drops from 0.34 ms to 0.02 ms on the quadratic demo — but the *verification of the plan shape*, not the timing, is the evidence that the cause was addressed. Hypothesis classes map to node shapes: scan-where-seek-expected means index or sargability ([[What is sargability in SQL]]); estimated-rows-far-from-actual means statistics ([[How do stale statistics hurt a query plan]]); sort-under-LIMIT means order-supplying index ([[How does LIMIT interact with ORDER BY and indexes]]); thousands of identical small statements mean N+1 in the application ([[What is the N plus 1 problem in SQL]]). The last step — re-check after growth — closes the loop because plans are decisions for one moment, not properties ([[What is a query plan in a relational database]]).

```sql
CREATE TABLE big_a (x INTEGER);
CREATE TABLE nums_b (y INTEGER);
INSERT INTO nums_b VALUES (6),(7),(8),(9),(10),(11),(12),(13),(14),(15);
CREATE INDEX idx_ba_x ON big_a(x);

EXPLAIN QUERY PLAN
SELECT COUNT(*) FROM big_a, nums_b WHERE big_a.x = nums_b.y;
-- QUERY PLAN
-- |--SCAN nums_b
-- `--SEARCH big_a USING COVERING INDEX idx_ba_x (x=?)
-- (was: SCAN nums_a / SCAN nums_b, 0.34 ms at 640 x 10 rows -> 0.02 ms)
```

**Listing 1.** Verified on SQLite 3.53.1. The post-fix plan names the new strategy — scan the small side once, seek the indexed side per row — which is the evidence that the diagnosis (missing index on the join column) was correct.

```d2
direction: right
d1: "1 identify statement
+ frequency" {width: 180; height: 80}
d2: "2 read plan
static + actuals" {width: 160; height: 80}
d3: "3 name dominant node" {width: 180; height: 80}
d4: "4 fix: index / rewrite / stats" {width: 200; height: 80}
d5: "5 verify plan + measure" {width: 180; height: 80}
d1 -> d2 -> d3 -> d4 -> d5
```

**Fig. 1.** The loop is evidence in, evidence out: the plan names the disease, the fix changes the plan, and the changed plan — not hope — closes the case.

> [!warning] Verifying by timing alone accepts placebo fixes
> The same query runs faster ten minutes later for cache, statistics or load reasons; a fix is accepted only when the plan shape changed as predicted *and* the measurement improved under comparable conditions. Checklists and before/after plans beat "it feels faster" ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> My loop is: identify the statement and how often it runs; read the plan — EXPLAIN for shape, ANALYZE for actual rows and loops; name the dominant node and turn it into a mechanism claim; apply the matching fix — index or sargability for scan-where-seek, statistics for estimate drift, rewrite or fetch batching for application-side patterns; then verify that the plan changed as predicted and measure under comparable load. No change before the plan names a cause, and no fix accepted on timing alone.
