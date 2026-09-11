<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> The **logical processing order** (binding order) of a `SELECT` is: `FROM` → `ON` → `JOIN` → `WHERE` → `GROUP BY` → aggregates/`ROLLUP` → `HAVING` → `SELECT` → `DISTINCT` → `ORDER BY` → `LIMIT/TOP`. Each clause can only reference names and aliases produced by an earlier step. It is called *logical* because the engine is free to physically reorder work — but only when that cannot change the declared result ([[In SQL does the engine conceptually apply JOIN or WHERE filtering first]]).

The order explains the everyday rules of the language. Column aliases defined in the `SELECT` list (step 8) are invisible to `WHERE` (step 4) but visible to `ORDER BY` (step 10). Aggregate functions are computed at the `GROUP BY` stage, so they cannot appear in `WHERE` — only in `HAVING` (which runs after grouping) or in the select list ([[What is the difference between SQL WHERE and HAVING clauses]]). Joins bind before row filters, so `ON` can legitimately reference columns of both joined tables, while `WHERE` cannot see columns a `LEFT JOIN` did not keep. Microsoft's T-SQL reference publishes exactly this list and notes the caveat that in uncommon cases (for example certain indexed-view `CONVERT`s) the observed sequence can differ.

```sql
-- Step visibility, verified on SQLite 3.53.1.
CREATE TABLE sales (region TEXT, amount INTEGER);
INSERT INTO sales VALUES ('EU',100),('EU',250),('US',80);

-- ORDER BY (step 10) can use the SELECT alias (step 8):
SELECT region, amount * 10 AS amount10
FROM sales ORDER BY amount10;
-- EU|1000
-- EU|2500
-- US|800

-- WHERE (step 4) cannot see aggregates computed at GROUP BY (step 5):
SELECT region FROM sales WHERE SUM(amount) > 100 GROUP BY region;
-- ERROR: misuse of aggregate: SUM()
-- (filter groups with HAVING instead, which runs after GROUP BY)
```

**Listing 1.** Verified on SQLite 3.53.1. The alias works in `ORDER BY` and the aggregate fails in `WHERE` — two direct observations of binding order. PostgreSQL/SQL Server error on the same two statements with equivalent "column does not exist"/"aggregate not allowed in WHERE" messages.

```d2
direction: right
from: "1 FROM\n2 ON\n3 JOIN" {width: 130; height: 90}
where: "4 WHERE" {width: 110; height: 90}
group: "5 GROUP BY\n6 ROLLUP\n7 HAVING" {width: 140; height: 110}
select: "8 SELECT\n9 DISTINCT" {width: 130; height: 110}
tail: "10 ORDER BY\n11 LIMIT/TOP" {width: 140; height: 110}
from -> where -> group -> select -> tail
```

**Fig. 1.** Numbered binding order — a clause can only bind names that earlier steps have already produced; `SELECT` aliases therefore flow rightward only.

> [!warning] Logical order is not execution order — quoting it as physical is a red flag
> The optimizer may push filters below joins, evaluate projections early, or reorder scans; it is *required* only to return the result the logical order defines. Answering "the engine runs FROM first" without the word *logically* (or *conceptually*) loses the point of the question — physical plans are what `EXPLAIN` shows, and they re-shuffle steps constantly ([[How do you use EXPLAIN ANALYZE in SQL]]).

> [!tip] Interview answer
> Logically, a SELECT runs FROM, then ON/JOIN, then WHERE, then GROUP BY, then HAVING, then the SELECT list, then DISTINCT, ORDER BY, and LIMIT. That binding order is why SELECT aliases are visible to ORDER BY but not WHERE, and why aggregates go to HAVING. Physically the optimizer reorders freely — the order is a correctness contract for what the result must be, not the schedule the engine follows.
