<!--
reps: 0
priority: 0
-->
#Databases/Keys #Databases/SQL #SRS

# How would you explain simple keys versus composite keys in databases?

> [!abstract] Short answer
> A simple key is one column that identifies rows; a composite key is two or more columns whose **combination** is the identifier. The uniqueness of a composite key applies to the whole tuple — individual columns may repeat freely — and every component must be NOT NULL, because a row missing part of its identifier is not identifiable.

## When one column is enough, and when only a tuple works

A simple key fits when a single attribute really is unique per row: a surrogate id, a natural code. Composite keys earn their place when no single column identifies the row — junction rows in many-to-many relationships, positions that only exist as a coordinate (aisle, rack, level in a warehouse), or scoped identities like (tenant_id, local_id). PostgreSQL accepts both shapes: a column-level `PRIMARY KEY` for the simple case, and a table-level `PRIMARY KEY (a, b, c)` — or `UNIQUE (a, b, c)` for non-primary candidate keys — for the composite case ([[What integrity constraints exist in SQL]]). Composite keys are a full topic of their own, including the index-order consequences in [[How would you explain composite keys in relational databases]] and the lookup rules in [[What is the leftmost prefix rule for composite indexes]]; the comparison card's job is the choice itself.

```sql
CREATE TABLE bins (
  aisle INTEGER NOT NULL,
  rack  INTEGER NOT NULL,
  lvl   INTEGER NOT NULL,
  sku   TEXT,
  PRIMARY KEY (aisle, rack, lvl)
);
INSERT INTO bins VALUES (1, 1, 1, 'A');
INSERT INTO bins VALUES (1, 1, 2, 'B');
INSERT INTO bins VALUES (2, 1, 1, 'C');
-- same aisle and rack as row 1 -- fine: the tuple differs
INSERT INTO bins VALUES (2, 1, 1, 'D');
-- ERROR: UNIQUE constraint failed: bins.aisle, bins.rack, bins.lvl
INSERT INTO bins (aisle, rack, lvl) VALUES (2, 1, NULL);
-- ERROR: NOT NULL constraint failed: bins.lvl
```

**Listing 1.** Verified on SQLite 3.53.1. Aisle 2 repeats, rack 1 repeats — the repeated combination is what fails. And the NULL component is rejected: partial identity is no identity.

```d2
direction: right
s: "simple key
one column
(id)" {width: 170; height: 80; style.fill: "#e3f2fd"}
c: "composite key
(aisle, rack, lvl)
tuple identity" {width: 210; height: 80; style.fill: "#fff3e0"}
r1: "parts may repeat
across rows" {width: 190; height: 70; style.fill: "#e8f5e9"}
r2: "the full combination
never repeats" {width: 200; height: 70; style.fill: "#e8f5e9"}
c -> r1
c -> r2
s -> r2
```

**Fig. 1.** Both key shapes converge on the same rule at the tuple level: for simple keys the tuple is one column, so "no repeated combinations" reads as plain uniqueness; composite keys distribute that uniqueness across the parts.

## The follow-ups an interviewer will attach to the choice

Choosing composite over simple has knock-on effects. Foreign keys referencing a composite key must carry the full column list and match the whole tuple, so child tables inherit the width. Some engines tie the primary key to physical layout — a clustered PK in InnoDB or SQL Server spreads its width into every secondary index — which pushes wide tuples toward a narrow surrogate PK plus a composite UNIQUE constraint instead ([[Is a primary key implemented as an index and why]], [[How many clustered indexes can a table have and what is a clustered index physically]]). And a composite key is a uniqueness concept, not an index recipe: the composite index built for it serves ordered lookups by its leading columns, which is a separate decision from identity ([[Can the same primary key value appear in two rows of one table]]).

> [!warning] "Composite means every column is unique" — the instant-fail answer
> Uniqueness applies to the combination only: `(2, 1, 1)` and `(1, 1, 1)` coexist in the verified listing because the tuples differ. Conflating a composite key with per-column uniqueness — or with a composite index, which is an access path — is the mistake [[How would you explain composite keys in relational databases]] warns about; mixing a parent tag with the child concept on one card is the same category error in reverse.

> [!tip] Interview answer
> Simple key: one identifying column. Composite key: a tuple of columns that is unique as a whole — parts may repeat, combinations may not, and no component may be NULL. I reach for composite keys when no single attribute identifies the row: junction tables, coordinates, per-tenant scoping. The consequences I name: foreign keys must reference the full tuple, index behavior follows column order, and in clustered engines wide keys bloat every secondary index — which is when a narrow surrogate plus a composite UNIQUE wins.

