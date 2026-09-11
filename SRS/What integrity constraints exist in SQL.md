<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> SQL's integrity constraints: **NOT NULL** (value required), **UNIQUE** (no duplicate non-NULL values), **PRIMARY KEY** (UNIQUE + NOT NULL, one per table — the row's identity), **FOREIGN KEY** (value must exist in the referenced table), **CHECK** (arbitrary boolean per row), **DEFAULT** (value when none supplied). Constraints live in the schema and the engine enforces them on every write — the database rejects bad data even when every application forgot to validate ([[What is the difference between PRIMARY KEY and UNIQUE]], [[Can a column referenced by a foreign key be NULL]]).

The verified demo fires each violation with its real error message — the detail interviewers remember: `UNIQUE constraint failed: acc.iban`, `CHECK constraint failed: balance >= 0`, `NOT NULL constraint failed: acc.iban`. PostgreSQL reports the same classes (`duplicate key value`, `new row violates check constraint`, `null value in column ... violates not-null constraint`). Two nuances worth volunteering. First, constraints are *declarative* — the alternative (application-side validation) protects against one app's bugs, not the DBA script, the migration, or the second microservice; the database-level constraint is the last line that cannot be bypassed by a client. Second, enforcement has cost and timing: UNIQUE and FK constraints need index lookups per write (FK checks fire per statement unless deferred), CHECK runs per row — cheap in isolation, visible in bulk loads where loaders legitimately disable and re-enable constraints around the load ([[How do you add constraints to a database]]). DEFAULT is the quiet one: it fills the column when the INSERT omits it — the demo shows `kind` surviving an explicit NULL... no: DEFAULT applies to *omission*, not to explicit NULL (a trap the NOT NULL + DEFAULT combination exposes).

```sql
CREATE TABLE acc (id INTEGER PRIMARY KEY, iban TEXT NOT NULL UNIQUE,
  balance NUMERIC NOT NULL CHECK (balance >= 0), kind TEXT DEFAULT 'personal');
INSERT INTO acc VALUES (1, 'DE89', 100, 'business');
-- (ok)
INSERT INTO acc VALUES (2, 'DE89', 50, 'personal');
-- ERROR: UNIQUE constraint failed: acc.iban
INSERT INTO acc VALUES (2, 'DE90', -5, 'personal');
-- ERROR: CHECK constraint failed: balance >= 0
INSERT INTO acc VALUES (2, NULL, 5, 'personal');
-- ERROR: NOT NULL constraint failed: acc.iban
```

**Listing 1.** Verified on SQLite 3.53.1. Three write attempts rejected by three different constraint classes with named errors — the schema defending itself without any application code.

```d2
direction: right
r: "INSERT / UPDATE / DELETE" {width: 200; height: 70}
c: "constraint layer
NN, UNIQUE, PK, FK, CHECK" {width: 220; height: 90}
a: "data accepted" {width: 130; height: 70}
x: "rejected + named error" {width: 190; height: 70}
r -> c
c -> a
c -> x
```

**Fig. 1.** Constraints are a gate in the write path: valid rows pass, violations bounce with a named error — regardless of which client issued the write.

> [!warning] DEFAULT fills omitted values, not NULL values
> `INSERT INTO acc (id, iban, balance) VALUES (...)` gets kind = 'personal'; `INSERT INTO acc VALUES (2, 'DE91', 5, NULL)` writes NULL and fails if the column is NOT NULL. The DEFAULT-versus-explicit-NULL distinction is a favorite gotcha because ORMs sometimes send NULL for unset fields, bypassing the default ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> The six constraint classes are NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK and DEFAULT. PRIMARY KEY is the row identity — unique plus not-null, one per table; FK ties a column to referenced values with cascade options; CHECK takes any row-level boolean. The point I emphasize: they are enforced by the engine on every write with named errors, so they protect data from every client including the ones that forgot validation, and UNIQUE plus FK enforcement ride on indexes, which is why bulk loads toggle them.
