<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# How does implicit type conversion hide an index

> [!abstract] Short answer
> When column and literal types differ, the engine casts one side to the other. If the cast lands on the column, the predicate stops being seekable: the comparison runs against transformed per-row values, not the stored sorted keys, so the plan degrades to a scan even though an index exists.

## The casting rules that matter

MySQL's rule is explicit and surprising: in comparisons between a string column and a number, MySQL converts the string column to a number, so `WHERE varchar_id = 123` cannot use an index on varchar_id — the manual states this verbatim in its type-conversion section, and it is the canonical example of a numeric literal on a string key column silently disabling the index. PostgreSQL generally casts the literal to the column's type, which keeps the index usable for common cases, but cross-type families still bite: comparing a uuid column to text, a varchar to an int in contexts where the cast applies per-row, or timestamp against a date literal in predicates where the planner cannot bound the range. The general principle: the cast must land on the constant side for the index to seek, the same bare-column principle as [[What is sargability in SQL]].

```sql
-- MySQL: string column vs numeric literal -> column cast to DOUBLE, index lost
SELECT * FROM orders WHERE external_ref = 123456;      -- external_ref VARCHAR
SELECT * FROM orders WHERE external_ref = '123456';    -- index used

-- PostgreSQL: uuid column vs text parameter in a driver that sends text
SELECT * FROM users WHERE id = $1::uuid;               -- explicit cast on the literal
```

**Listing 1.** Put the cast on the literal side, and the column's stored order stays matchable.

## How it shows up and how to catch it

The symptom is a plan that scans despite a matching index, often only in one environment: an ORM or driver binds parameters with the wrong type (strings for numbers, text for uuids, timestamps as strings), staging works against literals while production goes through prepared statements, and the difference is invisible in SQL review. The audit is mechanical — read the plan and look for the index you expected, following [[How do you read EXPLAIN ANALYZE in PostgreSQL]], and check the predicate's actual operator shape, which [[What is Index Cond versus Filter in EXPLAIN]] teaches you to distinguish. The fix is boring and effective: declare matching types, bind typed parameters, and cast constants explicitly rather than letting the engine guess, the same discipline behind keeping predicates sargable in [[Why does a function on a column prevent index use]].

> [!warning] "The index exists, so the type of the literal doesn't matter"
> This is the myth to kill. The index is on the column's stored form; a comparison against a differently-typed literal is a different predicate unless the cast is applied to the literal. There is also a subtle sibling: comparisons across collations or charset conversions in MySQL can similarly prevent index use on text columns. Both failures are environment-dependent, which is why they survive code review and explode in production.

> [!tip] Interview answer
> The index can only seek the column's stored, sorted form. If a type mismatch makes the engine cast the column side — MySQL casting a string column to a number against a numeric literal, or a text parameter compared to a uuid — the predicate no longer matches the stored keys and the plan scans. Fix by matching types and casting the literal, and verify with the plan, not by reading the DDL.
