<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is the difference between SQL WHERE and HAVING clauses?

> [!abstract] Short answer
> `WHERE` filters **individual rows** before grouping; `HAVING` filters **groups** after aggregation. They run at different stages of the logical pipeline, so WHERE cannot see aggregates (the rows are not grouped yet) and HAVING should not re-filter plain row conditions ([[What is the logical order of SQL SELECT execution]]).

The boundary is observable, not stylistic: an aggregate in WHERE is a syntax error in every mainstream engine — SQLite says `misuse of aggregate: COUNT()` — because at WHERE time groups do not exist. The reverse direction is legal but wasteful: a plain column predicate in HAVING runs after grouping, so the engine has already grouped rows it will throw away (PostgreSQL pushes qualifying HAVING predicates down automatically; SQLite does not, so the discipline matters there). One subtlety interviewers like: after grouping by a column, a predicate *on that column* is semantically identical in both clauses — `GROUP BY city HAVING city = 'Berlin'` keeps the same groups as `WHERE city = 'Berlin'` — but only the WHERE form filters before the aggregation work. The verified demo shows both gates in one query: WHERE first restricts to orders above 50, then GROUP BY, then HAVING keeps cities with at least one surviving order ([[How would you explain the SQL GROUP BY clause]], [[How would you explain the SQL HAVING clause]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO customers VALUES (1,'Alice','Berlin'),(2,'Boris',NULL),(3,'Carla','Berlin'),
 (4,'Dmitri','Paris'),(5,'Elena','Tokyo');
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5),(104,3,45.5),(105,3,300),
 (107,4,25),(108,3,25),(109,5,150),(110,5,150);

SELECT city FROM customers
WHERE COUNT(*) > 1 GROUP BY city;
-- ERROR: misuse of aggregate: COUNT()
SELECT c.city, COUNT(*) AS n FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE o.amount > 50
GROUP BY c.city HAVING COUNT(*) >= 1 ORDER BY c.city;
-- Berlin|3
-- Tokyo|2
```

**Listing 1.** Verified on SQLite 3.53.1. The aggregate-in-WHERE form errors out (groups do not exist yet); the working query filters rows with WHERE (amount over 50), groups by city, then filters groups with HAVING — Paris (order 25) never reaches HAVING.

```d2
direction: right
r: "rows" {width: 90; height: 60}
w: "WHERE row predicate" {width: 190; height: 60}
g: "GROUP BY + aggregates" {width: 210; height: 60}
h: "HAVING group predicate" {width: 210; height: 60}
o: "result" {width: 90; height: 60}
r -> w -> g -> h -> o
```

**Fig. 1.** WHERE and HAVING are the same operation applied at two heights of the pipeline — rows before grouping, groups after — and the aggregate boundary sits between them.

> [!warning] Semantically-equal placement is not performance-equal
> Moving `city = 'Berlin'` from WHERE to HAVING (legal after grouping by city) changes nothing in the result but does all the grouping work before discarding groups. Engines differ in fixing this automatically; treat WHERE for row conditions, HAVING for aggregate conditions as a hard rule ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> WHERE filters rows before grouping, HAVING filters groups after aggregation — that is why COUNT in WHERE is a misuse-of-aggregate error. Both may legally reference a grouping key, but only WHERE runs before the aggregation work, so row-level conditions always go there. The pipeline order is WHERE, GROUP BY, aggregates, HAVING, SELECT, ORDER BY, and I use HAVING exclusively for conditions on aggregates like COUNT, SUM or AVG over a threshold.
