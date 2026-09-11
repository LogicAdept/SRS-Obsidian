<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How do you write SQL queries for classic practice tasks?

> [!abstract] Short answer
> The classic interview tasks and their canonical shapes: **second-highest salary** — `DENSE_RANK() OVER (ORDER BY amount DESC)` filtered to rank 2 (handles ties correctly) or portable `ORDER BY amount DESC LIMIT 1 OFFSET 1`; **find duplicates** — `GROUP BY key HAVING COUNT(*) > 1`; **running total** — `SUM(...) OVER (PARTITION BY ... ORDER BY ...)`; **top-N per group** — `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` filtered to N; **Nth-highest per group** — DENSE_RANK again ([[How would you explain the SQL GROUP BY clause]], [[How would you explain the SQL HAVING clause]]).

The verified demo runs the three most-asked on one dataset, and each has a decision worth stating aloud. Second-highest: the window form with DENSE_RANK is *tie-correct* (two rows sharing the top amount both get rank 1, and rank 2 is the genuinely second value — 150), while the LIMIT/OFFSET form needs `DISTINCT` to mean the same thing; the naive `MAX(amount) < (SELECT MAX(...))` form fails when the top value is unique-but-the-second-is-duplicated... it actually handles that, but breaks when only one distinct value exists (returns empty instead of NULL — decide which the task wants). Duplicates: the GROUP BY/HAVING shape is the whole answer; the follow-up is "delete the duplicates" — `DELETE ... WHERE id NOT IN (SELECT MIN(id) ... GROUP BY key)` — with the NOT IN NULL caveat if the key is nullable ([[Why is NOT IN dangerous with NULL]]). Running total: the window frame matters — default `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` with ORDER BY gives the cumulative sum the task expects; the peer-row subtlety (RANGE includes tied peers in the same bucket) is the expert footnote ([[What are the main SQL aggregate functions]]).

```sql
SELECT DISTINCT amount FROM (
  SELECT amount, DENSE_RANK() OVER (ORDER BY amount DESC) AS r FROM orders
) t WHERE r = 2;
-- 150
SELECT DISTINCT amount FROM orders ORDER BY amount DESC LIMIT 1 OFFSET 1;
-- 150
SELECT amount, COUNT(*) AS c FROM orders
GROUP BY amount HAVING COUNT(*) > 1 ORDER BY amount;
-- 25|2
-- 45.5|2
-- 150|2
SELECT customer_id, id, amount,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY id) AS running
FROM orders WHERE customer_id IN (1, 3) ORDER BY customer_id, id;
-- 1|101|120|120
-- 1|102|80|200
-- 3|104|45.5|45.5
-- 3|105|300|345.5
-- 3|108|25|370.5
```

**Listing 1.** Verified on SQLite 3.53.1. Both second-highest spellings agree on 150; duplicates surface with counts; the running total accumulates per customer partition in id order — the three canonical tasks, complete with outputs.

```d2
direction: right
t1: "Nth-highest
DENSE_RANK + filter" {width: 170; height: 80}
t2: "duplicates
GROUP BY + HAVING" {width: 180; height: 80}
t3: "running total
SUM OVER (ORDER BY)" {width: 190; height: 80}
t4: "top-N per group
ROW_NUMBER + filter" {width: 190; height: 80}
```

**Fig. 1.** The canon is four shapes: window functions cover ranking and accumulation, GROUP BY/HAVING covers set-level predicates — everything else is decoration.

> [!warning] The tasks hide one decision each — say it before coding
> Second-highest: ties included (DENSE_RANK) or positions counted (ROW_NUMBER)? Duplicates: keep the lowest id or the latest? Running total: reset per partition or global? Two candidates who write "correct" SQL with different unstated choices produce different outputs — the articulate answer wins the point ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> My canon: second-highest via DENSE_RANK over a descending order filtered to rank two — tie-correct — with LIMIT/OFFSET as the portable fallback; duplicates via GROUP BY key HAVING COUNT over one; running total via SUM OVER PARTITION BY the entity ORDER BY time; top-N per group via ROW_NUMBER filtered to N. For each I state the hidden decision — tie handling, which duplicate survives, partition boundaries — because the shapes are easy and the semantics choices are what is actually being tested.
