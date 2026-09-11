<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> A **correlated subquery** references columns of the outer query, so it is logically re-evaluated for each outer row — "for this row, compute something from the related rows". It is the natural spelling of per-row questions (compare each employee to their department average), but a naive plan executes it N times, which is why the interview always attaches "and it can be slow" ([[How do you rewrite a correlated subquery for performance]]).

The cost model is the product of sizes: outer rows N times subquery cost per row. SQLite's query plan makes this visible — the plan lines literally contain `CORRELATED SCALAR SUBQUERY` with the outer scan nested above the inner scan, and for our five-employee demo the inner scan reports the same row count as the outer one, five executions of a five-row scan ([[What is the N plus 1 problem in SQL]]). Three escape routes exist. Rewrite to a **join against aggregates**: compute the per-group scalar once, then join — one pass over each side. Use **window functions**: `AVG(salary) OVER (PARTITION BY dept_id)` attaches the group value to every row in a single sort-and-scan. Or let the optimizer **decorrelate**: PostgreSQL's planner can turn scalar correlated subqueries into subplans or joins when semantics allow, though complex ones (non-equi correlations, side effects) block it. Correlation is not a defect — it is a *shape* whose cost depends on whether the engine can hoist the work out of the per-row loop.

```sql
CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary NUMERIC);
INSERT INTO employees VALUES (1,'Greta',1,5000),(2,'Hans',1,3500),(3,'Ivan',1,3500),
 (4,'Julia',2,4000),(5,'Kim',2,4000);

EXPLAIN QUERY PLAN
SELECT name, salary FROM employees e1
WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.dept_id = e1.dept_id);
-- QUERY PLAN
-- |--SCAN e1
-- `--CORRELATED SCALAR SUBQUERY 1
--    `--SCAN e2
SELECT name, salary FROM employees e1
WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.dept_id = e1.dept_id);
-- Greta|5000
SELECT dept_id, AVG(salary) FROM employees GROUP BY dept_id;
-- 1|4000.0
-- 2|4000.0
```

**Listing 1.** Verified on SQLite 3.53.1. The plan names the pattern — outer SCAN with a CORRELATED SCALAR SUBQUERY underneath; department averages 4000 and 4000 leave Greta (5000) the only employee above her department's mean.

```d2
direction: right
o: "outer scan
N rows" {width: 150; height: 70}
c: "correlated subquery
runs once per outer row" {width: 220; height: 80}
i: "inner scan
x N executions" {width: 160; height: 70}
o -> c -> i
```

**Fig. 1.** Correlation nests the inner scan inside the outer loop — the plan is a loop-invariant computation that failed to be hoisted.

> [!warning] An index on the correlation column decides whether "N times" is cheap
> With `e2.dept_id` indexed, each per-row execution is a few B-tree hops; without it, the subquery scans the whole inner table per outer row — quadratic total work that passes unit tests and dies in production. Check the plan for the inner SEARCH versus SCAN before blaming the correlation shape itself ([[How do you systematically diagnose a slow SQL query]]).

> [!tip] Interview answer
> A correlated subquery references the outer row, so it is logically evaluated once per outer row — the right shape for per-row questions like "compare to my department's average". It is slow when the plan really re-executes it N times over a large inner table; indexes on the correlation column make each execution cheap, and the rewrites are joining precomputed aggregates or a window function like AVG OVER PARTITION. I check the plan for the correlated-subquery node and try decorrelation when the inner side is big.
