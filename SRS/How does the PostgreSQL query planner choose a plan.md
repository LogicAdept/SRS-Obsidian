<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# How does the PostgreSQL query planner choose a plan?

> [!abstract] Short answer
> Cost-based optimization: the planner enumerates candidate plans (scan methods, join order, join algorithm), estimates the cost of each from table statistics — row counts, selectivity, correlation — multiplied by hard-coded cost constants, and picks the cheapest. The numbers come from ANALYZE-maintained catalogs and per-operation cost models, not from running the query.

## The inputs

- Table sizes and row counts (`pg_class.reltuples`, refreshed by VACUUM/ANALYZE, scaled to current file size).
- Column statistics in `pg_statistic`: most-common values, histograms, correlation of physical order — collected by ANALYZE from a random sample ([[How do stale statistics hurt a query plan]]).
- Cost constants: `seq_page_cost` 1.0, `random_page_cost` 4.0 (tuned down for SSD), `cpu_tuple_cost` 0.01, plus `effective_cache_size` as a hint of OS cache.
- Setup: enabled-path flags (`enable_seqscan`, `enable_indexscan`...), join-collapse limits.

```d2
stats: "Statistics\nreltuples, MCV, histograms,\ncorrelation" {width: 330; height: 90}
consts: "Cost constants\nseq_page_cost, random_page_cost,\ncpu costs, cache size" {width: 350; height: 90}
enum: "Enumerate plans\nscans x join order x join type" {width: 330; height: 80}
pick: "Cheapest estimated plan\n(never measured)" {width: 300; height: 70}
stats -> enum
consts -> enum
enum -> pick
```

**Fig. 1.** The planner is an estimator: everything is predicted from statistics and constants before execution starts.

## What it decides

For each query block: which scan per table (Seq, Index, Index Only, Bitmap — [[What scan types exist in a PostgreSQL query plan]]), in which order to join, and with which algorithm (nested loop with inner index scan for small driven sets, hash join for large unsorted inputs, merge join for pre-sorted data). The generic plan-making background is in [[What is a query plan in a relational database]]; reading the result is [[How do you read EXPLAIN ANALYZE in PostgreSQL]].

## Why estimates go wrong

Correlated columns (the planner assumes independence — fixed with CREATE STATISTICS), functions over columns (no statistics without an expression index), stale statistics after bulk changes, and non-uniform distributions beyond the MCV list. Prepared statements may even switch to a generic plan after five custom executions when the custom plans stop looking cheaper — the first five runs use literal values, then a one-size-fits-all plan takes over if it does not look worse (the plan_cache_mode setting can force either behavior).

## The output is a tree, not a verdict

The plan is a tree of nodes, each with estimated startup/total cost, rows and width; children execute before parents. Reading it well is a separate skill ([[How do you read EXPLAIN ANALYZE in PostgreSQL]]), and the node zoo starts with the four table-access types ([[What scan types exist in a PostgreSQL query plan]]).

> [!warning] The planner optimizes the estimate, not the truth
> A plan is "best" in the model of the world built from sampled statistics. A misestimated 10 rows versus 10 million rows flips nested loop into hash join and can be slower by orders of magnitude — and EXPLAIN without ANALYZE will happily show you the confident wrong number ([[How do you debug a slow PostgreSQL query]]).

> [!tip] Interview answer
> The planner is a cost-based optimizer: it enumerates scan and join combinations, prices each using catalog statistics and cost constants, and takes the minimum. Row estimates come from ANALYZE samples — MCV lists, histograms, correlation — so stale or missing statistics are the number-one cause of bad plans, followed by correlated columns that CREATE STATISTICS can fix.
