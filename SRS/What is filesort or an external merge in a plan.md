<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is filesort or an external merge in a plan?

> [!abstract] Short answer
> **Filesort** is MySQL's name for a sort node in the plan — rows are collected and sorted (in memory, or spilled to disk in runs and merged) because no index supplied the required order. SQLite names the equivalent `USE TEMP B-TREE FOR ORDER BY`; PostgreSQL shows a `Sort` node. It is a blocking operator: output starts only after all input is read and ordered.

The name is MySQL jargon but the mechanism is universal, and the cure is the same: make an index supply the order so no sort node exists. The demo shows the full arc on SQLite: ordering by price without an index produces `SCAN products` plus `USE TEMP B-TREE FOR ORDER BY`; after creating the index, the plan is `SCAN products USING INDEX idx_price` and the temp b-tree is gone — rows already arrive in order. PostgreSQL documents its own variants in the EXPLAIN output: `Sort` with `Sort Method: quicksort / external merge / external sort` — the "external merge" phrase in this interview question is exactly the spill-to-disk path, chosen when the sort does not fit in `work_mem`. The interview-worthy connections: a sort feeding a `LIMIT` may be optimized to a top-N heap (bounded memory), sorts invalidate index-order optimizations ([[How do you avoid a sort with an index]]), and a `DISTINCT` or `GROUP BY` without a usable index carries the same blocking cost ([[Why is SELECT DISTINCT expensive]]).

```sql
CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT, price NUMERIC);
INSERT INTO products VALUES (1,'Cable',10.0),(2,'Monitor',250.0),(3,'Chair',120.0);

EXPLAIN QUERY PLAN SELECT title FROM products ORDER BY price;
-- QUERY PLAN
-- |--SCAN products
-- `--USE TEMP B-TREE FOR ORDER BY
CREATE INDEX idx_price ON products(price);
EXPLAIN QUERY PLAN SELECT title FROM products ORDER BY price;
-- QUERY PLAN
-- `--SCAN products USING INDEX idx_price
```

**Listing 1.** Verified on SQLite 3.53.1. Before the index: full scan plus a temporary b-tree to sort — the filesort. After: the index scan emits rows already ordered and the sort node disappears entirely.

```d2
direction: right
in: "input rows
any order" {width: 150; height: 70}
s: "sort node
in-memory or spill + merge" {width: 230; height: 80}
out: "ordered output
starts after ALL input" {width: 220; height: 80}
in -> s -> out
```

**Fig. 1.** A sort is a full barrier: every input row must be read, ordered, and only then can output begin — which is why index-supplied order is a plan-level prize.

> [!warning] A sort under a LIMIT still sorts everything unless the engine top-N optimizes it
> `ORDER BY x LIMIT 10` without an index sorts the whole input (memory-bounded top-N at best); with an index on x it reads exactly 10 index entries. The difference is plan-level, not parameter tuning — check the plan for the sort node before blaming the LIMIT ([[How does LIMIT interact with ORDER BY and indexes]]).

> [!tip] Interview answer
> Filesort is MySQL's term for the plan's sort node — rows buffered, sorted in memory or spilled to disk and merged, SQLite calls it a temp b-tree for ORDER BY, PostgreSQL a Sort node with external merge as the spill case. It is blocking: nothing is returned until all input is sorted. The fix is structural — an index whose key order matches the ORDER BY, which turns the sort node into an ordered index scan — and I check plans for it the same way I check for scans.
