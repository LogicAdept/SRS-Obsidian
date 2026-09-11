<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What do cost rows and loops mean in EXPLAIN?

> [!abstract] Short answer
> In PostgreSQL's EXPLAIN: **cost** = planner's arbitrary units of estimated work (`cost=startup..total`, relative only); **rows** = estimated output rows of the node; **loops** = how many times the node repeats. Total time of a repeated node is per-loop time times loops — the number that actually matters. SQLite exposes the same idea through actual row counts per step in ANALYZE output ([[How do you use EXPLAIN ANALYZE in SQL]]).

Cost is *not* time — PostgreSQL's documentation is explicit that costs are an abstract unit calibrated against sequential page fetches, meaningful only relative to other plans for the same planner settings. The `startup` component is work before the first row (sorters that must consume all input have high startup cost — why `EXPLAIN` shows cost jumps at sort nodes) ([[What is filesort or an external merge in a plan]]). Rows estimates come from statistics: table sizes and per-column histograms ([[How do stale statistics hurt a query plan]]); when the estimate is wrong by orders of magnitude, every join-order decision downstream inherits the error. Loops carry the multiplication trap: PostgreSQL prints per-loop averages, and the node's real cost is `per-loop time x loops`; SQLite's ANALYZE reports actual rows and loops per opcode for the same purpose. Reading recipe: walk the tree root-down, find the node whose `actual rows x loops` dominates, and check whether its estimate matched reality — that single comparison localizes most bad plans ([[What is the difference between Nested Loop Hash Join and Merge Join]]).

```sql
EXPLAIN QUERY PLAN
SELECT COUNT(*) FROM orders o JOIN customers c ON c.id = o.customer_id;
-- QUERY PLAN
-- |--SCAN o
-- `--SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
-- (PostgreSQL prints the same shape with per-node metrics, per its docs:
--  cost=0.15..8.17 rows=1 width=... and inner nodes tagged loops=N)
```

**Listing 1.** Verified on SQLite 3.53.1 for the plan shape; the cost/rows/loops vocabulary comes from PostgreSQL's EXPLAIN documentation, which defines cost as planner units and rows as estimates. The scanning outer node runs once; the keyed search runs once per outer row — loops.

```d2
direction: right
c1: "cost
planner units, relative
startup..total" {width: 220; height: 90}
c2: "rows
estimated output per loop" {width: 220; height: 90}
c3: "loops
repetitions multiply cost" {width: 210; height: 90}
t: "real time = per-loop time x loops" {width: 250; height: 80}
c1 -> t
c2 -> t
c3 -> t
```

**Fig. 1.** Three estimate columns feed one conclusion: multiply by loops, compare with the estimate, and the outlier node is where the plan went wrong.

> [!warning] Estimated rows off by 10x+ is the red flag, not the cost number
> Costs are uncalibrated units — comparing cost values across different queries or servers is meaningless. What transfers between systems is the *pattern*: rows estimates matching actuals, loops bounded, no sort node feeding a large LIMIT. Quote estimates against actuals, never cost against clock time ([[What is sargability in SQL]]).

> [!tip] Interview answer
> In EXPLAIN output, cost is the planner's relative work estimate — startup to total, units, not milliseconds; rows is the estimated number of rows the node emits per iteration; loops is how many times it runs, and the real cost of an inner node is its per-loop time times loops. Estimates come from table statistics, so a badly wrong rows value means stale or missing stats and poisons every decision above it. I find the dominant node by actual-times-loops and check its estimate against reality first.
