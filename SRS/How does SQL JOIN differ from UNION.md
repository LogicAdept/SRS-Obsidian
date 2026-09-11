<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How does SQL JOIN differ from UNION?

> [!abstract] Short answer
> `JOIN` and `UNION` solve opposite problems. `JOIN` combines **columns** — it extends rows horizontally by matching two tables pairwise. `UNION` combines **rows** — it stacks the outputs of two queries with the same column count vertically. They are not interchangeable: one changes the width of the result, the other its length.

The formal distinction comes straight from the standard's two mechanisms: joins work on table expressions in `FROM` and use a predicate per pair of rows; set operators work between full `SELECT` statements and compare results positionally, column by column. Practical corollaries interviewers probe: `UNION` (without ALL) deduplicates whole rows and therefore needs a sort or hash pass, while `JOIN` never deduplicates by itself — it can only *multiply* rows ([[What is the difference between SQL UNION and UNION ALL]], [[Why can a JOIN multiply your row count]]). Column names of a `UNION` come from the first query; a join exposes all columns of both sides, disambiguated by alias. When you see `UNION` used to "attach" related data of different shape, that is a modeling smell — the standard tool is a join, and when row counts from two sources must be *summed*, the tool is `UNION ALL` inside a subquery with an outer `SUM` ([[When should you use UNION ALL instead of UNION]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE departments (id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO customers VALUES (1,'Alice','Berlin'),(2,'Boris','Oslo');
INSERT INTO departments VALUES (1,'IT'),(2,'HR');
INSERT INTO orders VALUES (101,1,120);

SELECT c.name, o.amount FROM customers c
JOIN orders o ON o.customer_id = c.id ORDER BY o.id;
-- Alice|120
SELECT city AS label FROM customers WHERE city IS NOT NULL
UNION SELECT title FROM departments ORDER BY label;
-- Berlin
-- HR
-- IT
-- Oslo
```

**Listing 1.** Verified on SQLite 3.53.1. The join extends each order row with the customer name (width grows); the union stacks city names and department titles into one column (length grows, duplicates merged positionally).

```d2
direction: right
j: "JOIN
row x row -> wider row
A|B columns" {width: 220; height: 90}
u: "UNION
row over row -> taller result
same column list" {width: 220; height: 90}
t1: "table A" {width: 110; height: 60}
t2: "table B" {width: 110; height: 60}
t1 -> j
t2 -> j
t1 -> u
t2 -> u
```

**Fig. 1.** JOIN multiplies and widens (every matched pair becomes one row); UNION appends and narrows to the shared column list — horizontal composition versus vertical concatenation.

> [!warning] UNION is not a join with extra steps — it is a distinct
> `a UNION b` sorts or hashes the combined result to remove duplicates; on large inputs that is a plan node with memory and I/O cost, not free concatenation. If duplicates are impossible by construction or unwanted, `UNION ALL` avoids the pass entirely ([[What is the difference between SQL UNION and UNION ALL]]).

> [!tip] Interview answer
> JOIN combines horizontally: it matches rows pairwise and extends the result with columns from both tables. UNION combines vertically: it stacks the row outputs of two queries that must share column count and compatible types, taking names from the first. JOIN can multiply rows but never dedups; plain UNION dedups whole rows and pays a sort or hash for it, UNION ALL does not. So I pick JOIN when one row needs data of another entity, and UNION when one result column list must collect rows from several sources.
