<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> `INTERSECT` and `EXCEPT` are the other two set operators next to `UNION`: `query1 INTERSECT query2` returns rows output by **both** queries; `query1 EXCEPT query2` returns rows from the **left** query that the right query does not output. Both return **distinct** rows (`INTERSECT ALL`/`EXCEPT ALL` exist in some engines for keeping duplicates), both require the same column count with compatible types, and both take `ORDER BY` only after the last operand.

Microsoft's T-SQL reference defines them exactly this way: "EXCEPT returns distinct rows from the left input query that aren't output by the right input query. INTERSECT returns distinct rows that are output by both the left and right input queries." SQLite spells the right-hand operator `EXCEPT`, PostgreSQL uses `EXCEPT`, and Oracle instead offers `MINUS` as its historical name. Semantically, `A EXCEPT B` is the anti-join of A against B, and `A INTERSECT B` is a semi-join — both with built-in dedup ([[What is a semi-join in SQL]], [[What is an anti-join in SQL]]).

Practical rules: the first query supplies result column names; matching is positional; `NULL` rows compare as "equal to each other" for set purposes (two `NULL` rows are duplicates and are removed by the distinctness step), which differs from ordinary `=` comparisons ([[What does NULL mean in SQL]]); and `NOT IN`/`NOT EXISTS` differ from `EXCEPT` in that they do **not** dedup the left side and handle `NULL`s differently in the subquery ([[Why is NOT IN dangerous with NULL]]).

```sql
CREATE TABLE this_year (id INTEGER); CREATE TABLE last_year (id INTEGER);
INSERT INTO this_year VALUES (1),(2),(3),(3);
INSERT INTO last_year VALUES (2),(3),(4);

SELECT id FROM this_year EXCEPT SELECT id FROM last_year ORDER BY id;
-- 1                    (in this year, not in last year; the (3),(3) pair deduped)

SELECT id FROM this_year INTERSECT SELECT id FROM last_year ORDER BY id;
-- 2
-- 3                    (rows output by both; distinct)
```

**Listing 1.** Verified on SQLite 3.53.1 (error-free; `ORDER BY` applies to the compound result). T-SQL produces the same results with identical operator semantics; the T-SQL-only extra is syntax around it, e.g. `EXCEPT DISTINCT` naming in newer versions is *not* required — plain `EXCEPT` already implies distinct.

```d2
direction: right
left: "left query\nrows 1 2 3 3" {width: 170; height: 80}
right: "right query\nrows 2 3 4" {width: 170; height: 80}
i: "INTERSECT\nrows in BOTH\ndistinct: 2 3" {width: 190; height: 110}
e: "EXCEPT\nleft minus right\ndistinct: 1" {width: 190; height: 110}
left -> i
right -> i
left -> e
right -> e
```

**Fig. 1.** Two intersections of one idea: `INTERSECT` keeps the overlap, `EXCEPT` keeps the left's difference — both deduplicated, both shape-preserving on the left's column list.

> [!warning] `EXCEPT` dedups the left side — it is not "NOT EXISTS with formatting"
> If the left query outputs `(3),(3)`, `A EXCEPT B` returns one `3`. Using `EXCEPT` to "find missing rows" silently collapses duplicates the caller may need to count; `NOT EXISTS` over a join preserves the left side's multiplicity and is the safer pair for row-level anti-joins ([[What is an anti-join in SQL]], [[Why is NOT IN dangerous with NULL]]).

> [!tip] Interview answer
> INTERSECT and EXCEPT are the two remaining set operators: INTERSECT returns distinct rows produced by both queries, EXCEPT returns distinct rows of the left that the right does not produce — Oracle names that MINUS. Both operands need matching column counts and compatible types, names come from the first query, and ORDER BY sits after the last operand. The nuance I add: both dedup, so for row-level missing-row checks with multiplicity preserved, NOT EXISTS is usually the better tool.
