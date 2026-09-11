<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How would you explain limitations of the SQL UNION operator?

> [!abstract] Short answer
> `UNION`'s limitations follow from its definition: both operands must have the **same number of columns** with **compatible types** (matched by position, not by name); result column names come from the **first** operand; `ORDER BY`/`LIMIT` are legal only **after the last operand** — individual operands cannot sort or page their own output; dedup is a full **sort-or-hash over the combined set**, so a plain `UNION` is expensive at scale; and row-locking clauses (`FOR UPDATE`) cannot be attached to a compound result.

Each constraint maps to a concrete failure or cost. Column-count mismatch is a hard error. Type mismatch either casts silently (integer to text) or fails on incompatible pairs (blob to number) — silent casts are the sneaky case, because the result column type then follows engine-specific resolution rules. Ordering inside an operand is discarded: the standard defines compound queries as unordered set combinations, so an `ORDER BY` before a set operator is a syntax error in most engines ([[How would you explain the SQL UNION operator]]). And because dedup compares **whole rows**, an `UNION` that differs in a hidden column (a timestamp, an internal id) keeps "duplicates" you expected to vanish.

```sql
-- Limitation 1: ORDER BY inside an operand is rejected.
SELECT v FROM a ORDER BY v UNION SELECT v FROM b;
-- ERROR: ORDER BY clause should come after UNION not before

-- Limitation 2: column count must match.
SELECT v, w FROM a UNION SELECT n FROM b;
-- ERROR: SELECTs to the left and right of UNION do not have
--        the same number of result columns

-- The legal place for ordering: after the last operand, over the combined set.
SELECT v FROM a UNION SELECT v FROM b ORDER BY v;
```

**Listing 1.** Verified on SQLite 3.53.1 (error text verbatim). PostgreSQL phrases the same two failures as "syntax error at or near UNION" (ORDER BY not allowed in a compound arm) and "each UNION query must have the same number of columns". Type-compatibility behavior differs more between engines than the two structural errors above.

```d2
direction: right
arm1: "operand 1\nown WHERE, GROUP BY" {width: 200; height: 80}
arm2: "operand 2\nown WHERE, GROUP BY" {width: 200; height: 80}
no: "no own ORDER BY / LIMIT\n(rejected)" {width: 220; height: 80}
combine: "combine + dedup\nsort or hash over all rows" {width: 240; height: 80}
tail: "ORDER BY / LIMIT\ncombined result only" {width: 220; height: 80}
arm1 -> combine
arm2 -> combine
combine -> tail
no -> arm1 [style.stroke: "#b71c1c"]
```

**Fig. 1.** Arms may filter and aggregate; ordering and paging belong to the compound query — the one `ORDER BY` after the last arm orders the final set.

> [!warning] `UNION` dedup compares whole rows — one differing hidden column defeats it
> If the operands select `SELECT *` or include an audit timestamp, every row differs and the dedup stage pays its full sort/hash cost while removing nothing. Project only the columns you mean to compare, or drop the dedup with `UNION ALL` ([[When should you use UNION ALL instead of UNION]]).

> [!tip] Interview answer
> The constraints are: equal column count with compatible types matched by position, names inherited from the first query, ORDER BY and LIMIT only after the last operand, no FOR UPDATE on the compound, and a real dedup cost — a sort or hash over every combined row. I flag the two runtime surprises: silent type casts and whole-row dedup being defeated by any hidden differing column.
