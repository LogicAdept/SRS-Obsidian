<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How would you explain the full syntax of a SQL SELECT statement?

> [!abstract] Short answer
> The full `SELECT` syntax is the ordered stack of optional clauses: `[WITH ...] SELECT [DISTINCT|ALL] select_list [INTO ...] FROM sources [JOIN ... ON ...] [WHERE ...] [GROUP BY ...] [HAVING ...] [WINDOW ...] [ORDER BY ...] [LIMIT/OFFSET | FETCH FIRST] [FOR UPDATE]`. Only the `SELECT` list is mandatory in the standard; every other clause is additive, and each appears in a fixed position.

Each clause plays one role. `WITH` defines CTEs — named subqueries readable in the main query ([[When should you use a subquery JOIN or CTE in SQL]]). `DISTINCT` collapses duplicate output rows (after projection). `FROM` names tables/views and may join them; `WHERE` filters individual rows before grouping. `GROUP BY` partitions rows into groups, aggregates (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) collapse each group, and `HAVING` filters *groups* ([[What are the main SQL aggregate functions]]). `ORDER BY` sorts the final rows; `LIMIT`/`OFFSET` (PostgreSQL/SQLite/MySQL) or `FETCH FIRST`/`OFFSET` (standard, Oracle 12c+) or `TOP` (T-SQL) page them. `FOR UPDATE` locks selected rows for a following write in the same transaction ([[What are SQL transaction isolation levels]]).

Set operations (`UNION`, `INTERSECT`, `EXCEPT`) combine two full selects and take `ORDER BY` only after the last operand ([[How would you explain the SQL UNION operator]]). A useful reading of the stack: *the engine applies the clauses in pipeline order, so a clause can only see what earlier clauses produced* — that is the same order you would use when hand-evaluating a query ([[What is the logical order of SQL SELECT execution]]).

```sql
-- Every major clause in one query (SQLite dialect; notes show portability).
WITH top_regions AS (                 -- CTE
  SELECT region FROM customers GROUP BY region HAVING COUNT(*) > 1
)
SELECT c.region, COUNT(*) AS orders, SUM(o.amount) AS total
FROM orders o
JOIN customers c ON c.id = o.customer  -- INNER JOIN
WHERE o.amount > 50                    -- row filter (before grouping)
GROUP BY c.region                      -- group
HAVING SUM(o.amount) > 100             -- group filter (after aggregation)
ORDER BY total DESC                    -- sort final rows
LIMIT 5;                               -- LIMIT/OFFSET; ANSI: FETCH FIRST 5 ROWS ONLY
-- EU|3|430
-- US|1|300
```

**Listing 1.** Verified on SQLite 3.53.1 (tables pre-filled with 3 customers and 4 orders; region totals after filtering and grouping). The statement exercises WITH, JOIN, WHERE, GROUP BY, HAVING, ORDER BY, and LIMIT in one shape.

```d2
direction: right
with: "WITH\nCTEs" {width: 110; height: 80}
from: "FROM\nJOIN" {width: 110; height: 80}
where: "WHERE" {width: 100; height: 80}
group: "GROUP BY\nHAVING" {width: 130; height: 80}
sel: "SELECT\nDISTINCT" {width: 130; height: 80}
order: "ORDER BY\nLIMIT" {width: 130; height: 80}
with -> from -> where -> group -> sel -> order
```

**Fig. 1.** Mandatory parts (SELECT list) drawn from the optional stack — clauses bind left to right, so each stage consumes the previous stage's output.

> [!warning] Portability lives in the corners of the stack, not in the core
> The order of clauses is fixed, but their spelling is not: row limiting has three dialect families (`LIMIT`, `TOP`, `FETCH FIRST`), `NULLS FIRST/LAST` support differs, and PostgreSQL allows `GROUP BY` position numbers while standard SQL does not. Queries that run "everywhere" stick to the intersection and test the corners ([[How does LIMIT interact with ORDER BY and indexes]]).

> [!tip] Interview answer
> A full SELECT is WITH for CTEs, then SELECT [DISTINCT] over FROM with JOINs, filtered by WHERE, grouped by GROUP BY with HAVING on aggregates, projected by the select list, sorted by ORDER BY, and paged by LIMIT/OFFSET or FETCH FIRST, optionally FOR UPDATE. Only the select list is required. Because the engine runs the clauses as a pipeline in that order, each clause can only reference what earlier stages produced.
