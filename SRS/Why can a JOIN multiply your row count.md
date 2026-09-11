<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> A join against the *many* side of a one-to-many relationship outputs **one row per match**, not one row per left row: a customer with 3 orders becomes 3 rows. Any aggregate computed over that result counts each parent row N times — the classic "totals are too big after joining" bug. The fix is to aggregate children first (pre-aggregation) or to aggregate parent columns before the join.

The multiplication is arithmetic, not a bug in the engine: the join relation is a set of pairs, and `SUM` over it sums every pair's payload. The PostgreSQL tutorial's join examples produce exactly such enlarged intermediate sets. Three concrete consequences are worth naming in an interview. First, `COUNT(*)` after a many-side join counts children, not parents. Second, joining *two* independent many-side tables (orders and invoices of one customer) multiplies twice — the row count becomes orders times invoices per customer, and totals inflate by that factor ([[How do you pre-aggregate before a join]]). Third, a `DISTINCT` "fix" hides the symptom while still computing the inflated set, so it is a correctness patch, not a performance one ([[Why is SELECT DISTINCT expensive]]). The reliable discipline: decide what one output row means; if it is a parent, aggregate each child stream to the parent grain before joining.

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
CREATE TABLE order_items (order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO customers VALUES (1,'Alice'),(2,'Boris'),(3,'Carla'),(4,'Dmitri'),(5,'Elena'),(6,'Fedor');
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5),(104,3,45.5),
 (105,3,300),(107,4,25),(108,3,25),(109,5,150),(110,5,150);

SELECT (SELECT COUNT(*) FROM customers) AS c,
       (SELECT COUNT(*) FROM orders) AS o,
       COUNT(*) AS joined
FROM customers c JOIN orders o ON o.customer_id = c.id;
-- 6|9|9
SELECT c.name, COUNT(*) AS orders FROM customers c
JOIN orders o ON o.customer_id = c.id GROUP BY c.name ORDER BY c.name;
-- Alice|2
-- Boris|1
-- Carla|3
-- Dmitri|1
-- Elena|2
```

**Listing 1.** Verified on SQLite 3.53.1. Six customers and nine orders become nine joined rows — Alice appears twice, Carla three times. `COUNT(*)` over the join counts orders; only grouping or pre-aggregation can count customers.

```d2
direction: right
p: "parent grain
1 customer row" {width: 170; height: 70}
m: "many-side join
N matched rows" {width: 170; height: 70}
s: "SUM/COUNT over join
counts the N copies" {width: 210; height: 70}
p -> m -> s
```

**Fig. 1.** A parent row is copied once per match into the join output; every aggregate downstream sees the copies, which is why child-driven joins inflate totals.

> [!warning] Two many-side joins in one query multiply twice
> `customers JOIN orders JOIN invoices` outputs orders times invoices per customer: a customer with 3 orders and 4 invoices contributes 12 rows, and any SUM over parent amounts is inflated 12-fold. Split such queries: aggregate each child stream to the shared parent key first, then join the aggregates ([[How do you pre-aggregate before a join]], [[What is a correlated subquery and why can it be slow]]).

> [!tip] Interview answer
> A join to the many side copies each parent row once per match, so the result has one row per matched pair — COUNT counts children and SUM repeats parent values. Two many-side joins multiply even worse, orders times invoices. I handle it by fixing the output grain first: if the row means "one customer", I aggregate each child stream to customer key before joining, or group immediately after the join and never sum parent columns over the multiplied set.
