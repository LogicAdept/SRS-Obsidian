<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SystemDesign/Performance #SRS

# When is a full table scan cheaper than using an index

> [!abstract] Short answer
> When the predicate matches a large fraction of rows, when the table is small, or when index hops would cost more than one sequential pass: a scan reads pages in bulk with one sweep, while an index path pays tree walks plus one random fetch per row. The planner compares those costs from statistics — which is why stale estimates flip the choice.

## The cost arithmetic behind the crossover

An index scan pays three costs: descending the tree, reading each matching row's heap location (random I/O per row unless the table is clustered), and rechecking predicates. A sequential scan pays one bulk pass, reading pages contiguously and applying the predicate per row. When the predicate matches, say, a quarter of a large heap table, the index path's per-row random fetches dominate and the sweep wins — the fraction where the flip happens depends on row width, clustering, and the engine's cost constants (random_page_cost versus seq_page_cost in PostgreSQL). SQLite's planner docs frame the same arithmetic in its simplest form: a scan is proportional to N, a lookup to log N plus per-row fetches, so tiny tables default to scans. The statistics feeding the comparison live in the catalogs, per [[What is selectivity and cardinality for indexes]].

```sql
-- matches 40% of rows: seq scan wins despite the index
EXPLAIN SELECT * FROM orders WHERE status = 'shipped';
-- Seq Scan on orders  (cost=0.00..35811.00 rows=400001 width=64)

-- matches 0.01%: index wins
EXPLAIN SELECT * FROM orders WHERE id = 8675309;
-- Index Scan using orders_pkey
```

**Listing 1.** Same table, opposite plans: the matched fraction decides, not index existence.

## The middle ground and the failure modes

Between plain index scan and seq scan sits the bitmap scan: index information selects pages, then the heap is read in physical order — PostgreSQL's middle path for moderate selectivity and OR-combination, per [[What is a bitmap index scan in SQL plans]]. Clustered storage shifts the crossover: InnoDB lookups by the clustered key fetch rows in place, and ordered ranges read contiguously, per [[What is the difference between clustered and non clustered database indexes]]. The failure mode is the planner computing this arithmetic from stale numbers: after a bulk load or mass delete, estimated rows no longer match actual, and the scan/index choice flips wrongly, per [[How do stale statistics hurt a query plan]] — diagnose with actual-versus-estimated rows, per [[How do you read EXPLAIN ANALYZE in PostgreSQL]]. And when the scan is genuinely right, forcing the index is the wrong fix; the sargability work in [[What is sargability in SQL]] applies to predicates that should seek but cannot.

> [!warning] "A full scan in the plan is always a problem" is the myth to kill
> Seq scans are frequently correct: low-selectivity predicates, small dimensions, analytics over most of the table. The actual red flags are scans on highly selective predicates, scans appearing after data growth with unchanged estimates, and scans where a sargable predicate exists but the plan says filter — each pointing to a different fix (index shape, statistics, predicate rewrite). Likewise "more indexes prevent scans" is backwards: bad indexes just add write cost, per [[When are database indexes a bad idea]].

> [!tip] Interview answer
> When the predicate matches a large fraction of rows, the table is small, or random per-row fetches would dominate, one bulk sequential pass is cheaper than index positioning plus row hops — the planner compares those costs from statistics, with bitmap scans as the middle ground at moderate selectivity. If the choice looks wrong, the first suspect is stale statistics, the second the predicate's sargability, not the absence of an index.
