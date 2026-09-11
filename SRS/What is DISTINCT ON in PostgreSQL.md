<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL #SRS

# What is DISTINCT ON in PostgreSQL?

> [!abstract] Short answer
> A PostgreSQL extension of DISTINCT: `SELECT DISTINCT ON (expr, ...)` keeps only the first row of each group of rows that share the given expressions — "top-1 per group" in one clause. The first row is undefined unless ORDER BY starts with the same expressions, so the production idiom is DISTINCT ON (group) plus ORDER BY group, ordering-column, which is exactly a window-function alternative.

## The canonical query

```sql
SELECT DISTINCT ON (customer_id)
       customer_id, id, created_at, total
FROM orders
ORDER BY customer_id, created_at DESC;
-- last order per customer
```

**Listing 1.** Groups by customer_id; within each group the DESC date ordering puts the wanted row first; DISTINCT ON keeps it and drops the rest.

Rules from the documentation: the DISTINCT ON expressions must match the leftmost ORDER BY expressions; the first row of each group is unpredictable without that ORDER BY; extra ORDER BY terms decide which row wins inside the group.

```d2
rows: "All rows sorted by\n(customer_id, created_at DESC)" {width: 330; height: 80}
grp: "Group boundaries:\nchange of customer_id" {width: 320; height: 80}
keep: "Keep first row of each group\nDROP the rest" {width: 320; height: 80}
rows -> grp -> keep
```

**Fig. 1.** It is a sort plus a per-group first-row filter — no aggregation semantics involved.

## Alternatives and tradeoffs

- Window functions: `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) = 1` — standard SQL, more flexible (top-N, ties, multiple ranks), heavier to read ([[What are window functions in PostgreSQL]]).
- LATERAL join against a grouped driver — best when you need several aggregates per group or index-driven retrieval ([[What is a LATERAL join in PostgreSQL]]).
- DISTINCT ON wins on brevity and on plans that can use an index matching (customer_id, created_at) to avoid the sort ([[How do you avoid a sort with an index]]).

Since it is a PostgreSQL extension, portability is the cost; MySQL and Oracle answer the same need with window functions or their own idioms — a difference worth naming in cross-engine discussions ([[What is the difference between PostgreSQL and MySQL]]).

> [!warning] Unpredictable first row without ORDER BY
> DISTINCT ON (x) without ORDER BY x, tiebreaker returns an arbitrary row of each group — valid SQL, wrong results when someone later assumes determinism. The second classic bug: DISTINCT ON expressions that do not match the leftmost ORDER BY expressions are rejected by the parser, but a matching-yet-ambiguous ORDER BY still yields unstable choices when ties exist.

> [!tip] Interview answer
> DISTINCT ON is PostgreSQL's top-1-per-group: it sorts by the grouping expressions plus your preference column and keeps the first row of each group. It must pair with a matching leftmost ORDER BY to be deterministic, and the same result is expressible with ROW_NUMBER windows or LATERAL joins — DISTINCT ON is the concise, index-friendly, non-portable option.
