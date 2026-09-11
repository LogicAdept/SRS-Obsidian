<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# When should you use a subquery JOIN or CTE in SQL?

> [!abstract] Short answer
> A **CTE** (`WITH name AS (...)`) is a named subquery in scope for one statement. Use a **subquery** for a single inline helper, a **CTE** when the helper is reused, recursive, or needs a name for readability, and a **JOIN** when combining rows of two existing row sources. They are composition tools, not competitors — most real queries nest all three.

Three CTE properties drive the choice. Readability: a long query decomposed into named steps ("active", "totals", "ranked") reads top-down, which is why teams standardize on CTEs for anything beyond two levels of nesting. Reuse: one CTE can be referenced several times in the statement, replacing copy-pasted derived tables. Recursion: only the `WITH RECURSIVE` form can walk hierarchies (org charts, BOM explosions) — no subquery or plain join can express "repeat until fixpoint" ([[How do you write SQL queries for classic practice tasks]]). One performance caveat is engine-specific and worth saying explicitly: historically PostgreSQL *materialized* CTEs, making them an optimization fence — the MATERIALIZED/NOT MATERIALIZED keywords (PG 12+) now control it explicitly, so a reused CTE on PG may legitimately be computed once deliberately ([[How would you explain MATERIALIZED VIEW]]). SQLite implements CTEs as co-routines or materializes them at its own discretion — visible in plans as `CO-ROUTINE` nodes, which is exactly what the demo shows.

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO customers VALUES (1,'Alice','Berlin'),(2,'Boris','Oslo'),(3,'Carla','Berlin');
INSERT INTO orders VALUES (101,1,120),(102,3,300),(103,3,25);

WITH active AS (
  SELECT DISTINCT customer_id FROM orders WHERE amount > 100)
SELECT c.name FROM customers c JOIN active a ON a.customer_id = c.id
WHERE c.city = 'Berlin' ORDER BY c.name;
-- Alice
-- Carla
EXPLAIN QUERY PLAN WITH active AS (
  SELECT DISTINCT customer_id FROM orders WHERE amount > 100)
SELECT c.name FROM customers c JOIN active a ON a.customer_id = c.id;
-- QUERY PLAN
-- |--CO-ROUTINE active
-- ...
```

**Listing 1.** Verified on SQLite 3.53.1. The CTE names one reusable concept ("customers with a big order"); the plan shows SQLite executing it as a co-routine pipelined into the join rather than a separate materialized step.

```d2
direction: right
sq: "subquery
inline, single use" {width: 200; height: 70}
ct: "CTE
named, reusable, recursive" {width: 230; height: 70}
jn: "join
combine rows of named sources" {width: 240; height: 70}
sq -> ct -> jn
```

**Fig. 1.** Escalation of composition tools: inline subquery for one-off logic, named CTE for reuse and recursion, joins to wire the named pieces together.

> [!warning] A CTE name is not a variable — it cannot be referenced outside its statement
> Unlike a temp table, a CTE exists only within the one statement that declares it, and each reference is re-planned (or materialized, engine-dependent). Need persistence or cross-statement reuse with indexes? That is a temporary table, not a bigger WITH clause ([[What is a temporary table in SQL and when is it used]]).

> [!tip] Interview answer
> Subquery, CTE and join are composition levels, not rivals. Inline subquery for one helper; CTE when I want a name, reuse within the statement, or recursion — WITH RECURSIVE is the only way to walk hierarchies in SQL. Joins then combine the named row sources. The nuance I add: CTEs may be materialized as an optimization fence — PG 12+ exposes MATERIALIZED and NOT MATERIALIZED to control it, and SQLite plans show co-routines — so a hot CTE is worth a plan check.
