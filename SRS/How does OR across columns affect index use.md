<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> `WHERE a = 1 OR b = 2` cannot be served by *one* B-tree — each disjunct needs its own access path. Three resolutions exist: the engine combines **multiple indexes** (SQLite: `MULTI-INDEX OR`; PostgreSQL: bitmap OR over two `Bitmap Index Scans`), it rewrites same-column OR to `IN`, or — when no indexes apply — it scans. OR across columns is not a sargability killer; it is a plan-complexity tax ([[What is a bitmap index scan in SQL plans]]).

The verified demo shows the multi-index plan on SQLite: two indexes each serve one disjunct, and the plan merges them (`INDEX 1`, `INDEX 2` under `MULTI-INDEX OR`); PostgreSQL documents the equivalent as bitmaps from each index ORed together, then one heap pass in physical order. Same-column OR is easier: `city = 'Berlin' OR city = 'Paris'` rewrites to `city IN ('Berlin','Paris')` — one index, one seek per value (verified: single SEARCH with the index). The costs to know: each disjunct's index must be maintained, results must be **deduplicated** (a row matching both disjuncts must appear once — the merge machinery exists exactly for that), and if one disjunct is non-sargable (`OR f(col) = 1`), the whole disjunction loses index use and scans. That last rule is the review checklist: OR chains inherit their weakest disjunct ([[Why does a function on a column prevent index use]], [[How do you optimize a search query over several columns]]). The UNION ALL rewrite (one branch per disjunct) is the manual escape hatch when the planner refuses — with the dedup caveat handed to the caller.

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE INDEX idx_city ON customers(city);
CREATE INDEX idx_name ON customers(name);

EXPLAIN QUERY PLAN
SELECT * FROM customers WHERE city = 'Berlin' OR name = 'Alice';
-- QUERY PLAN
-- |--MULTI-INDEX OR
-- |  |--INDEX 1
-- |  |  `--SEARCH customers USING INDEX idx_city (city=?)
-- |  `--INDEX 2
-- |     `--SEARCH customers USING INDEX idx_name (name=?)
EXPLAIN QUERY PLAN
SELECT * FROM customers WHERE city = 'Berlin' OR city = 'Paris';
-- QUERY PLAN
-- `--SEARCH customers USING INDEX idx_city (city=?)
```

**Listing 1.** Verified on SQLite 3.53.1. Cross-column OR costs two index probes plus a merge; same-column OR rewrites to one index serving both values. PostgreSQL's bitmap OR produces the same shapes with different names.

```d2
direction: right
o: "a = 1 OR b = 2" {width: 160; height: 60}
m: "multi-index / bitmap OR
two probes, merged + deduped" {width: 260; height: 80}
s: "one disjunct non-sargable
whole OR scans" {width: 240; height: 80}
o -> m
o -> s
```

**Fig. 1.** The disjunction forks the plan: either every branch gets an index and the engine merges, or one branch drags the entire predicate set into a scan.

> [!warning] OR is only as indexable as its weakest disjunct
> `WHERE indexed_col = 1 OR expensive_function(other) = 2` scans — the planner cannot skip half the rows when half the condition is unseekable. Split the query (UNION ALL) or make both branches seekable; do not accept "OR is slow" as an axiom, it is per-branch ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> OR across columns means no single index can serve both disjuncts, so the engine either combines multiple indexes — SQLite plans MULTI-INDEX OR, PostgreSQL bitmap-ORs two index scans — or falls back to a scan. Same-column OR is cheap because it rewrites to IN on one index. The rules I apply: every disjunct must be sargable or the whole predicate loses index use, results need dedup when rows match both branches, and a UNION ALL rewrite is the manual fallback when the planner refuses.
