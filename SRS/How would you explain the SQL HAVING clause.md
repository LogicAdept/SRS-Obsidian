<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> `HAVING` filters **groups** after aggregation, the way `WHERE` filters rows before it. It exists because aggregates are computed after WHERE runs, so "groups with SUM over 100" cannot be expressed in WHERE. Its conditions may reference aggregates and grouping keys ([[What is the difference between SQL WHERE and HAVING clauses]]).

The mechanics follow the logical order: WHERE prunes rows, GROUP BY partitions survivors, aggregates compute per group, HAVING prunes whole groups, then SELECT projects. Any aggregate usable in the select list is usable in HAVING — including ones never displayed, which is a common readability trick (`HAVING COUNT(*) > 2` while selecting only the name). PostgreSQL's HAVING documentation notes two fine points worth repeating: HAVING can be used without GROUP BY at all, in which case the entire result set is treated as one group (useful for "does any row aggregate past a threshold" checks), and aggregate conditions in HAVING need not appear in the SELECT list. Performance-wise, conditions that do *not* involve aggregates belong in WHERE, not HAVING — pushing them down lets the engine scan fewer rows before grouping; PostgreSQL's planner pushes qualifying HAVING conditions down automatically, but SQLite's does not, and on SQLite the misplaced predicate measurably costs ([[How would you explain common ways to optimize SQL queries]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO customers VALUES (1,'Alice'),(2,'Boris'),(3,'Carla'),(4,'Dmitri'),(5,'Elena');
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5),(104,3,45.5),(105,3,300),
 (107,4,25),(108,3,25),(109,5,150),(110,5,150);

SELECT c.name, COUNT(*) AS orders, SUM(o.amount) AS total
FROM customers c JOIN orders o ON o.customer_id = c.id
GROUP BY c.name HAVING SUM(o.amount) > 100 ORDER BY total DESC;
-- Carla|3|370.5
-- Elena|2|300
-- Alice|2|200
```

**Listing 1.** Verified on SQLite 3.53.1. Nine orders group into five customers; HAVING keeps the three whose total exceeds 100 — Dmitri (25) and Boris (45.5) drop out with their groups, not their rows.

```d2
direction: right
w: "WHERE
filter rows" {width: 140; height: 70}
g: "GROUP BY
build groups" {width: 150; height: 70}
h: "HAVING
filter groups" {width: 140; height: 70}
s: "SELECT / ORDER BY" {width: 180; height: 70}
w -> g -> h -> s
```

**Fig. 1.** HAVING is the second gate of the pipeline: it cannot see individual rows (WHERE already consumed them), only groups and their aggregate values.

> [!warning] Non-aggregate conditions in HAVING are a portability and performance bug
> `HAVING city = 'Berlin'` is legal only when city is a grouping key, and even then the condition filters at group granularity — putting row-level predicates there defeats filter pushdown and reads misleadingly. Row conditions go in WHERE; only group-level (aggregate or grouping-key) conditions belong in HAVING ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> HAVING filters groups after aggregation: WHERE prunes rows, GROUP BY forms groups, aggregates compute, and HAVING removes whole groups whose aggregate conditions fail. It can reference aggregates not shown in the SELECT list and works even without GROUP BY, treating everything as one group. I keep row predicates in WHERE so they run before grouping, and reserve HAVING for aggregate conditions like SUM over a threshold or COUNT above N.
