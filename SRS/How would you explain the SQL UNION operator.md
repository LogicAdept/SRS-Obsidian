<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How would you explain the SQL UNION operator?

> [!abstract] Short answer
> `UNION` combines the result sets of two queries into one: `query1 UNION query2` returns every row that appears in **at least one** operand, with duplicates removed. `UNION ALL` keeps duplicates. Both operands must produce the **same number of columns with compatible types**; column names come from the first query.

PostgreSQL's reference defines it as set union: a row is in the result if it appears in at least one operand, and "the result of UNION does not contain any duplicate rows unless the ALL option is specified". `UNION` (dedup) is logically equivalent to `SELECT DISTINCT` over the `UNION ALL` of both operands — deduplication is a full sort-or-hash step over the combined rows, which is why "UNION ALL is usually significantly quicker than UNION; use ALL when you can" ([[When should you use UNION ALL instead of UNION]]).

Mechanics worth stating: the operands are full queries (each may have its own `WHERE`, joins, grouping); the **combined** query takes `ORDER BY` and `LIMIT` only after the last operand, and they apply to the combined result; matching is by column *position*, not name; and multiple `UNION`/`INTERSECT`/`EXCEPT` operators chain left to right unless parenthesized ([[How would you explain limitations of the SQL UNION operator]]).

```sql
CREATE TABLE a (v TEXT); CREATE TABLE b (v TEXT);
INSERT INTO a VALUES ('x'),('y'),('x');
INSERT INTO b VALUES ('y'),('z');

SELECT v FROM a UNION SELECT v FROM b ORDER BY v;
-- x
-- y
-- z
-- ('x' appeared twice in a, 'y' in both: deduplicated)

SELECT v FROM a UNION ALL SELECT v FROM b ORDER BY v;
-- x,y,x,y,z  (5 rows, duplicates kept)
```

**Listing 1.** Verified on SQLite 3.53.1. `UNION` returns the three distinct values; `UNION ALL` returns all five rows. Dedup cost grows with operand size — on the 2,000-row demo in [[When should you use UNION ALL instead of UNION]], `UNION` returns 100 rows where `UNION ALL` returns 4,000.

```d2
direction: right
q1: "query 1\nrows A + B" {width: 160; height: 80}
q2: "query 2\nrows B + C" {width: 160; height: 80}
stack: "concatenate\n(UNION ALL)" {width: 180; height: 80}
dedup: "deduplicate\nsort or hash" {width: 180; height: 80}
out: "result set" {width: 130; height: 80}
q1 -> stack
q2 -> stack
stack -> dedup -> out
```

**Fig. 1.** `UNION ALL` is the first half only; plain `UNION` adds the dedup stage, which is the whole cost and semantic difference between them.

> [!warning] Column *names* of a UNION come from the first operand — and types must be compatible, not equal
> `SELECT id, name FROM a UNION SELECT dept_id, d.name FROM b` binds by position: if the second query's first column is a different compatible type, the engine casts silently or fails on incompatible pairs. Number-of-columns mismatch always fails ([[How would you explain limitations of the SQL UNION operator]]).

> [!tip] Interview answer
> UNION stacks two result sets and deduplicates, UNION ALL just stacks; both operands need the same column count with compatible types, matched by position, and ORDER BY or LIMIT applies to the combined result only. I mention that dedup makes UNION a sort-or-hash over the whole result — so when duplicates are impossible or acceptable, UNION ALL is the faster and more honest choice.
