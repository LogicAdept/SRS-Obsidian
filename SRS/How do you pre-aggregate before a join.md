<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> **Pre-aggregation** means pushing `GROUP BY` before the join: aggregate each child stream to the parent's key first, then join the small aggregates. It fixes fan-out inflation (`SUM` over a multiplied parent column), removes duplicate parent rows from memory, and often lets the engine hash-join two compact inputs instead of streaming a huge multiplied one.

The problem it solves is grain: joining orders to items produces one row per item, and any parent-level SUM now counts order 110's 150 as many times as it has items. The listing makes the arithmetic concrete — `SUM(o.amount)` per order after joining items yields 240 for order 101 (120 times two items) and 300 for order 110, while the pre-aggregated form returns the true item totals next to the unmultiplied order amounts ([[Why can a JOIN multiply your row count]]). The same technique is the standard fix for multi-fact joins: when orders and invoices both hang off customers, aggregate each child to `customer_id` first — otherwise rows multiply by orders times invoices ([[How would you explain common ways to optimize SQL queries]]). Performance-wise the win is not only correctness: the join inputs shrink from "parent times children" to "parent plus one-row-per-group", which is exactly the shape hash joins like, and covering indexes on the grouping column turn each aggregation into an index-only pass ([[What is the difference between Nested Loop Hash Join and Merge Join]]).

```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
CREATE TABLE order_items (order_id INTEGER, product_id INTEGER, qty INTEGER, price NUMERIC);
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5),
 (105,3,300),(106,NULL,60),(110,5,150);
INSERT INTO order_items VALUES (101,5,2,5.0),(101,1,1,30.0),(102,2,2,10.0),
 (103,5,1,5.0),(105,3,1,250.0),(106,2,1,10.0),(110,1,1,30.0),(110,2,2,10.0);

SELECT o.id, SUM(o.amount) AS inflated
FROM orders o JOIN order_items oi ON oi.order_id = o.id
GROUP BY o.id ORDER BY o.id;
-- 101|240
-- 102|80
-- 103|45.5
-- 105|300
-- 106|60
-- 110|300
SELECT o.id, o.amount, COALESCE(agg.items_total, 0) AS items_total
FROM orders o LEFT JOIN
(SELECT order_id, SUM(price * qty) AS items_total FROM order_items GROUP BY order_id) agg
ON agg.order_id = o.id ORDER BY o.id;
-- 101|120|40
-- 102|80|20
-- 103|45.5|5
-- 105|300|250
-- 106|60|10
-- 110|150|50
```

**Listing 1.** Verified on SQLite 3.53.1. The joined SUM reports 240 and 300 for orders 101 and 110 — each amount repeated once per item. The pre-aggregated form keeps `o.amount` at its true value and computes item totals once per order.

```d2
direction: right
raw: "join raw children
parent row x N" {width: 200; height: 70}
agg: "pre-aggregate
one row per group" {width: 200; height: 70}
j: "join compact aggregates
1:1 with parent" {width: 220; height: 70}
raw -> agg -> j
```

**Fig. 1.** Aggregate the many side down to the join key first; the join then happens at parent grain, where SUM and COUNT mean what they say.

> [!warning] Pre-aggregate every many-side stream, or the last one multiplies the rest
> With two child tables aggregated and one raw, the raw stream still fans the joined result out. The discipline is: reduce each child to the shared key, then join the reductions — a partial fix restores the bug it was meant to remove ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> Pre-aggregating before a join means grouping each child table to the parent key first and joining those aggregates. It fixes the fan-out math — SUM of a parent column stops counting each order once per item — and it gives the join two compact inputs, one row per group, which is ideal for a hash join. When several fact tables hang off one dimension, I aggregate every one of them to the key; otherwise the remaining raw stream multiplies the others back.
