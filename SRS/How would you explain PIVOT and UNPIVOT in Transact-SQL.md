<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How would you explain PIVOT and UNPIVOT in Transact-SQL?

> [!abstract] Short answer
> **PIVOT** rotates rows into columns: distinct values of a pivot column (months) become column headers, with an aggregate per cell (`SUM(amt)`). **UNPIVOT** is the inverse — columns back into (key, value) rows. T-SQL has the keywords `PIVOT`/`UNPIVOT`; everywhere else the operations are spelled with conditional aggregation (`SUM(CASE WHEN ... END)`) and `UNION ALL` — which is also the standard comparison point, since CASE-pivoting is portable to every engine ([[What are the main SQL aggregate functions]]).

The verified demo performs both rotations on SQLite with the portable spellings. PIVOT: per department, `SUM(CASE WHEN month = 1 THEN amt END)` per month-column — the CASE returns NULL for non-matching rows, SUM ignores NULLs, and each cell becomes the month total (HR: 80, 90, 70; IT: 100, 150, 120). UNPIVOT: the wide `sales_w` table is melted back with three `UNION ALL` branches, each mapping a column pair to a (month, amt) row — the shape T-SQL's `UNPIVOT` produces from its column list. Microsoft's T-SQL reference documents the keyword forms: `SELECT ... FROM source PIVOT (agg() FOR pivot_col IN ([v1], [v2])) AS p` — with two caveats interviewers probe: the `IN` list must be *literal* column names (no subquery — the pivot's output schema is fixed at parse time), and PIVOT implicitly **drops** rows with NULL in the pivot column unless handled explicitly. The design judgment behind the keyword: wide pivot output is a *reporting* shape (spreadsheets, matrices) and belongs at the presentation edge — the canonical answer notes that storage stays long-form (3NF-friendly) and pivots happen in the report layer, where CASE-pivoting in a view or the BI tool usually beats engine-specific keywords ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE sales_m (dept TEXT, month INTEGER, amt NUMERIC);
INSERT INTO sales_m VALUES ('IT',1,100),('IT',2,150),('IT',3,120),
 ('HR',1,80),('HR',2,90),('HR',3,70);

SELECT dept,
  SUM(CASE WHEN month = 1 THEN amt END) AS m1,
  SUM(CASE WHEN month = 2 THEN amt END) AS m2,
  SUM(CASE WHEN month = 3 THEN amt END) AS m3
FROM sales_m GROUP BY dept ORDER BY dept;
-- HR|80|90|70
-- IT|100|150|120
-- (rows -> columns; T-SQL: FROM sales_m PIVOT (SUM(amt) FOR month IN ([1],[2],[3])) p)
SELECT dept, 1 AS month, m1 AS amt FROM sales_w
UNION ALL SELECT dept, 2, m2 FROM sales_w
UNION ALL SELECT dept, 3, m3 FROM sales_w
ORDER BY dept, month;
-- HR|1|80
-- HR|2|90
-- ...
-- IT|3|120
-- (columns -> rows; T-SQL spells this UNPIVOT)
```

**Listing 1.** Verified on SQLite 3.53.1. Both rotations in portable SQL — conditional aggregation for the pivot, UNION ALL for the unpivot — with the T-SQL keyword forms documented as their engine-specific spellings.

```d2
direction: right
l: "long form
rows: dept, month, amt" {width: 190; height: 80}
p: "PIVOT
columns per month" {width: 170; height: 80}
w: "wide form
cols: m1 m2 m3" {width: 170; height: 80}
u: "UNPIVOT
back to rows" {width: 160; height: 80}
l -> p -> w -> u -> l
```

**Fig. 1.** PIVOT and UNPIVOT are the two directions of one rotation between storage shape (long) and presentation shape (wide) — the cycle closing back where it started.

> [!warning] PIVOT needs a literal value list — the output schema is fixed at parse time
> `FOR month IN ([1],[2],[3])` names real output columns; a subquery is not allowed, so new months require new SQL or dynamic SQL generation (the SQL Server dynamic-pivot folklore). If the pivot set grows unboundedly, long-form storage with an app-side rotation usually wins ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> PIVOT rotates rows into columns — each distinct pivot value becomes a column with an aggregate per cell — and UNPIVOT melts columns back into rows. T-SQL has the keywords with the caveat that the IN list must be literal, and rows with NULL pivot values are dropped implicitly; everywhere else I write the portable spellings — SUM(CASE WHEN ...) for pivoting and UNION ALL branches for unpivoting — which my demo verifies end to end. The design point I add: storage stays long-form, pivots live in views or the reporting layer, and dynamic pivot sets usually belong to the BI tool, not to generated SQL.
