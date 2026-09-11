<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS

# Why might PostgreSQL choose a sequential scan instead of an index?

> [!abstract] Short answer
> Because by its estimates it is cheaper: a seq scan reads pages sequentially at low cost per page, while an index path pays random-access costs per row plus index descent. It wins when the query returns a large fraction of the table, when statistics are stale or missing, when an operator or implicit cast cannot use the index, or when the table is small enough that descending an index costs more than reading everything.

## The legitimate reasons

1. **Selectivity** — fetching 20 percent of a table via random heap visits loses to one sequential pass; the cost model prices this ([[How does the PostgreSQL query planner choose a plan]]).
2. **Correlation** — if physical row order matches the index, index reads are nearly sequential; if not, each row is a random page.
3. **Small table** — a few pages fit in one or two reads anyway.
4. **No usable index operator** — `LIKE '%x%'` on a B-tree, or a function over the column ([[What is the difference between LIKE ILIKE and full-text search]], [[What is an expression index in PostgreSQL]]).
5. **Type mismatch** — implicit casts defeat the operator class ([[How does implicit type conversion hide an index]]).

## The fixable reasons

```sql
ANALYZE orders;                          -- stale statistics: refresh
SELECT * FROM pg_stats WHERE tablename = 'orders';  -- inspect estimates
SET enable_seqscan = off;                -- debugging only: what the index plan costs
```

**Listing 1.** First diagnose, then fix: refresh statistics, add or repair the index ([[How do you decide which database indexes to create]]), or rewrite the predicate. `enable_seqscan = off` is a diagnostic tool, never a production setting — it biases costs, not correctness ([[How do you read EXPLAIN ANALYZE in PostgreSQL]]).

```d2
est: "Estimated rows" {width: 200; height: 60}
frac: "Large fraction\nseq scan wins" {width: 260; height: 70}
bad: "Stale stats / cast / function\nindex unusable" {width: 300; height: 80}
fix: "ANALYZE, better index,\nor accept the seq scan" {width: 320; height: 80}
est -> frac
est -> bad -> fix
```

**Fig. 1.** Two branches: the planner is right (big fraction) or the index was disqualified (fixable).

> [!warning] A seq scan on a huge table with a selective predicate is never "the planner being weird"
> If EXPLAIN says Seq Scan and `Rows Removed by Filter` is enormous, one of: statistics never ran, the predicate is not indexable as written, or the index does not exist on this replica/schema. Check those before blaming cost constants — and never "fix" it by disabling seqscan cluster-wide.

> [!tip] Interview answer
> The planner picks seq scans when the model says random index reads cost more than one sequential pass: big result fractions, poor physical correlation, tiny tables, or an index the predicate cannot use — stale stats, functions, casts. The workflow is ANALYZE, then verify indexability of the predicate, and treat enable_seqscan=off as a diagnostic only.
