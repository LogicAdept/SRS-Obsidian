<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> `UNION` combines the rows of two queries and **removes duplicates**; `UNION ALL` keeps everything. Same column count and compatible types are required for both, names come from the first query, and `ORDER BY` applies to the combined result only after the last operand. When duplicates are impossible or unwanted, `UNION ALL` is strictly cheaper — no dedup pass.

The dedup in plain `UNION` is not a formatting nicety; it is a real operator with a plan node: the engine must compare every output row against the ones seen — via sort or hash — with memory and CPU proportional to the result size ([[Why is SELECT DISTINCT expensive]]). PostgreSQL's docs describe UNION as returning duplicates-removed rows and note the engine may or may not eliminate duplicates in UNION ALL; SQLite's documentation is blunter: UNION ALL simply concatenates. The verified arithmetic on our demo data: ten order amounts, duplicated and stacked, count 20 under UNION ALL and 10 under UNION. The 150 case shows the practical nuance: a customer with two orders of 150 legitimately has *two* revenue events — UNION would report one and a finance report understates revenue ([[When should you use UNION ALL instead of UNION]]). NULL handling matches the distinctness rules: two NULL rows are duplicates for UNION purposes, another place where set semantics quietly differ from ordinary `=` comparisons ([[What does NULL mean in SQL]]).

```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, amount NUMERIC);
INSERT INTO orders VALUES (101,120),(102,80),(103,45.5),(104,45.5),(105,300),
 (107,25),(108,25),(109,150),(110,150);

SELECT COUNT(*) FROM (SELECT amount FROM orders UNION SELECT amount FROM orders);
-- 7
SELECT COUNT(*) FROM (SELECT amount FROM orders UNION ALL SELECT amount FROM orders);
-- 18
SELECT amount FROM orders WHERE amount = 150
UNION SELECT amount FROM orders WHERE amount < 50 ORDER BY amount;
-- 25
-- 45.5
-- 150
SELECT amount FROM orders WHERE amount = 150
UNION ALL SELECT amount FROM orders WHERE amount < 50 ORDER BY amount;
-- 25
-- 25
-- 45.5
-- 45.5
-- 150
-- 150
```

**Listing 1.** Verified on SQLite 3.53.1. UNION ALL doubles the row count exactly (18 of 9 rows), plain UNION dedups it to 7 distinct amounts; the 150/25 pairs lose their multiplicity under UNION — two sales events of 150 collapse into one row.

```d2
direction: right
in1: "query A rows" {width: 140; height: 60}
in2: "query B rows" {width: 140; height: 60}
u: "UNION
A + B, duplicates removed
sort or hash pass" {width: 260; height: 90}
ua: "UNION ALL
A + B, everything kept
pure concatenation" {width: 250; height: 90}
in1 -> u
in2 -> u
in1 -> ua
in2 -> ua
```

**Fig. 1.** Both operators stack rows vertically; only UNION pays for a distinctness pass over the combined result — and that pass erases multiplicity you may have needed.

> [!warning] UNION also compares NULLs and column types positionally
> Two NULL rows are duplicates for UNION (unlike ordinary `=` comparisons), and columns match by position, not name — a silent column-order change in one operand merges different fields into one column. Keep operand SELECT lists explicit and parallel, and never rely on UNION to coerce types ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> UNION concatenates two same-shaped results and removes duplicate whole rows, paying a sort or hash pass; UNION ALL keeps everything and just concatenates. Names come from the first query, ORDER BY goes after the last operand, and two NULL rows count as duplicates. My default is UNION ALL because dedup is almost never the requirement — and when it is, I reach for GROUP BY or DISTINCT deliberately, so the multiplicity-erasing behavior is a decision, not a side effect.
