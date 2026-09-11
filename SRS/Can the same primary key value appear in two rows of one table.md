<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# Can the same primary key value appear in two rows of one table?

> [!abstract] Short answer
> **No.** The primary key is the table's identity: by definition its value is unique across all rows at every moment, and the engine enforces it — a duplicate PK insert fails with a unique-violation error. Every index-backed implementation (B-tree on the PK) makes the check exact and immediate ([[What is the difference between PRIMARY KEY and UNIQUE]]).

The verified demo shows the exact failure: the second insert of `k = 1` dies with `UNIQUE constraint failed: kv.k` — SQLite's phrasing of the underlying uniqueness violation (PostgreSQL: `duplicate key value violates unique constraint "kv_pkey"`). Three follow-ups complete the interview answer. *Why it cannot slip through:* uniqueness is enforced per-row at write time inside the statement's constraint checks — there is no configuration that permits two equal PK values in the same table (disabling triggers in PostgreSQL does not disable constraints; loaders that bypass uniqueness build a new table, not a duplicated one). *What people mistake for it:* duplicate *natural* data under a surrogate PK (two customer rows named alike with different ids — legal, and why business uniqueness needs its own UNIQUE constraint); and composite PKs, which forbid duplicate *combinations* while allowing individual column values to repeat — `(student_id, course_id)` in an enrollment table ([[How many normal forms are commonly taught for relational databases]]). *The race question:* two concurrent transactions inserting the same PK — one commits, the other's constraint check fails at commit/insert time; the constraint is the arbiter, the application just handles the error ([[What integrity constraints exist in SQL]]).

```sql
CREATE TABLE kv (k INTEGER PRIMARY KEY, v TEXT);
INSERT INTO kv VALUES (1, 'a');
INSERT INTO kv VALUES (1, 'b');
-- ERROR: UNIQUE constraint failed: kv.k
SELECT COUNT(*) FROM kv;
-- 1
-- composite PK: combinations unique, values may repeat
CREATE TABLE enrollment (student_id INTEGER, course_id INTEGER,
  PRIMARY KEY (student_id, course_id));
INSERT INTO enrollment VALUES (1, 1), (1, 2);
-- (ok: student 1 in two courses -- each combination distinct)
INSERT INTO enrollment VALUES (1, 2);
-- ERROR: UNIQUE constraint failed: enrollment.student_id, enrollment.course_id
```

**Listing 1.** Verified on SQLite 3.53.1. The duplicate single-column PK fails outright; the composite PK accepts `(1,1)` and `(1,2)` but rejects the repeated combination `(1,2)` — uniqueness applies to the key tuple.

```d2
direction: right
i1: "row id=1" {width: 120; height: 60}
i2: "row id=1
duplicate" {width: 130; height: 60}
ok: "rejected at write
named unique error" {width: 200; height: 70}
cp: "composite PK
(1,1) (1,2) ok
(1,2) again rejected" {width: 210; height: 80}
i1 -> ok
i2 -> ok
```

**Fig. 1.** Uniqueness is per key tuple: single-column PKs forbid any repeated value, composite PKs forbid repeated combinations — the engine rejects both at write time.

> [!warning] The PK guards identity, not business uniqueness — the duplicate-customer bug
> Two rows for the same real customer with different surrogate ids satisfy the PK and corrupt reporting. Business invariants (email, national id, per-tenant code) need their own UNIQUE constraints, ideally with a NOT NULL guard so multiple NULLs cannot quietly bypass them ([[What is the difference between PRIMARY KEY and UNIQUE]]).

> [!tip] Interview answer
> No — the PK's uniqueness is enforced per write by the engine, so a duplicate fails with a unique-violation error, immediately and unconditionally, including under concurrency where one of the two transactions loses. What is legal and often confused with it: repeating natural-looking values under a surrogate key, which is exactly why business uniqueness needs separate UNIQUE constraints. And composite PKs forbid repeated combinations while individual columns may repeat — the enrollment-table shape.
