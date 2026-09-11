<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# Why does a function on a column prevent index use?

> [!abstract] Short answer
> A B-tree index stores the column's *values*, so it can only seek values that exist as keys. `WHERE f(col) = x` asks for a computed value — absent from the index — so the plan degrades to a full scan. The fix is to index the expression itself: PostgreSQL supports expression indexes, SQLite indexes expressions since 3.9, SQL Server since 2008 via computed columns.

The demo shows both directions of the story on SQLite. Without an expression index, `WHERE substr(name, 1, 1) = 'A'` scans every customer row — the function output exists only per-row at runtime. After `CREATE INDEX idx_name_start ON customers(substr(name, 1, 1))`, the plan becomes `SEARCH customers USING INDEX idx_name_start (<expr>=?)`: the engine computed the expression for every row *once* at index build time, sorted the results, and can now seek them like any key. PostgreSQL documents expression indexes for exactly this purpose and adds the maintenance rule: the expression in the query must match the indexed expression textually (same functions, same arguments) for the planner to match them ([[What is sargability in SQL]]). The design decision behind the question: functions on columns in hot predicates are a schema smell — either the query should compare the stored form (normalize on write: store `email_lower`), or the expression deserves a materialized, indexed form. Both beats the runtime cost on every read ([[How do you implement case-insensitive search efficiently]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
INSERT INTO customers VALUES (1,'Alice','Berlin'),(2,'Boris',NULL),(3,'Carla','Berlin');

EXPLAIN QUERY PLAN SELECT * FROM customers WHERE substr(name, 1, 1) = 'A';
-- QUERY PLAN
-- `--SCAN customers
CREATE INDEX idx_name_start ON customers(substr(name, 1, 1));
EXPLAIN QUERY PLAN SELECT * FROM customers WHERE substr(name, 1, 1) = 'A';
-- QUERY PLAN
-- `--SEARCH customers USING INDEX idx_name_start (<expr>=?)
```

**Listing 1.** Verified on SQLite 3.53.1. Same query before and after the expression index: SCAN becomes SEARCH on the expression key — the computation moved from per-query runtime to index-build time, permanently.

```d2
direction: right
q: "WHERE substr(name,1,1) = 'A'" {width: 250; height: 70}
r1: "no expression index
evaluate per row" {width: 210; height: 80}
r2: "expression index
seek precomputed keys" {width: 220; height: 80}
q -> r1
q -> r2
```

**Fig. 1.** The function itself is never the problem — the problem is computing it at query time. Indexing the expression materializes the computation once and restores seeking.

> [!warning] The expression in the query must match the indexed expression exactly
> `CREATE INDEX ON t(upper(name))` does not serve `WHERE lower(name) = ?`, and argument changes (substr lengths, added casts) break the match silently — the plan just reverts to a scan. Copy the expression character-for-character, or better, normalize on write and index the plain column ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> A function on a column hides the index because the index stores column values, not computed results — WHERE UPPER(name) = ? cannot navigate a tree of raw names, so the plan scans and evaluates per row. My fixes in order: index the expression itself, which PostgreSQL and SQLite both support — the plan then seeks precomputed keys; use a generated column; or normalize on write so the query compares the stored form. And the query expression must match the indexed expression exactly, otherwise the planner will not use it.
