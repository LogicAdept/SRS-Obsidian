<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> Joins solve the problems normalization creates: **reassembling** facts split across tables (order + customer + items), **enrichment/lookup** (attach a name or category to a bare foreign key), **filtering by related data** (rows whose related rows satisfy a condition), and **aggregation across entities** (totals per customer computed from child rows). Any query touching more than one entity at SQL level is a join in disguise.

Each problem class maps to a join form. Reassembly is the plain inner join over foreign keys. Enrichment is a join to a small reference table (often a LEFT JOIN when the reference is optional). Filtering by related data is a semi-join — `EXISTS`, `IN`, or `JOIN` + `DISTINCT` — where the goal is row *membership*, not concatenation ([[What is a semi-join in SQL]]). Aggregation over children joins a parent to child rows and then groups, with the fan-out caveat: summing parent columns after a one-to-many join double-counts ([[Why can a JOIN multiply your row count]], [[How do you pre-aggregate before a join]]). The multi-table listing below is the canonical "reassemble an order" query: four tables, three joins, each `ON` a declared relationship — this is the shape of most production queries and the reason keys need indexes ([[What is the difference between Nested Loop Hash Join and Merge Join]]).

```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER);
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE order_items (order_id INTEGER, product_id INTEGER, qty INTEGER);
CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT);
INSERT INTO customers VALUES (1,'Alice');
INSERT INTO orders VALUES (101,1),(102,1);
INSERT INTO order_items VALUES (101,5,2),(101,1,1),(102,2,2);
INSERT INTO products VALUES (1,'SQL Pocket Guide'),(2,'USB Cable'),(5,'Notebook');

SELECT o.id AS order_id, c.name AS buyer, p.title AS product, oi.qty
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE o.id IN (101, 102) ORDER BY o.id, p.title;
-- 101|Alice|Notebook|2
-- 101|Alice|SQL Pocket Guide|1
-- 102|Alice|USB Cable|2
```

**Listing 1.** Verified on SQLite 3.53.1. Three joins reassemble one business fact — "who bought what and how many" — from four normalized tables; each row of the output is a path through the foreign-key graph.

```d2
direction: right
n: "normalized storage
4 tables, no copies" {shape: cylinder; width: 200; height: 90}
j: "joins ON declared
foreign keys" {width: 190; height: 80}
q: "reassembled facts
order, buyer, product, qty" {width: 240; height: 90}
n -> j -> q
```

**Fig. 1.** Normalization pushes redundancy out of storage; joins pull it back into query results on demand — the trade every relational schema makes.

> [!warning] The more joins, the more the row count is negotiable
> Every one-to-many join in a chain multiplies rows, so "SELECT plus a few aggregates" over a 4-table chain silently computes aggregates over the *multiplied* set unless intermediate tables are pre-aggregated or the fan-out is compensated. Decide per query what one output row means before choosing join forms ([[Why can a JOIN multiply your row count]]).

> [!tip] Interview answer
> Joins exist because normalized schemas split facts across tables. The four recurring problems: reassembly of an entity chain over foreign keys, enrichment of bare keys with names from reference tables, membership filtering which is really a semi-join, and aggregation across parent-child pairs — where I always watch for fan-out double counting. In practice that means most multi-entity queries are joins in one of those four shapes, and keys involved need indexes to stay fast.
