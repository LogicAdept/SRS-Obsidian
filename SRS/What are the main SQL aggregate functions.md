<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What are the main SQL aggregate functions?

> [!abstract] Short answer
> The five core aggregates: `COUNT` (rows or non-NULL values), `SUM`, `AVG`, `MIN`, `MAX`. They share one defining rule: **every aggregate except COUNT(*) ignores NULL inputs**. Beyond the five: `GROUP_CONCAT`/`string_agg` (lists), `array_agg`, statistical sets (`STDDEV`, `VARIANCE`), boolean aggregates (`BOOL_AND`/`BOOL_OR`, SQLite has none) and JSON aggregates in newer engines.

NULL semantics are the heart of every aggregate answer. `SUM` over an all-NULL or empty input returns NULL — not zero — and `AVG` divides by the count of *non-NULL* values, not by row count; only COUNT returns a number (zero) on empty input ([[What does NULL mean in SQL]]). On our demo table the mechanics are visible: ten orders, `COUNT(*)` and `COUNT(amount)` both 10 (amount has no NULLs — on customers, COUNT(city) is 5 of 6), AVG = 100.1, and over an empty filter SUM and AVG print as empty (NULL) while COUNT prints 0. `MIN`/`MAX` on strings use collation order; on dates, chronology. GROUP_CONCAT (SQLite, MySQL) and string_agg (PostgreSQL) concatenate values into a delimited string — SQLite demonstrated with `45.5,25`. DISTINCT inside aggregates is legal and changes the computation: `AVG(DISTINCT x)` averages unique values — almost never what people want ([[What is the difference between COUNT star and COUNT of a column]]). Window counterparts (`AVG(...) OVER (...)`) reuse the same functions per partition without collapsing rows ([[How would you explain the main ranking functions in Transact-SQL]]).

```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5),(104,3,45.5),(105,3,300),
 (106,NULL,60),(107,4,25),(108,3,25),(109,5,150),(110,5,150);

SELECT COUNT(*) AS n, COUNT(amount) AS amounts, SUM(amount) AS s,
       AVG(amount) AS a, MIN(amount) AS mn, MAX(amount) AS mx FROM orders;
-- 10|10|1001.0|100.1|25|300
SELECT COUNT(*), SUM(amount), AVG(amount) FROM orders WHERE amount > 10000;
-- 0||
SELECT GROUP_CONCAT(DISTINCT amount) FROM orders WHERE amount <= 50;
-- 45.5,25
```

**Listing 1.** Verified on SQLite 3.53.1. On the empty filter, COUNT returns 0 while SUM and AVG return NULL — the canonical empty-set aggregate rule. GROUP_CONCAT builds a delimited list from distinct values.

```d2
direction: right
i: "input values
per group" {width: 140; height: 70}
n: "NULLs dropped
(except COUNT(*))" {width: 170; height: 70}
f: "COUNT / SUM / AVG /
MIN / MAX / GROUP_CONCAT" {width: 240; height: 90}
o: "one scalar per group" {width: 190; height: 70}
i -> n -> f -> o
```

**Fig. 1.** An aggregate is a group-to-scalar reducer with a built-in NULL filter on its input — COUNT(*) being the only function that counts rows before that filter.

> [!warning] SUM returning NULL instead of 0 leaks into application arithmetic
> A report showing "no total" for an empty group (NULL) versus "no orders" (0) is the same query with different COALESCE decisions — and code doing `sum + tax` breaks on the NULL case. Decide per report whether empty means zero or unknown, and say it with COALESCE explicitly ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> The core aggregates are COUNT, SUM, AVG, MIN and MAX, plus GROUP_CONCAT or string_agg for lists. The rule I lead with: all of them ignore NULL inputs except COUNT(*), AVG divides by non-NULL count, and SUM or AVG on an empty input return NULL, not zero — only COUNT returns 0. DISTINCT inside an aggregate is legal but rarely intended, and the same functions work as window functions per partition when I need the aggregate without collapsing rows.
