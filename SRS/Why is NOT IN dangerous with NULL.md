<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# Why is NOT IN dangerous with NULL?

> [!abstract] Short answer
> `NOT IN` compares each outer value against the subquery result with ordinary equality. If the subquery returns even one NULL, every comparison yields UNKNOWN (neither true nor false), `NOT IN` rejects it, and the query returns **zero rows** — silently. `NOT EXISTS` avoids the trap because it tests for the absence of a *row*, not the comparison of a *value*.

The mechanism is the SQL standard's three-valued logic: `x NOT IN (a, b, NULL)` expands to `x <> a AND x <> b AND x <> NULL`, and `x <> NULL` is UNKNOWN, making the whole conjunction never true ([[What does NULL mean in SQL]]). SQLite's own documentation phrases the rule directly: if the right-hand side of IN contains any NULL, the NOT IN result is NULL overall. The consequences are asymmetrical and sneaky: `IN` with NULLs still returns correct positive matches; its negation returns nothing at all. Real-world trigger: a nullable foreign key (`orders.customer_id`) gains its first NULL row — every dashboard built on `NOT IN` goes blank at the same moment ([[What is an anti-join in SQL]]). Mitigations, in order of preference: rewrite to NOT EXISTS; filter the subquery with `WHERE col IS NOT NULL` (with a comment naming the trap); or enforce NOT NULL on the column so the class of bug cannot arise. The demo reproduces the empty result and both working alternatives on identical data.

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO customers VALUES (1,'Alice'),(2,'Boris'),(3,'Carla'),(4,'Dmitri'),(5,'Elena'),(6,'Fedor');
INSERT INTO orders VALUES (101,1),(102,1),(103,2),(104,3),(105,3),(106,NULL);

SELECT name FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders);
-- (0 rows: one NULL in customer_id poisons the whole NOT IN)
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id) ORDER BY c.id;
-- Fedor
SELECT name FROM customers WHERE id NOT IN
(SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);
-- Fedor
```

**Listing 1.** Verified on SQLite 3.53.1. Six customers, one order with a NULL `customer_id`: the NOT IN form returns nothing, NOT EXISTS and the filtered NOT IN both return Fedor — the only customer without orders.

```d2
direction: right
v: "x NOT IN (2, 5)" {width: 170; height: 60}
n: "x NOT IN (2, 5, NULL)" {width: 200; height: 60}
e: "x <> 2 AND x <> 5
AND x <> NULL" {width: 220; height: 60}
u: "UNKNOWN -> row dropped
entire result empty" {width: 250; height: 70}
v -> e
n -> e -> u
```

**Fig. 1.** One NULL in the list does not "add an unknown row" — it makes every row's predicate UNKNOWN, and the WHERE clause keeps nothing.

> [!warning] The bug is invisible: an empty result looks like valid business data
> No error, no warning, no log entry — just an empty report. That is why static analysis and code review ban `NOT IN (subquery)` outright rather than trusting authors to prove NULL-freedom, and why the column that feeds it should carry NOT NULL so the proof never expires ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> NOT IN with a NULL in the subquery returns an empty set, because x NOT IN expands to a conjunction of x not-equal comparisons and x not-equal NULL is UNKNOWN — three-valued logic. It fails silently, which is the worst part. I use NOT EXISTS, which checks row existence and is immune to NULLs, or I add an explicit IS NOT NULL filter with a comment. And I treat nullable columns feeding NOT IN as a schema smell worth fixing with a NOT NULL constraint.
