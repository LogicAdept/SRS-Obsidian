<!--
reps: 0
priority: 0
-->
#Databases/Keys #Databases/SQL #SRS

# What is automatic identity or autoincrement in different databases?

> [!abstract] Short answer
> Every engine ships a managed auto-numbering column, with different names and contracts: PostgreSQL has the SQL-standard `GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY` (plus the legacy serial macro); SQL Server has `IDENTITY(seed, increment)`, defaulting to (1,1); the MySQL/MariaDB family has the `AUTO_INCREMENT` column attribute — one per table, and the column must be part of a key; SQLite makes an `INTEGER PRIMARY KEY` an alias of the rowid and offers `AUTOINCREMENT` to forbid reuse of deleted ids. All mint values at insert time and never roll them back — gaps are by design.

## One idea, four contracts

PostgreSQL's identity columns attach "an implicit sequence" and fill newly inserted rows from it, and such a column is "implicitly NOT NULL" — with ALWAYS the system owns values (explicit inserts need OVERRIDING SYSTEM VALUE) while BY DEFAULT tolerates them ([[What is the difference between SERIAL and IDENTITY in PostgreSQL]] contrasts the standard feature with the legacy macro). SQL Server's IDENTITY takes explicit seed and increment — "you must specify both... or neither", with (1,1) as the default — and Microsoft documents the gap behavior: values consumed by a failed or rolled-back insert are lost and not regenerated. MariaDB documents the family contract for AUTO_INCREMENT: one per table, "it must be defined as a key", and in InnoDB a composite key forces the AUTO_INCREMENT column to be its first column; `LAST_INSERT_ID()` returns the session's last minted value. SQLite's move is different: INTEGER PRIMARY KEY *is* the rowid, so an omitted or NULL id auto-assigns; the AUTOINCREMENT keyword adds bookkeeping in `sqlite_sequence` "to prevent the reuse of ROWIDs from previously deleted rows" — at a documented cost in CPU, memory and disk ([[Should you use UUID as a primary key in PostgreSQL]] is the escape from engine-minted ids entirely).

```sql
CREATE TABLE plain (id INTEGER PRIMARY KEY, v TEXT);
INSERT INTO plain (v) VALUES ('a');
INSERT INTO plain (v) VALUES ('b');
DELETE FROM plain WHERE id = 2;
INSERT INTO plain (v) VALUES ('c');
SELECT id, v FROM plain;
-- 1|a
-- 2|c        (id 2 reused: rowid alias hands out the highest free id)

CREATE TABLE keyed (id INTEGER PRIMARY KEY AUTOINCREMENT, v TEXT);
INSERT INTO keyed (v) VALUES ('a');
DELETE FROM keyed WHERE id = 1;
INSERT INTO keyed (v) VALUES ('b');
SELECT id, v FROM keyed;
-- 2|b        (never 1 again: sqlite_sequence remembers the max ever used)
SELECT * FROM sqlite_sequence;
-- keyed|2
```

**Listing 1.** Verified on SQLite 3.53.1. Without AUTOINCREMENT the deleted id 2 is handed out again; with AUTOINCREMENT the counter only moves forward and `sqlite_sequence` records the high-water mark — the documented reuse-prevention contract, bought with extra bookkeeping.

```d2
direction: right
pg: "PostgreSQL
GENERATED AS IDENTITY
ALWAYS vs BY DEFAULT" {width: 230; height: 80; style.fill: "#e3f2fd"}
ms: "SQL Server
IDENTITY(seed, increment)
default (1,1), gaps stay" {width: 240; height: 80; style.fill: "#e3f2fd"}
my: "MySQL / MariaDB
AUTO_INCREMENT
one per table, must be keyed" {width: 250; height: 80; style.fill: "#fff3e0"}
sq: "SQLite
INTEGER PK = rowid alias
AUTOINCREMENT forbids reuse" {width: 260; height: 80; style.fill: "#fff3e0"}
```

**Fig. 1.** Four engines, one purpose: a system-managed numeric generator for the key column. The contracts differ on override rules, keying requirements, and reuse of deleted values — not on the fundamental "values are minted at insert and never rolled back".

> [!warning] Automatic numbering does not mean unique, and never means gap-free
> An identity column is NOT NULL and system-filled, but uniqueness is still only what you declare: a PostgreSQL identity column without a PRIMARY KEY or UNIQUE constraint accepts duplicates, and SQLite's AUTOINCREMENT lives on a column that is *already* the PK — the keyword adds reuse prevention, not uniqueness. Gaps, meanwhile, are structural: rolled-back and failed inserts burn values in every engine (SQL Server documents it explicitly; PostgreSQL sequences behave the same), so business logic must never assume "no holes" ([[What is the difference between SERIAL and IDENTITY in PostgreSQL]]).

> [!tip] Interview answer
> Same idea, per-engine contracts: PostgreSQL uses the standard GENERATED ALWAYS (or BY DEFAULT) AS IDENTITY over a sequence; SQL Server uses IDENTITY(seed, increment) with (1,1) defaults; the MySQL family uses AUTO_INCREMENT — one per table, it must be part of a key, and InnoDB wants it first in a composite; SQLite aliases INTEGER PRIMARY KEY to the rowid, with AUTOINCREMENT as the paid option that stops id reuse after deletes. All of them mint at insert time, never roll back, and none of them by themselves guarantee uniqueness — the key constraint does that.

