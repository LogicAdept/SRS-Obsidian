<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What SQL clauses usually accompany aggregate queries?

> [!abstract] Short answer
> Aggregate queries are assembled from a standard clause set: `WHERE` (row filter, before grouping), `GROUP BY` (the keys), `HAVING` (group filter on aggregates), aggregate functions in the SELECT list, `ORDER BY` (may sort by aggregates), plus optional refinements — `DISTINCT` inside aggregates, `FILTER (WHERE ...)` for conditional aggregation, and grouping sets/`ROLLUP` where supported ([[What is the logical order of SQL SELECT execution]]).

A complete aggregate query uses most of these at once, and the *order* is fixed by the logical pipeline — which is why moving a condition between WHERE and HAVING changes what it is allowed to see ([[What is the difference between SQL WHERE and HAVING clauses]]). The refinements matter in interviews. `COUNT(DISTINCT x)` counts unique values — the natural "unique customers per city" metric; the demo shows per-customer distinct amount counts. `FILTER (WHERE ...)` (standard SQL, PostgreSQL, SQLite 3.30+) computes several conditional aggregates in one pass — `COUNT(*) FILTER (WHERE amount > 100)` — instead of `SUM(CASE WHEN ...)` emulation or separate scans; it is the modern spelling of pivot-style columns ([[How would you explain PIVOT and UNPIVOT in Transact-SQL]]). `ROLLUP`/`GROUPING SETS` add subtotal and grand-total rows in one statement (PostgreSQL, MySQL; SQLite lacks them). ORDER BY may reference aggregate results, but only by alias or by repeating the aggregate — another alias-visibility consequence of the logical order ([[What is the difference between GROUP BY and DISTINCT]]).

```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5),(104,3,45.5),(105,3,300),
 (106,NULL,60),(107,4,25),(108,3,25),(109,5,150),(110,5,150);

SELECT customer_id,
       COUNT(DISTINCT amount) AS distinct_amounts,
       COUNT(*) AS n
FROM orders WHERE customer_id IS NOT NULL
GROUP BY customer_id
HAVING COUNT(*) >= 2
ORDER BY distinct_amounts DESC, customer_id;
-- 3|3|3
-- 1|2|2
-- 5|1|2
SELECT COUNT(*) AS all_rows,
       COUNT(*) FILTER (WHERE amount > 100) AS big
FROM orders;
-- 10|4
```

**Listing 1.** Verified on SQLite 3.53.1. The full clause stack: WHERE excludes the orphan order, GROUP BY keys per customer, COUNT(DISTINCT) and COUNT(*) compute, HAVING keeps multi-order customers, ORDER BY sorts by an aggregate alias. FILTER computes both counts in one pass.

```d2
direction: right
w: "WHERE
rows in" {width: 130; height: 70}
g: "GROUP BY
keys" {width: 120; height: 70}
a: "aggregates
COUNT, SUM, DISTINCT-in-aggregate, FILTER" {width: 250; height: 80}
h: "HAVING
groups out" {width: 140; height: 70}
o: "ORDER BY
on aggregates" {width: 150; height: 70}
w -> g -> a -> h -> o
```

**Fig. 1.** The aggregate clause pipeline: filters before and after grouping bracket the aggregate computation, and sorting can consume its outputs.

> [!warning] FILTER and grouping sets are the modern answers; CASE-emulation is the portable one
> `SUM(CASE WHEN ... THEN 1 END)` reproduces conditional aggregates on engines without FILTER, but it is easy to get NULL/0 wrong in the ELSE branch. Know both spellings and the engine matrix: FILTER in PostgreSQL and SQLite 3.30+, ROLLUP in PostgreSQL and MySQL, neither in older engines ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> An aggregate query is WHERE to filter rows, GROUP BY for keys, aggregates in SELECT — with COUNT DISTINCT and FILTER as refinements — then HAVING to filter groups and ORDER BY, which can sort by an aggregate alias. FILTER computes conditional aggregates in one pass instead of CASE-emulation or extra scans, and ROLLUP or GROUPING SETS add subtotals where the engine supports them. The order is fixed by the logical pipeline, which is exactly why aggregates can appear in HAVING and ORDER BY but not WHERE.
