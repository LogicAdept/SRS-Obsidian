<!--
reps: 0
priority: 0
-->
#Databases/Indexes/Functional #Databases/SQL #SRS

# How do you implement case-insensitive search efficiently

> [!abstract] Short answer
> Pick one mechanism and index it: an expression index on lower(email) so WHERE lower(email) = lower($1) seeks, the citext type which lowercases under the hood, or a nondeterministic collation for case- and accent-insensitive equality. MySQL needs nothing special — its default collations already compare case-insensitively — but the naive LOWER-on-a-plain-index form never uses the index.

## PostgreSQL: three indexed options

The naive form fails by construction: `WHERE lower(email) = ?` cannot seek an index that stores raw email values, per the mechanism in [[Why does a function on a column prevent index use]]. The first fix is an expression index: `CREATE INDEX ON users (lower(email))` — the planner matches the query's expression to the indexed expression. The second is citext, a contrib type whose comparisons internally apply lower, so `WHERE email = 'Larry'` matches a stored 'larry' without any expression in the query, and a citext primary key enforces uniqueness case-insensitively — something a plain text UNIQUE index does not. The third, which PostgreSQL's citext docs themselves recommend considering, is a nondeterministic collation (ICU-based), handling case and accent insensitivity with correct Unicode semantics. For pattern matching with wildcards, pg_trgm's GIN index supports ILIKE efficiently, per [[How does a trigram index help SQL search]].

```sql
CREATE INDEX idx_users_email_l ON users (lower(email));
SELECT * FROM users WHERE lower(email) = lower('Larry@example.com');

ALTER TABLE users ALTER COLUMN email TYPE citext;
SELECT * FROM users WHERE email = 'Larry@example.com';  -- seeks
```

**Listing 1.** Either the indexed expression or the citext type makes the comparison seekable.

## MySQL and the portability trap

MySQL's default collations such as utf8mb4_0900_ai_ci are already case- and accent-insensitive, so `WHERE email = 'Larry@...'` uses the ordinary B-tree index and matches case-insensitively — no LOWER and no special index needed. The portable rule is therefore: know your engine's collation model before writing LOWER anywhere; sprinkling lower() into MySQL queries is harmless but pointless, while omitting it in PostgreSQL silently disables the index. Uniqueness differs too: a citext column or a case-insensitive collation enforces case-insensitive uniqueness, whereas PostgreSQL's default text UNIQUE is case-sensitive — the classic source of duplicate-email bugs, adjacent to the constraint-vs-index layering in [[Is a primary key implemented as an index and why]].

> [!warning] Adding lower() to the query without changing the index does nothing
> The trap is "I made the query case-insensitive, now it's fast" — with a plain index on email, the query is both slower (per-row lower) and unindexed. The other half-trap: an expression index on lower(email) matches only queries that apply the identical lower(email) form; upper(email) or a different normalization will not match it. ILIKE also needs trigram support rather than the plain B-tree, as PostgreSQL's pattern-matching notes explain.

> [!tip] Interview answer
> In PostgreSQL I make the comparison seekable: an expression index on lower(email), the citext type, or a nondeterministic ICU collation — each one makes equality both case-insensitive and indexed. MySQL's default collations already compare case-insensitively, so a plain index suffices. The mistake to avoid is lower() on the column side of a plain-indexed query, which guarantees a scan.
