<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> When a predicate compares values of different types, the engine **converts one side** — and *which* side it converts decides whether the index survives. If the column side is converted (SQL Server's classic `varchar_col = N'literals'` or `varchar_col = 12345`), the seek becomes a scan: every row's column is cast before comparing. Engines that convert the *literal* side (SQLite's type affinity) keep the index usable ([[What is sargability in SQL]]).

SQL Server's data-type precedence rules — documented in its reference: the lower-precedence type converts to the higher — produce the production-classic: comparing a `varchar` column to an integer literal (int outranks varchar) converts the *column*, and `CONVERT_IMPLICIT` appears in the plan where an `Index Seek` should be. SQLite takes the opposite, safer-for-indexes route, verified in the demo: a TEXT-affinity column compared to the numeric literal `10` has its affinity applied to the *literal* (number to text), the comparison still matches index keys, and the plan stays `SEARCH ... USING COVERING INDEX`; `typeof(v)` returns `text`, proving the stored column was never converted ([[What is the difference between SQL char and varchar types]]). PostgreSQL's behavior is again literal-side: a `numeric_col = '42'` casts the constant, not the column. The interview checklist: quote the rule "the side that gets converted is the side that can't use the index", name one engine per behavior, and the preventive habit — compare like types deliberately, never rely on conversion semantics in hot predicates ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE tt (v TEXT);
INSERT INTO tt VALUES ('10'),('20');
CREATE INDEX idx_tt ON tt(v);

EXPLAIN QUERY PLAN SELECT * FROM tt WHERE v = '10';
-- QUERY PLAN
-- `--SEARCH tt USING COVERING INDEX idx_tt (v=?)
EXPLAIN QUERY PLAN SELECT * FROM tt WHERE v = 10;
-- QUERY PLAN
-- `--SEARCH tt USING COVERING INDEX idx_tt (v=?)
SELECT v, typeof(v) FROM tt WHERE v = 10;
-- 10|text
```

**Listing 1.** Verified on SQLite 3.53.1. The numeric literal was converted to text (affinity applied to the right-hand side), the column's stored values were untouched, and both plans seek the index — the literal-side conversion that keeps sargability.

```d2
direction: right
q: "text_col = 12345" {width: 180; height: 70}
a: "literal converted
(SQLite affinity, PG cast)
index seek survives" {width: 250; height: 90}
b: "column converted
(SQL Server precedence)
convert per row, scan" {width: 250; height: 90}
q -> a
q -> b
```

**Fig. 1.** One predicate, two possible plans: the engine's conversion side-effect decides whether the B-tree can answer it or every row must be cast and tested.

> [!warning] The conversion is invisible in the query text and explicit only in the plan
> Nothing in `WHERE v = 10` hints at a conversion; only EXPLAIN reveals `CONVERT_IMPLICIT` on the column or a silent scan. Code review cannot catch it reliably — the type discipline lives in the schema (use matching parameter types in drivers and ORMs) and in plan checks for hot queries ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> Type mismatch triggers an implicit conversion, and which side gets converted decides index use: if the column is converted — SQL Server converting varchar to int because int has higher precedence — the seek becomes a per-row cast and scan. Engines like SQLite convert the literal side via type affinity, and PostgreSQL casts constants, so the index survives; my demo shows SQLite still searching the index with a numeric literal against a text column. The habit: match types deliberately between column, literal, and driver parameter.
