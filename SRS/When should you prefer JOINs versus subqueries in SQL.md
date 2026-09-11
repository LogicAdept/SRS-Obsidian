<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# When should you prefer JOINs versus subqueries in SQL?

> [!abstract] Short answer
> Prefer subqueries when the question is **membership, existence, or a scalar per row**; prefer JOINs when you actually need **columns from both sides** or want the optimizer to reorder freely for set-at-a-time filtering. They are frequently equivalent in results *and* plans — the differences that matter are NULL behavior in negation, row multiplication, and readability ([[What is the difference between IN EXISTS and JOIN in SQL]]).

Modern planners blur the old performance folklore: PostgreSQL's planner flattens IN-subqueries into semi-joins, so "IN is slow" stopped being generally true years ago; correlated scalar subqueries are the one shape that can still force per-row execution ([[What is a correlated subquery and why can it be slow]]). The durable decision factors are semantic. A join to the many side multiplies rows; a subquery never does. NOT IN has the NULL trap; NOT EXISTS does not. A subquery can compute an aggregate without GROUP BY leaking into the outer query; the join form needs pre-aggregation ([[How do you pre-aggregate before a join]]). Readability is a real criterion too — queries are read far more often than written — but "always use JOINs because faster" is 2005 advice that plans disprove on modern engines. The honest interview answer states the equivalence, then names the three divergences: NULL semantics, fan-out, and per-row execution of correlated scalars.

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO customers VALUES (1,'Alice','Berlin'),(2,'Boris','Oslo'),(3,'Carla','Berlin');
INSERT INTO orders VALUES (101,1,120),(102,3,300),(103,3,25);

SELECT name FROM customers
WHERE city = 'Berlin' AND id IN (SELECT customer_id FROM orders WHERE amount > 100)
ORDER BY name;
-- Alice
-- Carla
SELECT DISTINCT c.name FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE c.city = 'Berlin' AND o.amount > 100 ORDER BY c.name;
-- Alice
-- Carla
```

**Listing 1.** Verified on SQLite 3.53.1. Identical answers; the join version needed DISTINCT to undo the Carla duplication (two big orders) — the subquery never had the problem. Different shapes, same set, different failure modes.

```d2
direction: right
s: "subquery
membership / existence / scalar
no fan-out" {width: 240; height: 90}
j: "join
columns from both sides
fan-out managed explicitly" {width: 250; height: 90}
d: "decide by:
NULL semantics, grain, plan" {width: 240; height: 80}
s -> d
j -> d
```

**Fig. 1.** Two tools with overlapping cores: the subquery questions membership and per-row values; the join reassembles entities. The decision factors sit where their semantics differ.

> [!warning] Equivalence today does not mean equivalence under growth
> A query that is a fast IN-subquery at 10 thousand orders may need a different plan shape at 10 million; conversely, a join the planner reorders freely at small sizes may need index or statistics help later. Re-check plans when data volume or distribution changes instead of trusting a shape decided years ago ([[How do you systematically diagnose a slow SQL query]]).

> [!tip] Interview answer
> I pick by question, not by speed folklore: subqueries for membership, existence, and per-row scalars; joins when I need columns from both sides or want free plan reordering. On modern planners IN often compiles to the same semi-join as EXISTS, so the differences that remain are semantic — joins fan out on the many side, NOT IN breaks on NULLs, correlated scalar subqueries run per row. I write the clearer form, check the plan, and keep semantics like NULL behavior and row grain explicitly in mind.
