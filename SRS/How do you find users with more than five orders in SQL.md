<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How do you find users with more than five orders in SQL?

> [!abstract] Short answer
> The canonical shape: `SELECT key, COUNT(*) FROM orders GROUP BY key HAVING COUNT(*) > 5`. GROUP BY collapses orders per customer; HAVING keeps only groups whose row count exceeds five. Add `WHERE customer_id IS NOT NULL` (exclude orphans), a JOIN for names, and ORDER BY for a ranked report — the task is a one-paragraph tour of the whole aggregate pipeline ([[What is the difference between SQL WHERE and HAVING clauses]]).

Interviewers use this task to check four decisions in one line each. First, grouping key: `customer_id` (the FK) or the joined `name` — grouping by id and projecting the name avoids merging two customers with equal names ([[What is the difference between GROUP BY and DISTINCT]]). Second, WHERE versus HAVING: rows with NULL customer or date-range limits go to WHERE (pre-grouping); the "more than five" condition is an aggregate, so it must be HAVING. Third, COUNT(*) versus COUNT(col): with no NULLs inside a grouped row the two agree here, but COUNT(*) is the correct intent — count orders, whatever their column values ([[What is the difference between COUNT star and COUNT of a column]]). Fourth, the count itself runs on the *filtered* set: WHERE amount > 100 changes which customers qualify — state which semantics you chose. The demo shows the literal > 5 form returning nothing on six-customer data, then the same query at threshold 2 proving the mechanics, then the joined form with names. On large tables the plan is a scan-plus-hash-aggregate or index-only count; the HAVING step costs nothing extra ([[How would you explain common ways to optimize SQL queries]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO customers VALUES (1,'Alice'),(2,'Boris'),(3,'Carla'),(4,'Dmitri'),(5,'Elena');
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5),(104,3,45.5),(105,3,300),
 (107,4,25),(108,3,25),(109,5,150),(110,5,150);

SELECT customer_id, COUNT(*) AS n FROM orders
WHERE customer_id IS NOT NULL GROUP BY customer_id HAVING COUNT(*) > 5;
-- (no customer has more than five orders in the demo data)
SELECT customer_id, COUNT(*) AS n FROM orders
WHERE customer_id IS NOT NULL GROUP BY customer_id HAVING COUNT(*) > 2;
-- 3|3
SELECT c.name, COUNT(*) AS n FROM customers c
JOIN orders o ON o.customer_id = c.id GROUP BY c.id HAVING COUNT(*) > 2;
-- Carla|3
```

**Listing 1.** Verified on SQLite 3.53.1. The literal form (over five) filters everyone out on the demo data; lowering the threshold to 2 exposes the machinery — Carla's three orders survive, and the joined variant attaches her name by grouping on the key, not the name.

```d2
direction: right
o: "orders
WHERE IS NOT NULL" {width: 190; height: 70}
g: "GROUP BY customer_id" {width: 200; height: 70}
h: "HAVING COUNT(*) > 5" {width: 200; height: 70}
r: "qualified customers" {width: 190; height: 70}
o -> g -> h -> r
```

**Fig. 1.** The task is the aggregate pipeline with one condition at each stage: row filter, group formation, group filter — no clause out of place.

> [!warning] "More than five" means strict inequality — and the WHERE changes the answer
> `HAVING COUNT(*) > 5` excludes exactly-five customers; `>= 5` includes them. And a WHERE like `amount > 100` silently changes *which* orders are counted. Restate the filter semantics in the answer; two candidates writing "the right shape" with different boundaries produce different reports ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> GROUP BY customer_id on orders, HAVING COUNT(*) over five — that is the core. I add WHERE customer_id IS NOT NULL before grouping, group by the key rather than the name so same-named customers stay separate, join to customers for display, and ORDER BY the count for a ranked report. I also spell out the semantics: strict inequality, and any WHERE predicate changes which orders the count sees. COUNT(*) is the right form since I am counting orders, not non-NULL column values.
