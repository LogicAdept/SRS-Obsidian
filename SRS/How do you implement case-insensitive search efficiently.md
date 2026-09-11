<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How do you implement case-insensitive search efficiently?

> [!abstract] Short answer
> Case-insensitive search has three tiers: (1) **case-insensitive LIKE** — SQLite's default for ASCII; PostgreSQL needs `ILIKE` or `lower(col) = lower(?)`; (2) **case-insensitive indexes** — SQLite `COLLATE NOCASE`, PostgreSQL `citext` type or a `lower()` expression index — restoring index seeks for the insensitive comparison; (3) **full-text/collation-aware machinery** for Unicode-correct folding at scale ([[What is the difference between LIKE ILIKE and full-text search]], [[Why does a function on a column prevent index use]]).

The verified demo pins SQLite's quirk precisely: `LIKE 'alice%'` matches both 'Alice' and 'ALICE' (default LIKE is case-insensitive for ASCII letters only), `GLOB 'alice%'` matches neither (always case-sensitive), and `lower(name) = lower('ALICE')` matches both but plans as a scan — the function-on-column form is the portable-but-unindexed fallback. The Unicode caveat is the senior detail: SQLite's ASCII-only folding means `LIKE 'é%'` will not match 'École' — case folding for non-ASCII requires lower() with proper locale handling or application-side normalization. PostgreSQL's documented answers: `ILIKE` operator (LIKE semantics, case-insensitive, still index-hostile), the `citext` extension type (stores and compares case-insensitively — indexes work transparently), and functional indexes on `lower(col)` paired with `WHERE lower(col) = lower(?)` — the standard production recipe ([[How does implicit type conversion hide an index]]). SQLite's tier-2 is `COLLATE NOCASE` on the column definition or index, which makes equality *and* the LIKE optimization seek case-insensitively ([[Why does LIKE with a leading wildcard not use a B-tree index]]). The design question to answer aloud: is case-insensitivity a *query* concern (ILIKE at the call site) or a *data* concern (citext/NOCASE storage)? Data-level folding simplifies every consumer; query-level keeps the original casing authoritative.

```sql
INSERT INTO customers (id, name, city) VALUES (7, 'ALICE', 'Rome');

SELECT name FROM customers WHERE name LIKE 'alice%' ORDER BY id;
-- Alice
-- ALICE
-- (SQLite LIKE: case-insensitive for ASCII)
SELECT name FROM customers WHERE name GLOB 'alice%';
-- (no rows: GLOB is always case-sensitive)
SELECT name FROM customers WHERE lower(name) = lower('ALICE') ORDER BY id;
-- Alice
-- ALICE
-- (works for any case, but the plan is a scan: function on column)
```

**Listing 1.** Verified on SQLite 3.53.1. Three spellings, two behaviors: default LIKE folds ASCII case, GLOB does not fold, and the lower() form folds everything at scan cost — the trade the three tiers navigate.

```d2
direction: right
t1: "LIKE / ILIKE
fold at query time
scan unless supported" {width: 200; height: 90}
t2: "NOCASE / citext /
lower() index
fold at storage or index" {width: 210; height: 90}
t3: "FTS machinery
Unicode folding, ranking" {width: 200; height: 90}
t1 -> t2 -> t3
```

**Fig. 1.** Case-insensitivity moves through three layers — query-time folding, folded storage or indexes, full text machinery — trading portability against index use and Unicode correctness.

> [!warning] ASCII-only folding breaks on real names — test with 'École', not 'alice'
> Engines' default folds cover a-z only; Turkish dotless i, German sharp s and accented initials all fall outside ASCII LIKE folding. For international data the choice is lower() with locale-aware collation, citext, or FTS — not bare LIKE ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> Three tiers: query-time folding — SQLite LIKE is ASCII-insensitive by default, PostgreSQL uses ILIKE or lower-equals, which works but scans; storage-or-index folding — COLLATE NOCASE in SQLite, citext or a lower() expression index in PostgreSQL — which restores seeks; and full-text machinery for Unicode-correct folding with ranking. My demo shows LIKE matching both Alice spellings, GLOB matching none, and lower() matching both at scan cost. The Unicode caveat I always add: ASCII folding stops at the alphabet's edge, so international data needs the second or third tier.
