<!--
reps: 0
priority: 0
-->
#Databases/Keys #Databases/SQL #SRS

# How would you explain candidate keys in relational databases?

> [!abstract] Short answer
> A candidate key is any **minimal** set of columns that uniquely identifies a row — a key that *could* serve as the table's primary key. A table can have several at once; the one you designate becomes the PRIMARY KEY, and the remaining candidate keys stay in force as UNIQUE constraints. "Minimal" matters: once a column set is already unique, adding more columns to it destroys candidacy.

## From relational theory to SQL enforcement

Relational theory defines a candidate key as a minimal superkey: a column set whose values are unique across the table, and which stops being unique if you remove any column. PostgreSQL's constraints chapter defines the primary key as "a column, or group of columns, [that] can be used as a unique identifier for rows in the table", which requires values to be "both unique and not null" — that contract is what makes every candidate key an identity candidate, not just a lookup shortcut. SQL has no CANDIDATE KEY syntax: the designation is one choice plus enforcement for the rest — the chosen key becomes PRIMARY KEY, and every other candidate key is declared as a UNIQUE constraint, each of which PostgreSQL implements as a unique B-tree index ([[What is the difference between PRIMARY KEY and UNIQUE]]). The keys that lose the primary designation but keep their constraint are exactly what [[How would you explain alternate or secondary keys in relational databases]] calls alternate keys.

```sql
CREATE TABLE users (
  id           INTEGER PRIMARY KEY,      -- chosen candidate key (surrogate)
  email        TEXT NOT NULL UNIQUE,     -- natural candidate key, still enforced
  national_id  TEXT NOT NULL UNIQUE,     -- second natural candidate key
  name         TEXT NOT NULL
);
INSERT INTO users VALUES (1, 'a@x.io', 'N1', 'Ann');
INSERT INTO users VALUES (2, 'b@x.io', 'N2', 'Bob');
INSERT INTO users VALUES (3, 'a@x.io', 'N3', 'Cid');
-- ERROR: UNIQUE constraint failed: users.email
INSERT INTO users VALUES (4, 'c@x.io', 'N1', 'Dan');
-- ERROR: UNIQUE constraint failed: users.national_id
```

**Listing 1.** Verified on SQLite 3.53.1. Three candidate keys, all enforced: the surrogate `id` accepts both rows, but a repeated `email` and a repeated `national_id` each fail — candidacy does not expire when another key wins the primary slot.

```d2
direction: right
sk: "column sets that are
unique for all rows" {width: 210; height: 80; style.fill: "#e3f2fd"}
min: "drop columns until
minimal -> candidate keys" {width: 230; height: 80; style.fill: "#e3f2fd"}
pk: "one designated
PRIMARY KEY" {width: 180; height: 80; style.fill: "#e8f5e9"}
ak: "the rest: UNIQUE
constraints (alternate)" {width: 220; height: 80; style.fill: "#fff3e0"}
sk -> min
min -> pk
min -> ak
```

**Fig. 1.** Uniqueness alone is not candidacy — the set must be minimal. Of the minimal sets, one is promoted to PRIMARY KEY and the others remain enforced identifiers as UNIQUE constraints.

> [!warning] A nullable or non-minimal "key" is not a candidate key
> A column set that admits NULL cannot identify rows — SQL treats NULL as unknown, which is why PostgreSQL forces NOT NULL on primary key columns and why a candidate key with nullable members is a modeling bug, not a key. And a unique superset (say `email, name`) adds nothing once `email` alone is unique: minimality is part of the definition. Interviewees who call every indexed column a candidate key fail the follow-up [[How would you explain what a primary key is in relational databases]] asks next.

> [!tip] Interview answer
> A candidate key is a minimal column set that uniquely identifies a row — a potential primary key. Tables routinely have several: a surrogate id, an email, a national identifier. SQL enforces all of them: one becomes the PRIMARY KEY, the rest are declared UNIQUE, so the engine protects every identity the data actually has. The trap to avoid: minimality (a unique superset is not a candidate key) and nullability (a key with NULLs identifies nothing).

