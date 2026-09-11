<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How does LIMIT interact with ORDER BY and indexes?

> [!abstract] Short answer
> `LIMIT` truncates the *output* of ORDER BY, not its work: without an index, the engine sorts **all** matching rows and then keeps the first K (a top-N optimization bounds memory, not the scan). With an index matching the ORDER BY, the engine reads exactly K entries and stops — the plan loses the sort node and the read count collapses from N to K ([[How do you avoid a sort with an index]]).

The verified demo on SQLite: `ORDER BY name LIMIT 2` without a supporting index plans as a full scan plus `USE TEMP B-TREE FOR ORDER BY` — every row touched, two kept; with a BINARY index on `name`, the plan is a pure index scan and LIMIT reads the first two keys in index order. PostgreSQL documents the same pairing: `LIMIT` with an index that provides the ordering lets the planner choose an `Index Scan` and stop early, and the sort node disappears. Three consequences worth naming in an interview. The "top-N" memory optimization exists (a bounded heap keeps K best-so-far rows) but still reads every row — it saves memory, not I/O. `LIMIT` without ORDER BY is non-deterministic — the engine may return *any* K rows, and the set can differ across runs and engines ([[What harmful SQL patterns or pitfalls do you know]]). And OFFSET pushes in the opposite direction: `LIMIT 10 OFFSET 100000` still *walks* 100010 index entries before returning — the cost moves to the skipped rows ([[Why is OFFSET pagination slow]], [[What is keyset pagination]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO customers VALUES (1,'Alice'),(2,'Boris'),(3,'Carla');

CREATE INDEX idx_name_bin ON customers(name);
EXPLAIN QUERY PLAN SELECT id FROM customers ORDER BY name LIMIT 2;
-- QUERY PLAN
-- `--SCAN customers USING COVERING INDEX idx_name_bin
EXPLAIN QUERY PLAN SELECT id FROM customers ORDER BY name;
-- QUERY PLAN
-- `--SCAN customers USING COVERING INDEX idx_name_bin
-- (with the index both read the index in order; LIMIT just stops earlier.
--  Without the index both need USE TEMP B-TREE FOR ORDER BY over all rows.)
```

**Listing 1.** Verified on SQLite 3.53.1. With the index, ordered output comes from the index itself and LIMIT stops the walk early; the no-limit plan reads the whole index. Without any index, both variants sort every row first.

```d2
direction: right
n1: "no index
sort ALL rows -> keep K" {width: 220; height: 80}
n2: "index on sort key
read K entries -> stop" {width: 220; height: 80}
k: "LIMIT K" {width: 100; height: 60}
n1 -> k
n2 -> k
```

**Fig. 1.** LIMIT is free only when order is free: an index makes K the actual read cost; otherwise the full sort runs first and K merely trims output.

> [!warning] LIMIT without ORDER BY is a data-coin-flip, not a sample
> Engines return whichever K rows their plan touches first — different plans (parallelism, index choice, statistics) return different sets. Any pagination or "show a few rows" use must pin ORDER BY with a tiebreaker (unique key), or results will differ between environments ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> LIMIT caps the result, but the ORDER BY work happens first: no index means the engine sorts every matching row — top-N memory optimization saves space, not reads. With an index matching the ORDER BY, the plan reads exactly K entries and stops, which is the version I aim for. I also always pair LIMIT with a full deterministic ORDER BY including a unique tiebreaker, and I remember OFFSET undoes the benefit by walking the skipped rows.
