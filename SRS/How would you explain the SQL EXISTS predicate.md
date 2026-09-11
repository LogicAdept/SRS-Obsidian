<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> `EXISTS (subquery)` is a boolean predicate that is true when the subquery returns **at least one row** — the engine stops scanning at the first match and ignores what the subquery selects. `NOT EXISTS` is its negation and the NULL-safe way to spell an anti-join ([[What is an anti-join in SQL]]).

EXISTS is the canonical *correlated* subquery: it usually references the outer row (`WHERE o.customer_id = c.id`), so its meaning is per-row — "does a partner exist for *this* row?" This per-row framing is why it never duplicates outer rows and never concatenates columns: it only votes. Two mechanical facts give it its reputation. First, short-circuit: the engine can stop on the first found row, so cost per outer row is "cost to find one match", not "cost to find all matches". Second, NULL-immunity: the subquery's *values* are never compared, only its row count — `NOT EXISTS` therefore has no `NOT IN`-style empty-result trap ([[What is the difference between IN EXISTS and JOIN in SQL]]). By convention the inner SELECT list is `SELECT 1` or `SELECT *` — both semantically identical, and reviewers prefer `1` because it documents that the projection is irrelevant. Optimizers frequently transform EXISTS into the same semi-join plan they would give `IN`, so "EXISTS is always faster" is folklore; verify with plans on your data volumes.

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO customers VALUES (1,'Alice'),(2,'Boris'),(3,'Carla');
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,3,300);

SELECT c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id) ORDER BY c.id;
-- Alice
-- Carla
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id
                  AND o.amount > 100) ORDER BY c.id;
-- Boris
-- Carla
```

**Listing 1.** Verified on SQLite 3.53.1. The first query asks "has any order" (Boris drops out); the second asks "has no order above 100" — Carla qualifies despite having orders, showing that the condition is part of the correlation, evaluated per outer row.

```d2
direction: right
o: "outer row c1" {width: 130; height: 60}
e: "EXISTS subquery
find first matching order" {width: 230; height: 70}
b: "true -> keep row
false -> drop row" {width: 190; height: 60}
s: "stop at first match
(columns ignored)" {width: 210; height: 70}
o -> e -> b
e -> s
```

**Fig. 1.** EXISTS is a per-row boolean gate: the subquery runs just until it can answer true or false, and its selected values never affect the result.

> [!warning] SELECT 1 versus SELECT * is style, but correlation is not optional decoration
> An EXISTS whose inner query references no outer column is uncorrelated — it either passes every row or none, which is almost always a bug rather than intent. If the optimizer cannot prove the subquery is constant, plans degrade to re-execution; either way the query's meaning silently changed ([[What is a correlated subquery and why can it be slow]]).

> [!tip] Interview answer
> EXISTS evaluates to true if the subquery returns any row, and the engine stops at the first match, ignoring the select list — that is why the convention is SELECT 1. It is inherently a semi-join: no duplication, no column concatenation, and NOT EXISTS is the NULL-safe anti-join, unlike NOT IN which an empty-set trap with NULLs. Usually the subquery is correlated and asks the question per outer row; uncorrelated EXISTS is a red flag meaning constant true or false.
