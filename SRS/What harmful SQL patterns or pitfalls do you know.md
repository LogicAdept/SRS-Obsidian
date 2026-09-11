<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What harmful SQL patterns or pitfalls do you know?

> [!abstract] Short answer
> The recurring harmful patterns: `SELECT *` (movement and coupling), non-sargable predicates (functions/conversions on columns), `NOT IN` against nullable subqueries (empty results via UNKNOWN), `LIKE '%x%'` on large tables (unseekable), fan-out joins summed incorrectly, unbounded queries without LIMIT, N+1 fetching from application code, implicit type conversions, and accidental cartesian products from comma-joins. Each is a *semantic or plan* failure with a one-line detection ([[What is sargability in SQL]], [[Why is NOT IN dangerous with NULL]], [[What is the N plus 1 problem in SQL]]).

Two of them verify in three lines. The unseekable LIKE: `WHERE customer_id LIKE '%3%'` plans as a bare `SCAN orders` — the leading wildcard leaves no range to seek, so every row is pattern-matched ([[Why does LIKE with a leading wildcard not use a B-tree index]]). The NOT IN trap: with one NULL in `orders.customer_id`, `id NOT IN (SELECT customer_id ...)` returns **zero rows** — every comparison UNKNOWN — which the demo shows as an empty result where one customer was expected ([[What does NULL mean in SQL]]). The others share a mechanism worth saying once: they either multiply work silently (fan-out joins feeding SUM; cartesian products from a forgotten join predicate) or move work that should be filtered (SELECT * defeating covering indexes; N+1 round trips). Detection is mostly plan-level and count-level: scan nodes on hot predicates, temp-b-tree sorts under LIMIT, row counts returned versus fetched, statements-per-request. Fixes are equally mechanical: bare-column predicates, explicit NOT EXISTS, covering projections, batching, and comma-join bans in review ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5),(104,3,45.5),
 (105,3,300),(106,NULL,60),(107,4,25),(108,3,25),(109,5,150),(110,5,150);

EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id LIKE '%3%';
-- QUERY PLAN
-- `--SCAN orders
SELECT name FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders);
-- (0 rows: the single NULL customer_id makes every row's predicate UNKNOWN)
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
-- Fedor
```

**Listing 1.** Verified on SQLite 3.53.1. The scan plan for the wildcard LIKE and the empty NOT IN result (with the NOT EXISTS correction returning Fedor) — two silent failure modes demonstrated on one dataset.

```d2
direction: right
p1: "silent wrong results
NOT IN + NULL, fan-out SUM" {width: 240; height: 80}
p2: "silent slowness
SELECT *, LIKE %x%, N+1" {width: 220; height: 80}
p3: "silent plan damage
non-sargable predicates" {width: 220; height: 80}
d: "detection: plans + counts,
not vibes" {width: 220; height: 80}
p1 -> d
p2 -> d
p3 -> d
```

**Fig. 1.** The patterns share one property — silence — which is why detection is built on plans and counts rather than on waiting for errors.

> [!warning] The dangerous patterns all pass tests on small clean data
> NOT IN is correct until one NULL arrives; fan-out SUM is correct until a second child row appears; SELECT * is cheap until the table widens. Tests cannot hold the line — review checklists and plan checks on production-shaped data are the actual defenses ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> The list I keep: SELECT *, non-sargable predicates, NOT IN against nullable subqueries — it silently returns nothing — leading-wildcard LIKEs, summing over fan-out joins, unbounded queries, N+1 fetching, implicit type conversions and comma-join cartesian products. What unites them is silence: they pass tests and fail on production-shaped data. I detect them with plans and counts — scan nodes, sorts under LIMIT, statements per request — and fix with sargable predicates, NOT EXISTS, covering projections and batching.
