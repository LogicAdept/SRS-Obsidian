<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> **PRIMARY KEY** = row identity: UNIQUE **plus NOT NULL**, at most one per table, and it is the key other tables reference. **UNIQUE** is just non-duplication: a table may carry many UNIQUE constraints, and — the interview point — NULLs are allowed *multiple times* in most engines, because NULL is not a value and no two NULLs are equal for the uniqueness test ([[What does NULL mean in SQL]]).

The verified demo shows the NULL hole concretely: two rows with NULL `slug` both insert fine under UNIQUE; the duplicate `slug` fails. PostgreSQL behaves identically (multiple NULLs under UNIQUE; the standard's own semantics); SQL Server famously deviates — a unique index treats NULLs as equal and allows only one (filtered indexes are the documented workaround for "unique when not null"). SQLite's second demo twist is engine-specific gold: `INTEGER PRIMARY KEY` is a rowid alias, so inserting NULL *auto-assigns* the next rowid rather than failing — while PostgreSQL rejects a NULL PK insert outright ([[Can the same primary key value appear in two rows of one table]]). Design guidance: PK for identity (surrogate `id` or natural key), UNIQUE for business invariants (IBAN, slug, email) — including **composite UNIQUE** for "unique per group" rules like `(tenant_id, email)` that a single-column UNIQUE cannot express. Multiple NULLs matter in practice: a UNIQUE email column with many "no email yet" NULL rows is legal — and NULL-empty-string conflation is the bug hiding next to it ([[How do you forbid NULL or empty values in a database column]]).

```sql
CREATE TABLE tags (id INTEGER PRIMARY KEY, slug TEXT UNIQUE);
INSERT INTO tags VALUES (1, 'sql');
INSERT INTO tags VALUES (2, NULL);
-- (ok: first NULL under UNIQUE)
INSERT INTO tags VALUES (3, NULL);
-- (ok: second NULL too -- NULLs are not equal for uniqueness)
INSERT INTO tags VALUES (4, 'sql');
-- ERROR: UNIQUE constraint failed: tags.slug
INSERT INTO tags (slug) VALUES ('auto');
-- (ok in SQLite: INTEGER PK is a rowid alias, NULL id auto-assigns)
```

**Listing 1.** Verified on SQLite 3.53.1. Multiple NULLs coexist under UNIQUE; the real duplicate fails; the NULL PK insert auto-assigns a rowid instead of erroring — SQLite's documented rowid-alias behavior, distinct from the standard's "no NULL PK".

```d2
direction: right
pk: "PRIMARY KEY
unique + not null
one per table" {width: 190; height: 90}
uq: "UNIQUE
duplicates rejected
NULLs pass (most engines)" {width: 230; height: 90}
r: "identity vs business invariant" {width: 230; height: 70}
pk -> r
uq -> r
```

**Fig. 1.** Both constraints reject duplicates; only the PK also refuses NULL and claims the row's identity — UNIQUE constraints police business rules in plural.

> [!warning] Multiple NULLs can undermine the invariant the UNIQUE was meant to enforce
> "Every active subscription has a unique cancel token" fails if inactive rows carry NULL and two actives also carry NULL by an application bug. Where the invariant must hold even for missing values, add NOT NULL to the UNIQUE column, or use a partial/filtered unique index on the rows that matter ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> PRIMARY KEY is unique plus not-null, one per table, and it is the identity other tables reference; UNIQUE constraints only reject duplicate non-NULL values and you can have many. The sharp edge: most engines, including PostgreSQL and SQLite, allow multiple NULLs under UNIQUE because NULL never equals anything — SQL Server allows one. And SQLite's INTEGER PRIMARY KEY is a rowid alias, so a NULL insert auto-assigns. I use PK for identity and UNIQUE for business invariants, often composite, per-tenant ones.
