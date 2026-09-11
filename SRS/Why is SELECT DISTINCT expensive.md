<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# Why is SELECT DISTINCT expensive?

> [!abstract] Short answer
> `DISTINCT` is a blocking dedup operator: the engine must compare **every output row** against all rows seen so far — via a sort or a hash — before it can emit anything. Cost grows with result size, not with table size, and it cannot stream. `EXPLAIN QUERY PLAN` names it explicitly on SQLite: `USE TEMP B-TREE FOR DISTINCT`.

Why it appears where it does not belong: most production DISTINCTs are bandages over join fan-out — the query multiplied rows, DISTINCT folds them back, and the reviewer sees a "working" plan that did all the duplication work first ([[Why can a JOIN multiply your row count]]). Three honest alternatives exist per case: an `EXISTS` semi-join that never duplicates (the demo shows SQLite planning it with a bloom filter and an index probe — no temp b-tree); pre-aggregation before the join; or fixing the join condition itself. When dedup *is* the requirement, DISTINCT is fine — dedup of a small projection (one indexed column) can even use an index and skip the sort. What makes DISTINCT expensive in practice: wide rows (the dedup key is the whole row), millions of group keys (hash/sort spills to disk on PostgreSQL — `work_mem`), and DISTINCT over expressions that defeat index use ([[What is the difference between GROUP BY and DISTINCT]], [[What is sargability in SQL]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO customers VALUES (1,'Alice','Berlin'),(2,'Boris',NULL),(3,'Carla','Berlin');

EXPLAIN QUERY PLAN SELECT DISTINCT c.city FROM customers c
JOIN orders o ON o.customer_id = c.id;
-- QUERY PLAN
-- |--SCAN o
-- |--SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
-- `--USE TEMP B-TREE FOR DISTINCT
EXPLAIN QUERY PLAN SELECT city FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
-- QUERY PLAN
-- |--SCAN c
-- |--BLOOM FILTER ON o (customer_id=?)
-- `--SEARCH o EXISTS USING AUTOMATIC PARTIAL COVERING INDEX (customer_id=?)
```

**Listing 1.** Verified on SQLite 3.53.1. Same business question ("cities that ordered"): the DISTINCT form materializes the multiplied join and dedups in a temp b-tree; the EXISTS form never duplicates a row, so there is nothing to dedup.

```d2
direction: right
j: "join (fan-out)
N x M rows" {width: 170; height: 70}
d: "DISTINCT
sort/hash all rows" {width: 180; height: 70}
o1: "deduped output
late, blocking" {width: 180; height: 70}
e: "EXISTS semi-join
first match per row" {width: 200; height: 70}
o2: "output
streaming, no dedup" {width: 180; height: 70}
j -> d -> o1
e -> o2
```

**Fig. 1.** Two shapes for one question: the blocking pipeline pays for duplication then removes it; the semi-join never produces duplicates at all.

> [!warning] DISTINCT changes results, not just plans — verify before deleting it
> Removing a DISTINCT that *was* correct (dedup of genuinely duplicate rows from a UNION or a self-join) silently multiplies output rows; removing a fan-out bandage changes nothing but makes the query faster. Diff outputs on production-like data before and after, then keep the version whose semantics are intentional ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> DISTINCT is a blocking operator — a sort or hash over the whole result to drop duplicate rows, so it costs by output size and cannot stream; SQLite plans literally say temp b-tree for distinct. Most DISTINCTs I see are patches over join fan-out, and the better fix is EXISTS, which stops at the first match and never duplicates, or pre-aggregation. When dedup is genuinely required I keep DISTINCT, ideally over a narrow or indexed projection so the engine can use an index instead of spilling a sort.
