<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How do you alter a table in a relational database?

> [!abstract] Short answer
> `ALTER TABLE` redefines a live table: add/drop/rename columns, change types and defaults, add or drop constraints. SQLite supports `RENAME COLUMN` (3.25+), `ADD COLUMN` (restricted: with DEFAULT, or CHECK; no primary-key additions), `DROP COLUMN` (3.35+), and `RENAME TO`; anything deeper follows its documented 12-step rebuild recipe. PostgreSQL ALTER handles all of the above plus type changes with `USING` conversion expressions ([[How do you add constraints to a database]]).

The verified demo exercises the common three on SQLite — rename, add, drop — and `PRAGMA table_info` confirms the schema morphed in place. The differences worth an interview minute are the *costs*. PostgreSQL's type change (`ALTER COLUMN ... TYPE bigint`) rewrites the whole table and rebuilds indexes (documented; with `USING` for the cast expression) — a table-length lock, which is why big-table type changes go through add-new-column/backfill/switch/drop-old. SQLite's ALTER is deliberately shallow because its schema is the CREATE statement text: ADD COLUMN can always append (existing rows materialize the DEFAULT), but a column that participates in the PK, a constraint change, or a column *removal* before 3.35 all meant the rebuild dance; DROP COLUMN since 3.35 is real but runs the same copy machinery internally for many cases. Online-safety framing completes the answer: every ALTER is either metadata-fast (rename), rewrite-slow (type change, drop in old engines), or validation-slow (constraint adds) — and the production playbook chooses per cost, not per syntax ([[What integrity constraints exist in SQL]], [[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE old_t (id INTEGER PRIMARY KEY, name TEXT);
ALTER TABLE old_t RENAME COLUMN name TO full_name;
-- (ok: SQLite 3.25+)
ALTER TABLE old_t ADD COLUMN city TEXT;
-- (ok: nullable append, instant)
ALTER TABLE old_t DROP COLUMN city;
-- (ok: SQLite 3.35+)
PRAGMA table_info(old_t);
-- 0|id|INTEGER|0||1
-- 1|full_name|TEXT|0||0
```

**Listing 1.** Verified on SQLite 3.53.1. Three ALTER forms mutate the live table, and the catalog readback shows `city` gone and `name` renamed — the schema is a mutable object, not a frozen CREATE.

```d2
direction: right
m1: "rename
metadata only" {width: 160; height: 80}
m2: "add column
append + default fill" {width: 180; height: 80}
m3: "type change / drop
rewrite or rebuild" {width: 190; height: 80}
t: "table lock grows ->" {width: 170; height: 70}
m1 -> t
m2 -> t
m3 -> t
```

**Fig. 1.** ALTER operations sort into cost tiers: renames touch the catalog, appends touch new writes only, and type changes or drops touch every stored row.

> [!warning] "ALTER works" and "ALTER works online" are different claims
> A rename is instant on any engine; a type change rewrites the table under a lock that a billion-row production table cannot afford. Migration tools chain cheap ALTERs into scheduled windows, do backfills in batches, and use views or expansion-contraction patterns to keep both reader generations alive ([[How do you alter a table in a relational database]]).

> [!tip] Interview answer
> ALTER TABLE covers add, drop, rename columns, type changes and constraint changes. SQLite's surface is the subset — rename since 3.25, drop since 3.35, ADD COLUMN with defaults or checks, and a documented rebuild recipe for the rest — while PostgreSQL does full ALTER including TYPE with USING. What I actually answer with is the cost model: renames are metadata, adds are appends, and type changes or constraint validations rewrite or scan the table under locks, so on big tables they become backfill migrations rather than one statement.
