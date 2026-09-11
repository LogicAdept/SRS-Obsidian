<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What kinds of SQL JOIN exist?

> [!abstract] Short answer
> SQL defines five join kinds: **INNER** (matching pairs only), **LEFT/RIGHT/FULL OUTER** (additionally keep unmatched rows of the named side padded with NULLs), and **CROSS** (cartesian product, no condition). `JOIN` alone means `INNER JOIN`. Comma-joins (`FROM a, b WHERE ...`) predate the `JOIN` keyword and are equivalent to an inner join with the condition in `WHERE`.

The PostgreSQL tutorial presents exactly this family and notes that `JOIN ... ON`, `LEFT/RIGHT/FULL OUTER JOIN` and `CROSS JOIN` differ only in what happens to non-matching rows. Two widely-interviewed wrinkles follow. First, engine support is not uniform: Oracle has no `FULL` keyword (it is emulated with `UNION ALL` of two joins), old SQLite versions (before 3.39) had neither `RIGHT` nor `FULL`, and MySQL still has no `FULL` — knowing one emulation per engine is part of the answer ([[How do you emulate RIGHT JOIN using only LEFT JOIN support]]). Second, the `USING (col)` shorthand joins on the shared column name and hides the duplicate column, while `NATURAL JOIN` matches *all* same-named columns implicitly — a maintenance hazard when a column rename silently changes the join predicate. The join condition may also be an inequality; SQL then just pairs every row combination that satisfies it ([[What kinds of problems does SQL JOIN solve]]).

```sql
CREATE TABLE l (k INTEGER, v TEXT);
CREATE TABLE r (k INTEGER, w TEXT);
INSERT INTO l VALUES (1,'a'),(2,'b'),(2,'b2');
INSERT INTO r VALUES (2,'x'),(3,'y');

SELECT l.k, l.v, r.w FROM l JOIN r ON r.k = l.k ORDER BY l.k, l.v;
-- 2|b|x
-- 2|b2|x
SELECT l.k, l.v, r.w FROM l LEFT JOIN r ON r.k = l.k ORDER BY l.k, l.v;
-- 1|a|
-- 2|b|x
-- 2|b2|x
SELECT l.v, r.w FROM l CROSS JOIN r ORDER BY l.v, r.w;
-- a|x
-- a|y
-- b|x
-- b|y
-- b2|x
-- b2|y
```

**Listing 1.** Verified on SQLite 3.53.1 (which since 3.39 also accepts `RIGHT`/`FULL`). The inner join drops row `1|a` and column `3|y`; LEFT keeps the left orphan with NULL padding; CROSS produces every pair — 3 times 2 rows.

```d2
direction: right
i: "INNER
matches only" {width: 150; height: 80}
l: "LEFT
+ left orphans" {width: 150; height: 80}
r: "RIGHT
+ right orphans" {width: 150; height: 80}
f: "FULL
+ all orphans" {width: 140; height: 80}
x: "CROSS
all pairs" {width: 140; height: 80}
i -> l -> f
i -> r -> f
l -> x
```

**Fig. 1.** The five kinds differ only in the fate of unmatched rows: INNER discards both sides, LEFT/RIGHT save one side, FULL saves both, and CROSS ignores matching entirely.

> [!warning] Comma-joins and NATURAL JOIN are traps, not features
> `FROM a, b WHERE a.k = b.k` mixes join logic into the filter list: forget one predicate and you get an accidental cartesian product that can return billions of rows. `NATURAL JOIN` binds the result to column names, so adding a column like `comment` to both tables changes every natural join in the codebase. Prefer explicit `JOIN ... ON` with named columns ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> There are five join kinds: INNER keeps matched pairs; LEFT, RIGHT and FULL OUTER additionally keep unmatched rows of the corresponding side, padded with NULLs; CROSS produces the cartesian product without a condition. JOIN alone means INNER. I mention engine gaps — MySQL and old SQLite lack FULL, Oracle calls it differently — and that USING and NATURAL are shorthand forms I avoid because they depend on column names. The semantics are universal; only syntax support varies.
