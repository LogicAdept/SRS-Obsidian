<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> `GROUP BY` collapses rows that share the same values in the grouped expressions into **one group per distinct combination**, then computes aggregate functions per group. Every selected column must be either a grouped expression or an aggregate — anything else has no single value for the group. `GROUP BY` runs after `WHERE` (row filter) and before `HAVING` (group filter) in the logical order ([[What is the logical order of SQL SELECT execution]]).

The clause is the standard's answer to "report per something": per city, per customer, per day. PostgreSQL's tutorial defines the semantics exactly this way — grouped rows are reduced, aggregates summarize each group, and non-aggregated select items must be listed in `GROUP BY`. Three practical rules follow. First, grouping keys are compared for equality, and under SQL's NULL semantics NULLs group together — one NULL group, not one group per NULL ([[How does GROUP BY handle NULL in SQL]]). Second, grouping happens *after* WHERE, so rows filtered out never form groups; the filter for "customers from Berlin" precedes the group "per customer" ([[What is the difference between SQL WHERE and HAVING clauses]]). Third, the grouped expression may be any expression — `GROUP BY date(created_at)` groups by day regardless of storage precision, and grouping by column *alias* is engine-dependent (SQLite allows it, the standard and PostgreSQL do not, ORDER BY always allows it). The demo aggregates orders per customer city: four groups from ten orders, one of them the NULL city.

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO customers VALUES (1,'Alice','Berlin'),(2,'Boris',NULL),(3,'Carla','Berlin'),
 (4,'Dmitri','Paris'),(5,'Elena','Tokyo');
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5),(104,3,45.5),(105,3,300),
 (107,4,25),(108,3,25),(109,5,150),(110,5,150);

SELECT c.city, COUNT(*) AS orders, SUM(o.amount) AS total
FROM customers c JOIN orders o ON o.customer_id = c.id
GROUP BY c.city ORDER BY total;
-- Paris|1|25
-- |1|45.5
-- Tokyo|2|300
-- Berlin|5|570.5
```

**Listing 1.** Verified on SQLite 3.53.1. Ten orders collapse into four groups keyed by city; Boris's order lands in the NULL-city group (displayed empty), proving NULLs form their own single group.

```d2
direction: right
r: "rows
10 orders" {width: 130; height: 70}
g: "GROUP BY city
4 groups" {width: 150; height: 70}
a: "aggregates per group
COUNT, SUM" {width: 190; height: 70}
r -> g -> a
```

**Fig. 1.** GROUP BY partitions the row set into key-equal groups; aggregates then reduce each group to one row, so the output has exactly as many rows as there are distinct keys.

> [!warning] Grouping changes the meaning of every column in the SELECT list
> After `GROUP BY city`, a bare `name` column is invalid in the standard (SQLite permits it and picks an arbitrary row's value — a portability trap). "Works on my engine" is not a spec; write every selected column as either a grouping expression or an aggregate ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> GROUP BY partitions rows into one group per distinct combination of the grouped expressions and reduces each group with aggregates, so output rows equal distinct keys. WHERE filters rows before grouping, HAVING filters groups after it, and every selected column must be a group key or an aggregate. NULLs form one group, and grouping may also happen on expressions like date(created_at) — which is why I never select bare non-key columns and rely on arbitrary engine behavior.
