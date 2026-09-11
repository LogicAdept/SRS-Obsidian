<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> **Partition pruning** lets the engine skip entire partitions of a partitioned table when the query's predicates prove they cannot contain matching rows: `WHERE created_at BETWEEN '2024-01-01' AND '2024-01-31'` on a monthly-partitioned table touches one partition instead of all of them. PostgreSQL documents it as a core feature of declarative partitioning, enabled by `enable_partition_pruning` (on by default).

The mechanism is plan-time constraint math: the partition key's bounds (range lists or hash) are known to the planner, so predicates on the partition key are compared against each partition's range and non-overlapping ones are excluded from the plan — PostgreSQL's partitioning documentation shows the EXPLAIN difference as one `Seq Scan` on the matching partition versus one per partition. Two conditions for pruning that interviews probe: the predicate must be on the **partition key** (filtering on any other column prunes nothing), and values must be known at plan time — constants and parameters prune fully; a predicate on a *joined* column prunes only at execution time (the documented "runtime pruning" with `InitPlan` parameters). SQLite has no partitioned tables; the same discipline is emulated with sharding-by-table and UNION ALL views — the verified demo shows the engine pushing the WHERE into each branch and probing each branch's primary key, i.e., constraint pushdown replacing pruning ([[What harmful SQL patterns or pitfalls do you know]]). The payoff framing: pruning is data-locality on the scan axis — it divides the scanned bytes by the number of partitions — while indexes divide it further *within* the surviving partition; the two compose ([[How do you optimize COUNT star on a large table]]).

```sql
CREATE TABLE o2023 (id INTEGER PRIMARY KEY, amount NUMERIC);
CREATE TABLE o2024 (id INTEGER PRIMARY KEY, amount NUMERIC);
INSERT INTO o2023 VALUES (1, 100);
INSERT INTO o2024 VALUES (1, 200);

EXPLAIN QUERY PLAN
SELECT * FROM (
  SELECT id, amount FROM o2023
  UNION ALL
  SELECT id, amount FROM o2024
) t WHERE id = 1;
-- QUERY PLAN
-- |--COMPOUND QUERY
-- |  |--LEFT-MOST SUBQUERY
-- |  |  `--SEARCH o2023 USING INTEGER PRIMARY KEY (rowid=?)
-- |  `--UNION ALL
-- |     `--SEARCH o2024 USING INTEGER PRIMARY KEY (rowid=?)
```

**Listing 1.** Verified on SQLite 3.53.1. The UNION ALL "partitions" get the WHERE pushed down and each branch is probed by primary key — the emulated shape. PostgreSQL's native pruning goes further: non-matching partitions are removed from the plan entirely, leaving a single scan node.

```d2
direction: right
q: "WHERE key in Jan 2024" {width: 200; height: 70}
p1: "2023 partitions
pruned from plan" {width: 170; height: 80}
p2: "2024-01 partition
scanned" {width: 170; height: 80}
p3: "2024-02..12
pruned" {width: 150; height: 80}
q -> p1
q -> p2
q -> p3
```

**Fig. 1.** Partition bounds turn date predicates into partition sets: the planner subtracts non-overlapping partitions, and only the survivors are ever read.

> [!warning] Wrapping the partition key in a function or cross-partition logic disables pruning
> `WHERE date(created_at) = '2024-01-15'` computes on every partition (no key predicate), and `WHERE created_at = other_table.col` prunes only at runtime, if the planner can bind it. Keep predicates bare on the partition key and range-shaped — pruning and sargability fail for the same reasons ([[What is sargability in SQL]]).

> [!tip] Interview answer
> Partition pruning means the planner drops partitions whose bounds cannot satisfy the query's predicate on the partition key — a month filter on monthly partitions scans one partition instead of twelve. It needs a bare predicate on the partition key with plan-time values; cross-table predicates only get runtime pruning. SQLite has no partitions but shows the same idea via UNION ALL with pushed-down constraints; in PostgreSQL, pruning plus indexes within the surviving partition compose into the full scan strategy.
