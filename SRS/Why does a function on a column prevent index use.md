<!--
reps: 0
priority: 0
-->
#Databases/Indexes/Functional #SRS

# Why does a function on a column prevent index use

> [!abstract] Short answer
> The index stores the column's raw values in sorted order. A function applied to the column — YEAR(created_at), LOWER(email), col::int — asks for a range of transformed values that the index never stored, so the engine cannot seek and must compute the expression for every row. The fixes are to rewrite the predicate as a range over the raw column, or to index the expression itself.

## The mechanism

A B-tree seek works because the predicate narrows a contiguous run of stored keys. `created_at >= '2026-01-01' AND created_at < '2027-01-01'` is such a run; `WHERE EXTRACT(YEAR FROM created_at) = 2026` is not — the years 2026 live at many separate offsets of the timestamp order, and the index contains no year values to compare against. The planner therefore sees a predicate it cannot bound and either scans the table, evaluating the function per row, or scans the index fully. PostgreSQL's documentation on expression indexes names this directly: the index does not get used because the query predicate must match the indexed expression, and an index on the expression makes the query indexable.

```sql
-- scan: function on the column
SELECT * FROM events WHERE EXTRACT(year FROM created_at) = 2026;

-- seek: same semantics as a range over raw values
SELECT * FROM events
WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01';

-- seek via expression index when you truly need the function form
CREATE INDEX idx_events_year ON events ((EXTRACT(year FROM created_at)));
SELECT * FROM events WHERE EXTRACT(year FROM created_at) = 2026;
```

**Listing 1.** Three forms of the same query: one scans, one seeks after rewriting, one seeks after indexing the expression.

## The standard fixes and their trade-offs

Rewriting to a range over the raw column is free and portable — prefer it whenever possible, and it composes with partition pruning and the ordered scans in [[How do you avoid a sort with an index]]. The expression index costs extra storage and write time and must match the query's expression exactly (same function, same arguments, same cast), which is the definition-level nuance in [[What is an expression index in PostgreSQL]]. For case-insensitive matching the ecosystem answer is citext or a nondeterministic collation rather than hand-written LOWER everywhere, per [[How do you implement case-insensitive search efficiently]]. And remember the decision still belongs to the planner: an indexable predicate on a low-selectivity value will still scan, per [[What is sargability in SQL]].

> [!warning] "Non-sargable predicate forces a full table scan" is overstated
> The engine can still use the index for other clauses of the query, can do an index-only scan if the predicate columns are covered, or can pick the index scan for ordering and filter afterwards. The precise claim is that this predicate cannot seek; the plan may still touch the index for other reasons. Conversely, rewriting the predicate does not guarantee an index use if selectivity is poor.

> [!tip] Interview answer
> Functions on the column break seeking because the index holds raw, sorted values and the predicate now describes a range of transformed values — the engine would have to evaluate the function per row. Fix by rewriting to a range over the raw column, or create an expression index whose definition matches the query exactly. That is the same idea behind LOWER(email) needing an index on lower(email) or citext.
