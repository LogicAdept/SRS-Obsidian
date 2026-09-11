<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# What is sargability in SQL

> [!abstract] Short answer
> A predicate is sargable (Search ARGument ABLE) when the engine can turn it into a seek over an index instead of evaluating it row by row: the column stands bare against a constant or expression, with no function wrapped around the column, no leading wildcard, and no type mismatch forcing a cast of the column side.

## What makes a predicate seekable

The index stores raw key values in sorted order, so the engine can only jump into that order if the predicate describes a contiguous range of the stored values. `WHERE email = 'x@y.z'`, `created_at >= '2026-01-01'`, and `col LIKE 'abc%'` all describe ranges of the stored form and are sargable. `WHERE LOWER(email) = ...` describes a range of transformed values the index never stored; `LIKE '%abc'` hides the start of the range; comparing a string column to a number may cast the column to the literal's type, discarding the stored form. PostgreSQL's B-tree page states exactly which operators are indexable for a type and that pattern matching works when the pattern is anchored to the beginning of the string, and its index introduction uses the same framing for the general operators; the same shape rules appear in MySQL's range optimization docs.

```sql
-- sargable
SELECT * FROM users  WHERE email = 'a@b.c';
SELECT * FROM orders WHERE created_at >= now() - interval '30 days';
SELECT * FROM users  WHERE email LIKE 'abc%';
-- non-sargable (column inside the function / hidden prefix)
SELECT * FROM users  WHERE LOWER(email) = 'a@b.c';
SELECT * FROM users  WHERE email LIKE '%abc';
```

**Listing 1.** The dividing line is whether the stored, sorted value form can be matched without per-row transformation.

## How to fix the classics

Wrap the constant instead of the column: `created_at >= '2026-01-01' AND created_at < '2027-01-01'` instead of `YEAR(created_at) = 2026` — the general mechanism is in [[Why does a function on a column prevent index use]]. For case-insensitive search, an expression index on `lower(email)` makes the transformed form indexed, per [[How do you implement case-insensitive search efficiently]]. For substring search there is no B-tree fix: you move to trigram, full-text, or a specialized engine, as in [[How do you optimize substring search in SQL]]. Match literal types to column types so the cast lands on the constant, the trap detailed in [[How does implicit type conversion hide an index]].

> [!warning] Sargability is necessary, not sufficient
> A sargable predicate can still produce a seq scan: low selectivity, tiny tables, stale statistics, or a better overall plan all make scanning cheaper, and the planner decides by cost. The reverse myth — "sargable means indexed" — confuses eligibility with the planner's decision. Also note operator-class and collation requirements for text pattern operators, which are engine-specific preconditions on top of predicate shape.

> [!tip] Interview answer
> Sargable means the predicate's shape lets the engine seek the index's stored order: bare column versus constant, no function on the column, no leading wildcard, no column-side casts. Functions on the column, '%x' patterns, and type mismatches are the classic killers, each with a standard fix: rewrite the range, add an expression index, or switch to trigram or full-text structures.
