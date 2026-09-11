<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is the difference between IN EXISTS and JOIN in SQL?

> [!abstract] Short answer
> All three answer "which left rows relate to some (or no) right rows" but differ in mechanics: `IN` is a set-membership test against a materialized list; `EXISTS` is a correlated existence check that stops at the first match; `JOIN` produces one row per match and needs `DISTINCT` to recover left multiplicity. For positive membership they are usually interchangeable; for negation only `NOT EXISTS` is NULL-safe ([[Why is NOT IN dangerous with NULL]]).

Semantics first, plans second. `IN (subquery)` evaluates membership against the subquery's result set; `EXISTS` evaluates the subquery as a correlated predicate per candidate row, and the optimizer may rewrite either into the other — PostgreSQL's planner transforms `IN` subqueries into semi-joins when profitable. The real fork is `JOIN`: it *concatenates*, so if a left row has five matches it appears five times; semi-join semantics need an explicit `DISTINCT` (or the optimizer recognizing a semi-join) ([[What is a semi-join in SQL]]). Decision rules that survive interviews: for "has at least one", EXISTS or IN — pick by plan, not by taste; for "no match", NOT EXISTS always; for "need columns from both sides", JOIN is not an alternative but a different question. NULL asymmetry completes the picture: `x IN (subquery)` returns rows even with NULLs present, its negation does not — the most quoted trap of this trio ([[What is an anti-join in SQL]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER);
INSERT INTO customers VALUES (1,'Alice'),(2,'Boris'),(3,'Carla');
INSERT INTO orders VALUES (101,1),(102,1),(103,3);

SELECT name FROM customers WHERE id IN (SELECT customer_id FROM orders) ORDER BY id;
-- Alice
-- Carla
SELECT c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id) ORDER BY c.id;
-- Alice
-- Carla
SELECT DISTINCT c.name FROM customers c
JOIN orders o ON o.customer_id = c.id ORDER BY c.name;
-- Alice
-- Carla
```

**Listing 1.** Verified on SQLite 3.53.1. Same two-name answer three ways: IN tests membership in the order list, EXISTS checks per customer for a first match, JOIN+DISTINCT produces the duplicated join output (Alice twice) and collapses it back.

```d2
direction: right
in: "IN
set membership
list materialized" {width: 190; height: 90}
ex: "EXISTS
correlated check
stops at first match" {width: 200; height: 90}
jn: "JOIN
row per match
DISTINCT to dedup" {width: 200; height: 90}
q: "same question:
which left rows have a match" {width: 240; height: 80}
in -> q
ex -> q
jn -> q
```

**Fig. 1.** Three spellings of one membership question, ranked by how directly they express it — and the JOIN spelling is the only one that changes the result shape, requiring DISTINCT to fold back.

> [!warning] The trio diverges the moment NOT appears or NULLs exist
> `NOT IN` with NULLs empties the result; `NOT EXISTS` does not. `IN` with NULLs still answers positively but its negation does not. And JOIN without DISTINCT inflates left multiplicity silently. Each of the three is safe in its intended corner and wrong in the others — decide by question shape first, verify by plan second ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> IN tests membership in a materialized set, EXISTS runs a correlated existence check that stops at the first hit, and JOIN emits one row per match so left multiplicity grows until DISTINCT folds it back. For "has a match" all three agree, and I choose by plan. For "has no match" only NOT EXISTS is NULL-safe, because NOT IN returns an empty result if the subquery yields one NULL. And if I need columns from the right side, that is not membership anymore — that is a plain join question.
