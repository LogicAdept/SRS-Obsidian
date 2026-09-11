<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How do you avoid a sort with an index?

> [!abstract] Short answer
> A sort disappears when an index already supplies the required order: build (or extend) an index whose key sequence equals the `ORDER BY` sequence — including direction and filter column. `WHERE category = ? ORDER BY price` wants the composite `(category, price)`: the equality pins the prefix, the index returns rows in price order, no sort node. SQLite plans the before/after difference as `USE TEMP B-TREE FOR ORDER BY` present versus absent ([[What is filesort or an external merge in a plan]]).

The composite design rule generalizes: equality predicates first, then the ORDER BY columns, then range predicates. `WHERE category = 'books' ORDER BY price` with `(category, price)` is a single seek whose output is pre-sorted — the verified demo shows the temp b-tree vanishing when the composite replaces the single-column index. PostgreSQL documents the same mechanism: an index scan can return rows in order, letting the planner drop the Sort node — and adds that the reverse direction works too by scanning the index backwards, so `ORDER BY price DESC` needs no separate descending index. The cases an index *cannot* save: mixed-direction sorts on a plain index (`ORDER BY a ASC, b DESC` needs a matching partial-descending index), expressions not matching the indexed ones, and sorts over computed values ([[Why does a function on a column prevent index use]]). Note the trade: every sort-avoiding index is a write-time cost and an index-maintenance liability — worth it for hot ordered reports, overkill for ad-hoc sorts ([[How would you explain the SQL ORDER BY clause]]).

```sql
CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT, category TEXT, price NUMERIC);
CREATE INDEX idx_cat2 ON products(category);
EXPLAIN QUERY PLAN
SELECT title FROM products WHERE category = 'books' ORDER BY price;
-- QUERY PLAN
-- |--SEARCH products USING INDEX idx_cat2 (category=?)
-- `--USE TEMP B-TREE FOR ORDER BY
DROP INDEX idx_cat2;
CREATE INDEX idx_cat_price ON products(category, price);
EXPLAIN QUERY PLAN
SELECT title FROM products WHERE category = 'books' ORDER BY price;
-- QUERY PLAN
-- `--SEARCH products USING INDEX idx_cat_price (category=?)
```

**Listing 1.** Verified on SQLite 3.53.1. Same query: the single-column index filters but still needs a sort; the composite `(category, price)` returns matching rows already in price order and the sort node is gone.

```d2
direction: right
f: "equality filter
category = ?
index prefix" {width: 190; height: 90}
o: "ORDER BY price
next index key
rows emerge sorted" {width: 200; height: 90}
n: "no sort node
streaming output" {width: 180; height: 80}
f -> o -> n
```

**Fig. 1.** The composite index encodes the query's shape — filter on the prefix, output in the tail's order — turning two plan stages into one seek.

> [!warning] The index must match the ORDER BY exactly — direction and columns included
> `(category, price)` does not serve `ORDER BY price` alone, and `ORDER BY price DESC` on an ascending index works only because engines scan backwards; a mixed `ORDER BY a, b DESC` needs the index built with matching per-column direction or it sorts anyway. Check the plan for the vanished sort node, not the presence of "an index" ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> I avoid sorts by making an index supply the order: equality-filter columns as the index prefix, ORDER BY columns as the tail — WHERE category equals x ORDER BY price wants (category, price). The plan proof is the disappearing sort node: SQLite's temp b-tree for ORDER BY, PostgreSQL's Sort node. DESC works by backward index scans, mixed-direction sorts need matching index directions, and I accept the write cost only for queries that run hot.
