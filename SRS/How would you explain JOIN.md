<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How would you explain JOIN?

> [!abstract] Short answer
> A `JOIN` combines rows of two tables into one result by matching them against a join condition: for every pair of rows that satisfies the condition (typically `t1.key = t2.key`), one output row is produced from the concatenated columns. `FROM a JOIN b ON ...` is an **inner** join by default; `LEFT`, `RIGHT`, `FULL` and `CROSS` variants change which unmatched rows survive ([[What kinds of SQL JOIN exist]]).

Joins are the direct consequence of normalization: business facts are split across tables (customers, orders, items), and a join reconstructs the wider row at query time. The PostgreSQL tutorial defines the join step exactly this way — a join of two tables "on" a condition checks pairs of their rows for the condition and outputs the combined row for each match ([[What conditions define a relational database]]). Rows without a partner are silently dropped by an inner join, which is the single most common logical bug: an inner join to `orders` removes customers who never ordered, so audience counts silently shrink. The join condition usually references a key, but SQL accepts any boolean expression — ranges, inequalities (`ON o.date BETWEEN s.from AND s.to`), even constants — and the engine's job is only to find matching pairs efficiently ([[What is the difference between Nested Loop Hash Join and Merge Join]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO customers VALUES (1,'Alice'),(2,'Boris'),(3,'Carla');
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5);

SELECT o.id, c.name, o.amount
FROM orders o JOIN customers c ON c.id = o.customer_id
ORDER BY o.id;
-- 101|Alice|120
-- 102|Alice|80
-- 103|Boris|45.5
-- (Carla has no orders: one input row, no output rows)
```

**Listing 1.** Verified on SQLite 3.53.1. Each order found exactly one matching customer and produced one row; Carla, having no match, contributes nothing — the defining property of an inner join.

```d2
direction: right
o: "orders rows
101 102 103" {width: 160; height: 80}
c: "customers rows
1 2 3" {width: 160; height: 80}
j: "join on c.id = o.customer_id
one row per matched pair" {width: 230; height: 90}
o -> j
c -> j
```

**Fig. 1.** A join is a pairwise matcher: the condition is evaluated against row pairs, and every satisfied pair becomes one concatenated output row.

> [!warning] An inner join is a filter — unmatched rows vanish
> Any row on either side without a match is dropped. If a report "lost" customers or the totals shrank after adding a join, that is the mechanism at work, not a data bug. Decide explicitly whether unmatched rows must survive, and if so use `LEFT JOIN` with an `IS NULL` check or aggregate against a pre-joined subquery ([[How does LEFT JOIN differ from INNER JOIN in SQL]], [[Why can a JOIN multiply your row count]]).

> [!tip] Interview answer
> A join combines two tables by evaluating a condition against row pairs and emitting one row per satisfying pair, usually on a key match. Inner join keeps only matches; LEFT, RIGHT and FULL keep the unmatched side padded with NULLs; CROSS keeps everything. Joins exist because normalized data is split across tables and must be reassembled at query time. The nuance I add: an inner join is also a filter — unmatched rows disappear, which is why "rows went missing" bugs usually trace back to a join that should have been a LEFT JOIN.
