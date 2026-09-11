<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL #SRS

# What is CTE materialization in PostgreSQL?

> [!abstract] Short answer
> A CTE can be computed once and stored (materialized, pre-PostgreSQL-12 behavior for every CTE) or folded into the parent query and re-planned inline (inlining, the PostgreSQL-12+ default when the CTE is non-recursive, side-effect-free, and referenced exactly once). MATERIALIZED and NOT MATERIALIZED keywords override the decision. The choice changes whether predicates push down into the CTE.

## The rule since PostgreSQL 12

```sql
WITH big AS (
  SELECT * FROM events WHERE type = 'click'
)
SELECT * FROM big WHERE ts > now() - interval '1 hour';
-- inlined by default: ts filter reaches the scan, index usable

WITH big AS MATERIALIZED (
  SELECT * FROM events WHERE type = 'click'
)
SELECT * FROM big WHERE ts > now() - interval '1 hour';
-- materialized: big computed fully, then filtered again
```

**Listing 1.** Same text, two plans: inlining lets the outer predicate and indexes apply inside the CTE; materialization builds the full intermediate result first.

The optimizer inlines when the CTE is non-recursive, contains no volatile functions, and the parent references it once. Referenced twice, it is materialized by default (computing twice could cost more). NOT MATERIALIZED forces inlining even with multiple references, risking duplicate computation ([[How do you implement a recursive query in PostgreSQL]] — recursive CTEs are always materialized).

```d2
cte: "WITH query" {width: 200; height: 60}
inl: "Inlined (default, 1 use, pure)\nouter predicates push down\nindexes apply inside" {width: 360; height: 100}
mat: "Materialized\ncomputed once into a tuplestore\nopaque to outer predicates" {width: 360; height: 100}
cte -> inl: "NOT MATERIALIZED / default"
cte -> mat: "MATERIALIZED / multi-use / volatile"
```

**Fig. 1.** The decision fork and what each branch means for pushdown.

## Why materialization is still useful

- You want the CTE computed exactly once even though it is referenced several times (expensive aggregate, sampled set).
- Old plans expected the pre-12 fence: materialization prevented predicate pushdown; sometimes the "worse" plan is the safe one for volatility or permission reasons (security-barrier views behave similarly).
- Debugging: materialize once and reuse in several exploratory queries in the same statement.

## Diagnosing

When a wrapped CTE query ignores an index, check the plan: an inlined CTE disappears into the parent nodes; a materialized one appears as a CTE Scan with its own sub-plan, and outer filters show as Filters on the scan — the pushdown blocked ([[How do you read EXPLAIN ANALYZE in PostgreSQL]], [[Why might PostgreSQL choose a sequential scan instead of an index]]).

> [!warning] Pre-PostgreSQL-12 knowledge inverts the advice
> Before 12, every CTE was an optimization fence; old advice says "unwrap CTEs for performance". Since 12 the default is inline, and the modern trap is the opposite: MATERIALIZED typed by habit blocks predicate pushdown and index use. Version context is part of the answer — and per-statement data-modifying CTEs (INSERT ... RETURNING in WITH) have their own visibility rules.

> [!tip] Interview answer
> Since PostgreSQL 12 a plain CTE is inlined into the parent when it is non-recursive, pure, and used once — predicates push down, indexes work. MATERIALIZED forces a one-shot tuplestore (useful for expensive multi-referenced CTEs), NOT MATERIALIZED forces inlining. The symptom of accidental materialization is a CTE Scan node with outer filters that never reach the index.
