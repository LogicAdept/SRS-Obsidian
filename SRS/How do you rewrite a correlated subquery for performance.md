<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How do you rewrite a correlated subquery for performance?

> [!abstract] Short answer
> The two standard rewrites of a slow correlated subquery: (1) **aggregate first, join second** — compute per-group values in a derived table or CTE, then join the aggregate to the base rows; (2) **window functions** — `AVG(...) OVER (PARTITION BY ...)` computes the group value while scanning, no self-join at all. Both replace "N re-executions" with "one aggregation pass plus one join".

The rewrite preserves semantics when the correlation is a plain equality on the grouping column — the overwhelmingly common case ([[What is a correlated subquery and why can it be slow]]). The aggregate-first form is portable to every engine and is the one to reach for when the subquery computes `MAX`, `AVG`, `TOP-per-group` conditions. The window-function form is even leaner: one scan attaches the partition aggregate to every row, and the outer filter becomes a simple `WHERE` on the window result (in a wrapping query or QUALIFY where supported). SQLite's plan for the rewritten query shows the difference concretely: the `CORRELATED SCALAR SUBQUERY` node disappears, replaced by a co-routine for the aggregate plus an ordinary join — with a bloom filter the engine adds automatically ([[What is the difference between Nested Loop Hash Join and Merge Join]]). What *blocks* a rewrite: correlations that are inequalities, reference aggregates of different grains, or appear in `SELECT` per-row computations with side conditions — then keep the correlated form and index the correlation column instead.

```sql
CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary NUMERIC);
INSERT INTO employees VALUES (1,'Greta',1,5000),(2,'Hans',1,3500),(3,'Ivan',1,3500),
 (4,'Julia',2,4000),(5,'Kim',2,4000);

EXPLAIN QUERY PLAN
WITH d AS (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id)
SELECT e.name, e.salary FROM employees e JOIN d ON d.dept_id = e.dept_id
WHERE e.salary > d.avg_sal ORDER BY e.name;
-- QUERY PLAN
-- |--CO-ROUTINE d
-- |  |--SCAN employees
-- |  `--USE TEMP B-TREE FOR GROUP BY
-- |--SCAN e
-- |--BLOOM FILTER ON d (dept_id=?)
-- `--SEARCH d USING AUTOMATIC COVERING INDEX (dept_id=?)
WITH d AS (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id)
SELECT e.name, e.salary FROM employees e JOIN d ON d.dept_id = e.dept_id
WHERE e.salary > d.avg_sal ORDER BY e.name;
-- Greta|5000
```

**Listing 1.** Verified on SQLite 3.53.1. Same answer as the correlated form (Greta|5000), but the plan has no correlated subquery node: the CTE aggregates once, the join probes it — the bloom filter and automatic index are the engine's own optimizations on top ([[What is a query plan in a relational database]]).

```d2
direction: right
a: "correlated
N x inner query" {width: 180; height: 70}
b: "aggregate-first
1 x GROUP BY + join" {width: 200; height: 70}
c: "window function
1 x scan, OVER (PARTITION)" {width: 230; height: 70}
a -> b -> c
```

**Fig. 1.** Ladder of increasing hoisting: from per-row execution, to one aggregation feeding a join, to a single scan that carries the partition aggregate along.

> [!warning] The rewrite changes semantics if the correlation is not an equality on the grouping key
> `WHERE e.salary > (SELECT AVG(...) WHERE e2.city = e1.city AND e2.age > e1.age)` cannot become a GROUP BY join — the subquery depends on the *row*, not just its group. Aggressive rewrites of such queries return different rows, silently. Rewrite only what the correlation shape allows, and diff results between old and new queries on real data ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> My first rewrite is aggregate-then-join: compute the per-group value in a CTE or derived table and join on the group key — one GROUP BY plus one join instead of N subquery executions. The second is a window function, AVG or MAX OVER PARTITION BY the correlation column, filtered in an outer query — a single scan. Both are safe when the correlation is equality on the group key; unequal or row-dependent correlations keep the correlated form, and then I make sure the correlation column is indexed.
