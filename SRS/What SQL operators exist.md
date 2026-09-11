<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What SQL operators exist?

> [!abstract] Short answer
> SQL operators fall into a handful of families: **arithmetic** (`+ - * / %`), **comparison** (`= <> != < <= > >=`, plus `IS NULL`, `IS DISTINCT FROM`, `BETWEEN`, `IN`, `LIKE`), **logical** (`AND`, `OR`, `NOT`), **set operators** (`UNION`, `INTERSECT`, `EXCEPT`), **string** (`||` concatenation, `LIKE`/`SIMILAR TO` patterns), and **bitwise** (`& | ^ ~ << >>`). The engine gives comparison operators the three-valued logic of `NULL`, which is where most operator surprises live.

The standard families, with dialect notes:

- **Arithmetic**: `+ - * / %`; integer/integer division truncates in many engines (`7/2 = 3` in SQLite/PostgreSQL, `3.5` in engines with true numeric promotion); `* /` bind tighter than `+ -`, parentheses override.
- **Comparison**: `= <> < <= > >=` return true/false/**unknown**; `NULL = NULL` is not true — use `IS NULL` / `IS NOT NULL`, and `IS DISTINCT FROM` for `NULL`-safe inequality ([[What does NULL mean in SQL]]). Range and membership sugar: `BETWEEN a AND b`, `IN (list)`, `IN (subquery)` ([[How would you explain SQL IN BETWEEN and LIKE predicates]]).
- **Logical**: `AND`, `OR`, `NOT` over three-valued logic; `NOT (unknown)` is still unknown, so negated predicates do not rescue `NULL` rows ([[Why is NOT IN dangerous with NULL]]).
- **Pattern/string**: `LIKE` with `%`/`_`, `ILIKE` in PostgreSQL, `||` concatenation (T-SQL uses `+` and `CONCAT`).
- **Set operators**: `UNION [ALL]`, `INTERSECT`, `EXCEPT` combine whole result sets, not scalars ([[How would you explain the SQL UNION operator]]).
- **Bitwise**: `& | ^ << >> ~` on integer types. Operator precedence is engine-defined but follows the same intuition as most languages — arithmetic over comparison, comparison over logical — so explicit parentheses are the cheap way to make intent survive code review.

```sql
-- Operator families side by side (SQLite).
SELECT 7 / 2 AS int_div, 7.0 / 2 AS real_div, 7 % 3 AS modulo, 2 * 3 AS mul;
-- 3|3.5|1|6
SELECT 5 > 3 AS gt, 'abc' < 'abd' AS str_cmp, NULL = NULL AS null_eq, NULL IS NULL AS null_is;
-- 1|1||1        (null_eq is NULL: empty output between pipes)
SELECT 1 AND 0 AS and01, 1 OR 0 AS or01, NOT 1 AS not01;
-- 0|1|0
SELECT 'data' || 'base' AS concat;
-- database
```

**Listing 1.** Verified on SQLite 3.53.1. Note the two traps in the middle row: `NULL = NULL` yields unknown (empty), while `IS NULL` yields true; and `7 / 2` truncates to `3` because both operands are integers — the same expression on `7.0` gives `3.5`.

```d2
direction: right
arith: "Arithmetic\n+ - * / %" {width: 160; height: 80}
cmp: "Comparison\n= <> < > IS NULL" {width: 200; height: 80}
logic: "Logical\nAND OR NOT" {width: 150; height: 80}
sets: "Set ops\nUNION INTERSECT EXCEPT" {width: 210; height: 80}
pattern: "String/Pattern\n|| LIKE ILIKE" {width: 180; height: 80}
cmp -> logic
cmp -> pattern
```

**Fig. 1.** The families compose: comparison operators feed logical operators, and pattern predicates are comparisons over strings; set operators sit one level above, joining whole queries.

> [!warning] `=` is the equality of a single value — it never reports "both unknown"
> Writing `WHERE col = NULL` is always false-or-unknown, never true; the engine does not warn you, the query just returns fewer rows. The same three-valued logic hides inside `IN`, `NOT IN`, and joins on nullable keys ([[Why is NOT IN dangerous with NULL]]).

> [!tip] Interview answer
> I group SQL operators as arithmetic, comparison, logical, set, string/pattern, and bitwise. The part that matters in practice is three-valued logic: comparisons with NULL return unknown, so you test with IS NULL or IS DISTINCT FROM, and AND/OR/NOT propagate that unknown through filters. Also worth naming: BETWEEN and IN as comparison sugar, LIKE for patterns, UNION/INTERSECT/EXCEPT as set-level operators, and dialect quirks like integer division or `+` vs `||` for strings.
