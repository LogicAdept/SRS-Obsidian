<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# Can a column referenced by a foreign key be NULL?

> [!abstract] Short answer
> **Yes** — a foreign key column can be NULL in every mainstream engine. A NULL FK means "no related row" (the relationship is optional), not "invalid reference": the FK constraint only checks *non-NULL* values against the referenced table. `ON DELETE SET NULL` even produces NULL FKs deliberately when the referenced row is deleted ([[What integrity constraints exist in SQL]]).

The semantics fall out of the constraint's contract: FK validates that a *value* exists in the parent; NULL is the absence of a value, so there is nothing to validate. The verified demo covers all three behaviors: the NULL FK insert succeeds, the bogus reference fails with `FOREIGN KEY constraint failed`, and deleting the referenced customer SET NULLs the invoice's `cust_id` — the cascade option documented in PostgreSQL's constraints chapter alongside CASCADE and RESTRICT/NO ACTION. The design consequences are what the interviewer wants next: an optional relationship (`invoice.customer_id` nullable) versus a mandatory one (`NOT NULL` on the FK when every invoice must have a customer); and the NULL-FK filtering rule — joins and checks must use `IS NULL` semantics, because a plain join drops NULL-FK rows and `NOT IN` against the FK column turns poisoned ([[What does NULL mean in SQL]], [[Why is NOT IN dangerous with NULL]]). One engine nuance: SQLite enforces FKs only with `PRAGMA foreign_keys = ON` per connection (off by default, for backward compatibility) — the demo sets it explicitly; PostgreSQL enforces always ([[What is an anti-join in SQL]]).

```sql
PRAGMA foreign_keys = ON;
CREATE TABLE custs (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE invoices (id INTEGER PRIMARY KEY,
  cust_id INTEGER REFERENCES custs(id) ON DELETE SET NULL, total NUMERIC);
INSERT INTO custs VALUES (1,'Alice'),(2,'Boris');

INSERT INTO invoices VALUES (10, NULL, 99);
-- (ok: NULL FK = no customer yet, nothing to validate)
INSERT INTO invoices VALUES (11, 1, 50);
-- (ok: valid reference)
INSERT INTO invoices VALUES (12, 9, 50);
-- ERROR: FOREIGN KEY constraint failed
DELETE FROM custs WHERE id = 1;
-- (SET NULL fires)
SELECT id, cust_id FROM invoices ORDER BY id;
-- 10|
-- 11|
```

**Listing 1.** Verified on SQLite 3.53.1 (FK enforcement on). NULL inserts pass, invalid references fail, and deleting the parent rewrites children's FKs to NULL — the constraint's full lifecycle with an optional relationship.

```d2
direction: right
i: "invoice row" {width: 130; height: 60}
c: "cust_id = 5
must exist in parent" {width: 190; height: 70}
n: "cust_id = NULL
no parent required
constraint silent" {width: 220; height: 80}
i -> c
i -> n
```

**Fig. 1.** The constraint guards values, not absences: a real id must reference an existing parent; NULL means "relationship absent" and passes untouched.

> [!warning] A nullable FK silently changes every aggregation and join over it
> LEFT JOIN-based reports, NOT IN subqueries and NOT NULL assumptions all shift meaning where NULL FKs exist. Decide per column: mandatory relationship = NOT NULL FK (with a default or backfill strategy); optional = nullable, and every consumer handles the NULL branch explicitly ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> Yes, FK columns can be NULL — the constraint validates non-NULL values against the parent, and NULL means the relationship is optional. ON DELETE SET NULL produces NULLs by design. The nuances I add: make the FK NOT NULL when the relationship is mandatory; SQLite needs PRAGMA foreign_keys ON per connection while PostgreSQL always enforces; and nullable FKs change join and aggregation semantics, so consumers must handle the missing-relationship branch explicitly.
