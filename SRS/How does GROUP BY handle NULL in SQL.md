<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How does GROUP BY handle NULL in SQL?

> [!abstract] Short answer
> In `GROUP BY`, **all NULLs belong to one group**. Grouping uses distinctness semantics, not the `=` operator: two NULL values are "not distinct" from each other for grouping purposes, so they collapse into a single NULL-keyed group — exactly as two NULL rows collapse under `UNION` or `DISTINCT` ([[What does NULL mean in SQL]]).

This is specified, not incidental: the SQL standard defines grouping via the "not distinct" comparison, and PostgreSQL's SELECT documentation states that NULL values are grouped together for GROUP BY. The contrast with ordinary comparison is the point of the question: `WHERE city = NULL` matches nothing, but `GROUP BY city` still produces a NULL group. The same convention drives `DISTINCT` (one NULL row), `UNION` (one NULL row) and unique indexes (one NULL allowed in PostgreSQL, many in SQLite — a different NULL rule for a different operator) ([[What is the difference between PRIMARY KEY and UNIQUE]]). Aggregates interact predictably: COUNT(*) counts the NULL group's rows; COUNT(city) inside it returns zero because the column value is NULL; SUM over the group works because it sums the *other* columns' values. The verified demo shows the NULL group first (SQLite sorts NULLs before non-NULLs in ascending ORDER BY; PostgreSQL sorts them last by default — an ORDER BY portability nuance worth naming).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
INSERT INTO customers VALUES (1,'Alice','Berlin'),(2,'Boris',NULL),
 (3,'Carla','Berlin'),(4,'Dmitri','Paris'),(5,'Elena','Tokyo'),(6,'Fedor',NULL);

SELECT city, COUNT(*) FROM (SELECT NULL AS city UNION ALL SELECT NULL) GROUP BY city;
-- |2
SELECT city, COUNT(*) FROM customers GROUP BY city ORDER BY city;
-- |2
-- Berlin|2
-- Oslo|1
-- Paris|1
-- Tokyo|1
```

**Listing 1.** Verified on SQLite 3.53.1. Two synthetic NULL rows collapse into one group of 2; with six customers, Boris and Fedor (both NULL city) form a single group displayed as the empty key — not two separate groups.

```d2
direction: right
a: "city = Berlin
rows 1, 3" {width: 170; height: 70}
b: "city = NULL
rows 2, 6" {width: 170; height: 70}
c: "one NULL group
key displayed empty" {width: 210; height: 70}
a -> c
b -> c
```

**Fig. 1.** The NULL rows are not dropped and not split — they merge into a single group, because grouping treats NULLs as one key value.

> [!warning] One NULL group can hide a data problem under a legitimate-looking bucket
> Reports rendered with "N/A" for the NULL group make dirty data look like a designed category. Decide deliberately: label the group (`COALESCE(city, 'unknown')`), exclude it (`WHERE city IS NOT NULL`), or fix the data — never let the NULL bucket silently absorb rows ([[How do you GROUP BY value NULL]], [[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> GROUP BY puts all NULLs into one group, because grouping uses not-distinct semantics rather than the equals operator — the same rule that makes DISTINCT and UNION collapse NULL rows. So two customers with NULL city form one group, while WHERE city = something matches neither. COUNT(*) counts them, COUNT(city) does not. If the NULL bucket means something, I label it with COALESCE or filter it explicitly with IS NOT NULL rather than letting it look like a normal category.
