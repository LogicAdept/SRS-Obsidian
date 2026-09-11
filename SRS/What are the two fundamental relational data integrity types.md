<!--
reps: 0
priority: 0
-->
#Databases/Keys #Databases/SQL #SRS

# What are the two fundamental relational data integrity types?

> [!abstract] Short answer
> **Entity integrity**: every row is identifiable — the table has a primary key and none of its components may be NULL or duplicated. **Referential integrity**: every non-NULL foreign key value must match an existing row in the referenced table. The first makes rows addressable, the second keeps relationships between tables truthful; everything else (CHECK, DEFAULT, domains) refines column content rather than identity.

## Entity integrity: rows must be addressable

Entity integrity lives in the key of the table. PostgreSQL's constraints chapter ties the pieces together: a primary key "can be used as a unique identifier for rows in the table", which "requires that the values be both unique and not null" — a NULL identifier would mean a row that no equality search can ever reach again, so the engine refuses it ([[How would you explain what a primary key is in relational databases]]). This is why primary key columns are forced NOT NULL even when you never write the words, and why the uniqueness side is enforced at write time rather than by a later cleanup query ([[Can the same primary key value appear in two rows of one table]]).

## Referential integrity: relationships must resolve

Referential integrity lives between tables: a foreign key value must "match the values appearing in some row of another table" — PostgreSQL's own phrasing for what the constraint "maintains". An orphan row (child pointing at a missing parent) is exactly the corruption class FK constraints exist to reject, and the declared referential action (CASCADE, SET NULL, RESTRICT, NO ACTION) decides what happens to children when a parent dies rather than leaving orphans behind ([[How would you explain foreign keys in relational databases]], [[What is foreign key cascading in a relational database]]).

```sql
CREATE TABLE depts (id INTEGER PRIMARY KEY, title TEXT NOT NULL);
CREATE TABLE emps (id INTEGER PRIMARY KEY,
  dept_id INTEGER NOT NULL REFERENCES depts(id), name TEXT);
INSERT INTO depts VALUES (1, 'IT');
INSERT INTO depts VALUES (1, 'HR');
-- ERROR: UNIQUE constraint failed: depts.id       (entity integrity)
INSERT INTO emps VALUES (1, 1, 'Greta');
-- ok
INSERT INTO emps VALUES (2, 9, 'Hans');
-- ERROR: FOREIGN KEY constraint failed            (referential integrity)
```

**Listing 1.** Verified on SQLite 3.53.1 with `PRAGMA foreign_keys = ON`. The duplicate department id violates entity integrity; the employee pointing at department 9 violates referential integrity — two different gates, two different named errors.

```d2
direction: right
row: "row in table" {width: 130; height: 60; style.fill: "#e3f2fd"}
ei: "entity integrity
PK unique + not null
row is addressable" {width: 220; height: 85; style.fill: "#e3f2fd"}
fk: "FK value in
child row" {width: 150; height: 60; style.fill: "#fff3e0"}
ri: "referential integrity
value exists in parent
(or is NULL by design)" {width: 240; height: 85; style.fill: "#fff3e0"}
row -> ei
fk -> ri
```

**Fig. 1.** Entity integrity guards the row's identity inside its own table; referential integrity guards the link between tables. A violation of either is rejected at write time with a named error.

> [!warning] The two types do not imply each other
> A table can have perfect entity integrity and still hold orphaned references if the FK was never declared or the engine skips it (SQLite runs with foreign keys off unless you opt in per connection) — and a fully FK-policed schema still fails entity integrity the moment someone sneaks a NULL into a key component. Naming the two types and then pointing at what breaks each one is the interview move; treating "constraints" as one undifferentiated blob is what the follow-up in [[What integrity constraints exist in SQL]] is designed to expose.

> [!tip] Interview answer
> Entity integrity: every row is uniquely addressable — a primary key with unique, non-NULL values. Referential integrity: every non-NULL foreign key resolves to an existing parent row, with declared actions for parent deletion. The first is about identifying rows within a table, the second about relationships between tables surviving writes. Both are enforced by the engine at write time, which is what separates them from application-side validation that only protects one client.

