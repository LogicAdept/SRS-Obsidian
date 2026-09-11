<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> PostgreSQL: `ALTER TABLE ... ADD CONSTRAINT name UNIQUE/PK/FK/CHECK (...)`, plus column-level additions (`SET NOT NULL`, `SET DEFAULT`, typed `ADD COLUMN`) — constraints can also be added `NOT VALID` and validated later to avoid long locks. SQLite: ALTER is narrower — you can `ADD COLUMN` (with DEFAULT, CHECK, or a UNIQUE-with-index via `CREATE UNIQUE INDEX`), but not add a constraint to existing columns; the documented path is the 12-step table-rebuild recipe ([[How do you alter a table in a relational database]]).

The split is architectural, not a version gap: PostgreSQL's catalog holds constraints as objects, so ADD CONSTRAINT is metadata-plus-validation; SQLite's schema is the CREATE TABLE text, so constraints on *existing* columns require rewriting the table (its documentation prescribes the procedure: new table with the desired schema, copy, drop, rename, recreate indexes, fix foreign keys). The verified demo shows what SQLite does directly: ADD COLUMN with NOT NULL (requires a DEFAULT — otherwise the existing rows would violate it), ADD COLUMN with a CHECK, and the failure of PG-style `ADD CONSTRAINT` syntax. Adding a constraint on PostgreSQL also has a production twist worth naming: `ADD CONSTRAINT ... NOT VALID` applies the constraint to *new* rows immediately while a later `VALIDATE CONSTRAINT` checks existing rows with only a light lock — the standard answer to "how do you add a FK to a billion-row live table" ([[What integrity constraints exist in SQL]]). And the reverse direction is symmetric-ish: dropping constraints is easy in both (DROP CONSTRAINT / rebuild), which is why the ADD path is the one with the playbook ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE staff (id INTEGER PRIMARY KEY, name TEXT);
ALTER TABLE staff ADD COLUMN email TEXT NOT NULL DEFAULT 'unknown';
-- (ok: NOT NULL requires a DEFAULT for existing rows)
ALTER TABLE staff ADD COLUMN age CHECK (age > 0);
-- (ok: CHECK allowed on ADD COLUMN in SQLite)
ALTER TABLE staff ADD CONSTRAINT uq UNIQUE (name);
-- ERROR: near "UNIQUE": syntax error
-- (SQLite: no ADD CONSTRAINT; create UNIQUE INDEX instead, or rebuild the table)
CREATE UNIQUE INDEX staff_name_uq ON staff(name);
-- (ok: the SQLite route to uniqueness on an existing column)
```

**Listing 1.** Verified on SQLite 3.53.1. Column-level additions work within their rules; the PG-style ADD CONSTRAINT does not parse — the SQLite escape is a unique index, and a full table rebuild for CHECK/FK on old columns.

```d2
direction: right
pg: "PostgreSQL
ADD CONSTRAINT object
NOT VALID -> VALIDATE" {width: 240; height: 90}
sq: "SQLite
ADD COLUMN only
rebuild recipe for the rest" {width: 230; height: 90}
b: "big table production rule:
add NOT VALID, validate off-peak" {width: 270; height: 80}
pg -> b
sq -> b
```

**Fig. 1.** Same goal, two toolchains: catalog-object constraints on PostgreSQL, index-or-rebuild on SQLite — and a lock-aware procedure for large tables on both.

> [!warning] Adding a constraint validates every existing row — plan for the lock
> A plain `ADD CONSTRAINT ... CHECK/FK` on PostgreSQL takes a full-table validation under a lock that blocks writes; on a live big table that is an outage. The documented sequencing is NOT VALID now, VALIDATE CONSTRAINT later, and for FKs an index on the referencing column so the validation scan is not a second incident ([[How do you alter a table in a relational database]]).

> [!tip] Interview answer
> PostgreSQL adds constraints as catalog objects — ADD CONSTRAINT for UNIQUE, PK, FK and CHECK, plus SET NOT NULL — and for big live tables the pattern is NOT VALID first, then VALIDATE CONSTRAINT in a quiet window, since validation scans every row. SQLite's ALTER is narrower: ADD COLUMN with DEFAULT or CHECK, unique via a separate CREATE UNIQUE INDEX, and for constraints on existing columns the documented table-rebuild recipe. The principle either way: constraint addition is a validation scan, so schedule it like one.
