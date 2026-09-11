<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes/Functional #SRS

# What is an expression index in PostgreSQL?

> [!abstract] Short answer
> An expression index (functional index) indexes the result of a function or expression over columns instead of raw column values, for example `lower(email)` or `(payload->>'status')`. The planner matches it when the query contains the same expression, which is the standard cure for "my WHERE clause wraps the column in a function and the index is ignored".

## Mechanism

```sql
CREATE INDEX users_email_lower_idx ON users ((lower(email)));
CREATE INDEX orders_unshipped_idx ON orders ((due_date - interval '2 days'));
SELECT * FROM users WHERE lower(email) = 'ana@example.com';  -- uses the index
```

**Listing 1.** The indexed expression must be written identically (modulo constant folding); wrapping the column in `lower()` in the query is exactly what makes this index usable rather than harmful.

Internally the index stores the expression's result as a virtual column with a regular operator class, so it can be B-tree, GIN, GiST, and so on. Statistics are collected for the expression, improving row estimates — the documentation notes an expression index is also the way to get planner statistics for a function's selectivity.

```d2
raw: "WHERE lower(email) = x\nagainst B-tree on (email)" {width: 330; height: 80}
expr: "WHERE lower(email) = x\nagainst B-tree on ((lower(email)))" {width: 340; height: 80}
scan: "Seq Scan: function defeats the index" {width: 320; height: 70}
idx: "Index Scan on expression" {width: 260; height: 60}
raw -> scan
expr -> idx
```

**Fig. 1.** Same query text, two outcomes: the index must be over the expression the query applies.

## Typical uses

- Case-insensitive lookups: `lower(col)` (or a citext column instead).
- JSON accessors: `(payload->>'sku')` with a B-tree, or a GIN over the whole document for containment ([[How do you index JSONB in PostgreSQL]]).
- Computed keys like `(a + b)` or date truncation `(created_at::date)`.
- Uniqueness over a normalized value: `CREATE UNIQUE INDEX ON users ((lower(email)));` — case-insensitive unique email.

## Related pitfalls

A general mechanism with the same symptom — index silently unused — is implicit type conversion, covered in [[How does implicit type conversion hide an index]]. If the expression includes `VOLATILE` functions it cannot be used in an index-scan condition at all; volatility categories matter for what the optimizer may assume ([[What are IMMUTABLE STABLE and VOLATILE functions in PostgreSQL]]).

> [!warning] The expression in the query must match, character for concept
> `WHERE lower(email) = 'x'` uses the index on `lower(email)`; `WHERE email = 'x'` does not, and `WHERE lower(email::text) = 'x'` may not if casts differ. The planner does not "reverse" the function; it matches expressions.

> [!tip] Interview answer
> An expression index stores the result of a function or expression — lower(email), a jsonb accessor, date truncation — instead of the raw column. It turns "function in WHERE defeats the index" into a fast path, gives the planner statistics for that expression, and can enforce unique-on-expression constraints. The query must contain the same expression for the planner to use it.
