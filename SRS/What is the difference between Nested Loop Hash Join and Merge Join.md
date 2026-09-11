<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is the difference between Nested Loop Hash Join and Merge Join?

> [!abstract] Short answer
> Three physical join algorithms exist: **Nested Loop** probes the inner side per outer row (great when the probe is an index seek and the outer side is small); **Hash Join** builds an in-memory hash table of one side and probes it with rows of the other (great for large unsorted inputs with equality conditions); **Merge Join** walks two inputs sorted on the join key in lockstep (great for large sorted or presorted inputs, and the only one that feeds ordered output directly).

The database plans each query by choosing among them from available access paths, indexes, sizes and statistics. SQLite is a nested-loop engine at heart — its EXPLAIN QUERY PLAN output names only scan and search operations, and its optimizer's core job is picking the outer/inner order so each inner step is an index SEARCH instead of a SCAN ([[What is a query plan in a relational database]]). PostgreSQL implements all three and its EXPLAIN names them explicitly: `Nested Loop`, `Hash Join` with `Hash Cond`, `Merge Join` with `Merge Cond` — the textbook demonstration is a join whose plan flips from nested loop to hash join as the inner table grows past the cached-index point. The demo shows the nested-loop end of the spectrum on SQLite: outer scan of employees, inner SEARCH by primary key per row — 45 rows probed, one index seek each ([[How does a database query run]]). Hash joins need equality conditions; a range join (`BETWEEN`) forces nested loops or merge with predicates. Merge additionally preserves sort order, which lets the optimizer skip an explicit ORDER BY.

```sql
CREATE TABLE departments (id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
INSERT INTO departments VALUES (1,'IT'),(2,'HR');
INSERT INTO employees VALUES (1,'Greta',1),(2,'Hans',1),(3,'Julia',2);

EXPLAIN QUERY PLAN SELECT e.name, d.title FROM employees e
JOIN departments d ON d.id = e.dept_id;
-- QUERY PLAN
-- |--SCAN e
-- `--SEARCH d USING INTEGER PRIMARY KEY (rowid=?)
```

**Listing 1.** Verified on SQLite 3.53.1. A nested loop: scan employees once, and per employee SEARCH departments by primary key — the probe cost is one B-tree descent. PostgreSQL would print `Nested Loop` here and may switch to `Hash Join` once employees stops fitting the cached side.

```d2
direction: right
nl: "Nested Loop
per outer row: index probe
small outer, indexed inner" {width: 260; height: 90}
hj: "Hash Join
build hash of side A
probe with B
big unsorted, equality" {width: 230; height: 110}
mj: "Merge Join
both sides sorted on key
walk in lockstep
keeps order" {width: 230; height: 110}
nl -> hj -> mj
```

**Fig. 1.** The three algorithms trade memory, sort order and index availability: seek per row, hash probe, or ordered merge — the planner picks per query from statistics.

> [!warning] The algorithm is chosen per execution, not per query text
> The same SQL can plan as a nested loop today (small inner table, hot index) and a hash join tomorrow after a data load or statistics refresh. Performance conclusions drawn from one run's plan are stale the moment sizes change; re-read EXPLAIN when volumes shift ([[How do stale statistics hurt a query plan]]).

> [!tip] Interview answer
> Nested Loop probes the inner side once per outer row — unbeatable with an index seek and a small outer side. Hash Join builds a hash table of one side and streams the other through it — the default for large equality joins. Merge Join walks both sides in key order — wins when data is already sorted and preserves ordering for the outer query. SQLite essentially does nested loops with index searches; PostgreSQL picks among all three per plan. I read the chosen algorithm in EXPLAIN and treat plan flips after data growth as expected behavior.
