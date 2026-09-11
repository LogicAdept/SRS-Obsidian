<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How does LEFT JOIN differ from INNER JOIN in SQL?

> [!abstract] Short answer
> `INNER JOIN` returns only rows with a match on **both** sides; `LEFT JOIN` returns **all** rows of the left table, and for rows with no match produces NULLs for every right-table column. So `INNER` can only shrink a result relative to the left table, while `LEFT` preserves its row multiplicity — that is the entire semantic difference.

The two are identical plans when every left row finds a match; they diverge exactly on orphans. This makes the choice a *business* decision, not a style one: "orders with customer names" (orphans impossible or irrelevant) wants INNER, "all customers with their optional orders" wants LEFT. Two mechanics matter in practice. First, with a LEFT JOIN, predicates on the right table belong in the `ON` clause — putting them into `WHERE` turns the LEFT JOIN back into an INNER JOIN whenever the predicate rejects NULL (PostgreSQL's table-expressions chapter describes exactly this pitfall) ([[How would you explain JOIN]]). Second, `WHERE right.id IS NULL` is the idiomatic *anti-join* idiom — a deliberate, legitimate use of the NULL padding ([[What is an anti-join in SQL]]). An inner join also stops the optimizer from reordering away the filter, whereas a LEFT JOIN with a WHERE constraint often plans identically to INNER — same plan, different row semantics.

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO customers VALUES (1,'Alice'),(2,'Boris'),(3,'Carla'),(4,'Fedor');
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5);

SELECT c.name, o.id AS order_id, o.amount FROM customers c
INNER JOIN orders o ON o.customer_id = c.id ORDER BY c.id, o.id;
-- Alice|101|120
-- Alice|102|80
-- Boris|103|45.5
-- (Carla, Fedor absent: no orders)
SELECT c.name, o.id AS order_id, o.amount FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id ORDER BY c.id, o.id;
-- Alice|101|120
-- Alice|102|80
-- Boris|103|45.5
-- Carla||
-- Fedor||
```

**Listing 1.** Verified on SQLite 3.53.1. Same data, same condition: INNER keeps 3 rows, LEFT keeps 4 — Carla and Fedor appear once with NULL order columns. The difference lives entirely at the orphans.

```d2
direction: right
c: "customers
A B C D" {width: 140; height: 80}
o: "orders
(o1 A) (o2 B)" {width: 150; height: 80}
i: "INNER
A-o1 A-o2 B-o3" {width: 170; height: 80}
l: "LEFT
A-o1 A-o2 B-o3
C-null D-null" {width: 190; height: 100}
c -> i
o -> i
c -> l
o -> l
```

**Fig. 1.** INNER is the intersection of the match relation; LEFT is the intersection plus every left row padded with NULLs when its match set is empty.

> [!warning] A WHERE predicate on the right table silently converts LEFT into INNER
> `LEFT JOIN o ... WHERE o.amount > 100` removes the NULL-padded rows (NULL > 100 is not true), so the LEFT JOIN degenerates into an INNER JOIN with extra syntax. Put right-side filters into the ON clause or accept that they filter; never assume LEFT "protected" the query ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> INNER JOIN returns only matched pairs; LEFT JOIN returns every left row and pads unmatched ones with NULLs on the right side. They are the same when everything matches and differ exactly at orphans — so the choice expresses whether unmatched rows must survive. I always mention the two classic traps: a WHERE predicate on the nullable right side turns LEFT back into INNER, and WHERE right.id IS NULL is the anti-join idiom that uses the padding deliberately.
