<!--
reps: 0
priority: 0
-->
#Databases/Keys #Databases/SQL #SRS

# How would you explain what a primary key is in relational databases?

> [!abstract] Short answer
> The primary key is the column (or column group) a table designates as its row identity: values must be unique and NOT NULL, there is at most one per table, and the engine enforces both on every write. PostgreSQL's documentation describes it as "a unique identifier for rows in the table" and notes that adding one automatically creates a unique B-tree index and forces the columns NOT NULL.

## The contract, and what it is for

The PK bundles three promises: uniqueness (no two rows share the identifier), non-nullness (every row has one), and singularity (one per table — while UNIQUE constraints are plural). The SQL-standard way to say the same thing: PRIMARY KEY is equivalent to UNIQUE NOT NULL, which is why PostgreSQL's docs show a `product_no integer UNIQUE NOT NULL` table accepting exactly the same data as the PRIMARY KEY form. Enforcement is not advisory — the engine checks each write, and duplicates or NULL identifiers fail with named errors ([[Can the same primary key value appear in two rows of one table]]). The identity role is what other machinery builds on: foreign keys reference it by default, clustered engines store rows physically by it, and replication uses it to find rows to change ([[Is a primary key implemented as an index and why]]).

```sql
CREATE TABLE accs (id INTEGER PRIMARY KEY, iban TEXT NOT NULL);
INSERT INTO accs VALUES (1, 'DE89');
INSERT INTO accs VALUES (1, 'DE90');
-- ERROR: UNIQUE constraint failed: accs.id
INSERT INTO accs VALUES (NULL, 'DE91');
-- ok in SQLite: INTEGER PRIMARY KEY is a rowid alias,
-- so NULL is replaced by the next rowid (2) instead of failing
SELECT id, rowid, iban FROM accs;
-- 1|1|DE89
-- 2|2|DE91
```

**Listing 1.** Verified on SQLite 3.53.1. The duplicate fails outright. The NULL insert shows a documented engine nuance: SQLite's INTEGER PRIMARY KEY is an alias for the rowid, so a NULL id auto-assigns the next rowid — while the standard's default reading (and PostgreSQL) rejects NULL PK values outright.

```d2
direction: right
u: "unique values
enforced per write" {width: 200; height: 75; style.fill: "#e3f2fd"}
n: "NOT NULL
every row identifiable" {width: 190; height: 75; style.fill: "#e3f2fd"}
o: "one per table
(UNIQUE constraints are plural)" {width: 230; height: 75; style.fill: "#fff3e0"}
id: "row identity:
referenced by FKs,
locator in clustered engines" {width: 250; height: 85; style.fill: "#e8f5e9"}
u -> id
n -> id
o -> id
```

**Fig. 1.** Three constraints make the primary key the row's identity — and identity is what downstream machinery (foreign keys, clustering, replication) consumes.

## Natural or surrogate — the design decision hiding in the definition

The definition does not choose the key for you. A natural key (iban, national id) carries meaning but changes when reality changes and couples the table to external formats; a surrogate key (identity sequence, UUID) is stable and meaningless but adds a second uniqueness problem, because business uniqueness then needs its own UNIQUE constraints ([[What is a unique database constraint for]]). The costs differ by engine: in SQLite the single-column INTEGER PK is free (it is the rowid), while in clustered engines the PK's width multiplies into every secondary index — the reason [[Should you use UUID as a primary key in PostgreSQL]] is a tradeoff question and not a default ([[How would you explain candidate keys in relational databases]] explains how the losing candidates remain enforced as UNIQUE).

> [!warning] The primary key guarantees identity, not business uniqueness
> Two rows for the same real customer under two different surrogate ids satisfy the PK perfectly and still corrupt your reporting. The PK answers "which row is this", never "is this row legitimate" — business invariants need their own UNIQUE constraints, ideally NOT NULL so multiple NULLs cannot quietly bypass them ([[What is the difference between PRIMARY KEY and UNIQUE]]).

> [!tip] Interview answer
> A primary key is the table's designated row identifier: unique, NOT NULL, one per table, enforced on every write and backed by a unique index the engine creates for you. It is what foreign keys reference and what clustered engines physically order rows by. The judgment I show in interviews: surrogate versus natural is a design tradeoff, not a law — and either way the PK is identity, not business-rule enforcement, which is what UNIQUE constraints are for.

