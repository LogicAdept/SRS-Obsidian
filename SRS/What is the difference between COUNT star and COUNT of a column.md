<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is the difference between COUNT star and COUNT of a column?

> [!abstract] Short answer
> `COUNT(*)` counts **rows**; `COUNT(col)` counts rows where `col` is **not NULL**; `COUNT(DISTINCT col)` counts distinct non-NULL values. Semantically they answer different questions ("how many orders" versus "how many orders have a city"); performance-wise COUNT(*) is the cheapest row-count and the one engines optimize specially ([[What are the main SQL aggregate functions]]).

The NULL rule is the whole answer's core: COUNT's argument is evaluated per row, NULL results are dropped, and only the asterisk form bypasses evaluation and counts rows. Verified numbers: six customers, one with NULL city — `COUNT(*)` 6, `COUNT(city)` 5. The standard's `COUNT(*)` has no column to evaluate, which is also why engines implement fast paths: PostgreSQL scans the smallest index (index-only scan) and still counts every row — it cannot shortcut via table metadata because of MVCC visibility; SQLite likewise scans a covering index, the smallest one available after ANALYZE. Applications that "count rows" but accidentally write `COUNT(col)` under-report silently — the classic production bug this card exists for ([[What does NULL mean in SQL]]). Related count-family facts worth one sentence each: `SUM(1)` over a table equals COUNT but is not special-cased; `EXISTS` beats `COUNT(*) > 0` for "any rows?" because it stops at the first row ([[What is the difference between IN EXISTS and JOIN in SQL]]); and `COUNT(1)` is identical to `COUNT(*)` by definition — the old "COUNT(1) is faster" claim is folklore.

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
INSERT INTO customers VALUES (1,'Alice','Berlin'),(2,'Boris',NULL),
 (3,'Carla','Berlin'),(4,'Dmitri','Paris'),(5,'Elena','Tokyo'),(6,'Fedor',NULL);

SELECT COUNT(*) AS all_rows, COUNT(city) AS with_city FROM customers;
-- 6|5
```

**Listing 1.** Verified on SQLite 3.53.1. Same table, same instant: six rows, five non-NULL cities — Boris and Fedor drop out of COUNT(city) but not from COUNT(*).

```d2
direction: right
t: "6 rows
1 with NULL city" {width: 170; height: 80}
cs: "COUNT(*)
counts rows
6" {width: 130; height: 90}
cc: "COUNT(city)
counts non-NULL
5" {width: 130; height: 90}
t -> cs
t -> cc
```

**Fig. 1.** The asterisk counts the row itself; the column form first evaluates the column and discards NULLs — a one-token difference that changes the denominator.

> [!warning] COUNT(col) under-counts silently when the column becomes nullable
> A column that was NOT NULL at query-writing time and gains NULLs after a schema change turns every COUNT(col)-based KPI into a quietly shrinking number. For "number of rows" always write COUNT(*); reserve COUNT(col) for genuinely conditional counts ([[What harmful SQL patterns or pitfalls do you know]], [[How do you optimize COUNT star on a large table]]).

> [!tip] Interview answer
> COUNT(*) counts rows, COUNT(col) counts rows where the column is not NULL, and COUNT(DISTINCT col) counts unique non-NULL values — the entire difference is NULL handling. COUNT(*) is also the form engines optimize with covering-index scans, though MVCC engines still walk everything and cannot use metadata shortcuts. For existence checks I use EXISTS rather than COUNT > 0, since it stops at the first row, and I never write COUNT(col) to count rows, because a nullable column silently under-reports.
