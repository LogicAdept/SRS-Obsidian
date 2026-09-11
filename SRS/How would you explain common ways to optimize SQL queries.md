<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Relational/MySQL #Databases/Relational/PostgreSQL #Databases/Relational/Oracle #SystemDesign/Performance #SRS

# How would you explain common ways to optimize SQL queries?

> [!abstract] Short answer
> Organize by leverage: (1) make the access path right — indexes that match predicates and avoid functions or casts over indexed columns; (2) reduce the data — select only needed columns, filter early, paginate by keyset; (3) fix the shape — avoid correlated subqueries where a join or window works, keep ORs indexable; (4) keep statistics fresh so the optimizer is honest; (5) only then touch memory and server settings.

## The ladder

```d2
l1: "Access path\nindex matches WHERE/ORDER BY,\nno cast or function on the column" {width: 360; height: 100}
l2: "Less data\nprojected columns, early filters,\nkeyset pagination" {width: 320; height: 100}
l3: "Query shape\njoin vs correlated subquery,\nAND/OR rewrites, DISTINCT hygiene" {width: 340; height: 100}
l4: "Optimizer honesty\nfresh statistics, expression indexes\nfor computed predicates" {width: 340; height: 100}
l1 -> l2 -> l3 -> l4
```

**Fig. 1.** Escalating levels: each rung is cheaper than rearchitecting everything above it later.

## What each rung means concretely

- **Access path**: the WHERE shape decides usable indexes ([[How do you decide which database indexes to create]]); functions over columns need expression indexes ([[What is an expression index in PostgreSQL]]); implicit casts silently disable them ([[How does implicit type conversion hide an index]]); leading-wildcard LIKE needs trigram-class structures ([[How does a trigram index help SQL search]]).
- **Less data**: `SELECT *` defeats index-only scans ([[What is an index-only scan in PostgreSQL]]); OFFSET pagination re-reads everything ([[What is the difference between offset and cursor pagination]]).
- **Shape**: correlated subqueries rewrite into joins or window functions ([[How do you rewrite a correlated subquery for performance]], [[What is a correlated subquery and why can it be slow]]); OR across columns becomes a bitmap union in PostgreSQL ([[How does OR across columns affect index use]]).
- **Optimizer honesty**: ANALYZE after bulk changes; extended statistics for correlated columns ([[How do stale statistics hurt a query plan]]).
- **Engine-side memory and plans** come last: work_mem, joins, plan reading ([[How do you read EXPLAIN ANALYZE in PostgreSQL]]).

## The discipline that makes it work

One change per iteration, measured before and after with the actual plan — cost estimates, actual rows, buffers ([[What is Index Cond versus Filter in EXPLAIN]] names the counters that matter). An optimization without a re-measurement is a hypothesis that will outlive its welcome; a portfolio of three index adds plus a query rewrite plus a memory bump applied together tells you nothing about which mattered. Keep the regression risk visible: every added index taxes writes ([[How do you decide which database indexes to create]]), so the loop ends with removing what did not pay for itself.

The same ladder applies across engines; the vocabulary differs — MySQL has its own optimizer hints and index rules ([[How would you explain MySQL replication strategies]] covers the replication side of that ecosystem), Oracle adds plan stability mechanisms, and analytical workloads change the rules entirely ([[What is the difference between PostgreSQL and ClickHouse]]).

> [!warning] "Add an index" is the most overused optimization
> An index that does not match the query's operator shape adds write cost and changes nothing; a fifth index on the same hot table slows every write ([[What goes wrong with indexing every field combination for flexible search]]). Measure with the plan, verify the Index Cond, and remember that fixing the query text is often free where the index is not.

The same ladder reads differently per engine: PostgreSQL gives you bitmap scans for ORs and expression indexes for functions ([[What is an expression index in PostgreSQL]]); MySQL leans on covering indexes and optimizer switches; Oracle on hints and statistics stability. What transfers everywhere is the sequence — access path, data volume, shape, statistics, memory — because every cost-based optimizer rewards the same kind of honesty about what the query actually needs.

And the sequence has an order for a reason: shape changes can invalidate the index you just added; statistics changes can flip the join algorithm the new shape relies on. Presenting the ladder in order, measured at each rung, is the difference between an optimization story and an optimization anecdote.

> [!tip] Interview answer
> I present it as a ladder: first the access path — indexes matching the predicates, no functions or casts breaking them; then reducing data touched — projections, early filters, keyset pagination; then query shape — joins over correlated subqueries, indexable ORs; then statistics so the optimizer tells the truth; and only after that server memory. Each step is verified with the actual plan, not intuition.
