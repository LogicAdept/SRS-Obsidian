<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# How do you read EXPLAIN ANALYZE in PostgreSQL?

> [!abstract] Short answer
> EXPLAIN shows the estimated plan; EXPLAIN ANALYZE executes it and annotates every node with actual time, rows and loops. Read it bottom-up per subtree, compare estimated versus actual rows at each node, find the nodes consuming the most time, and add BUFFERS to see page traffic. It runs the query for real — on writes use EXPLAIN ANALYZE inside a rollback.

## The workflow

```sql
BEGIN;
EXPLAIN (ANALYZE, BUFFERS) DELETE FROM events WHERE ts < '2020-01-01';
ROLLBACK;   -- the delete is undone; you keep the timing
```

**Listing 1.** The safe pattern for DML; plain SELECT needs no wrapping.

Read the output: the plan is a tree printed top-down, but time is spent in leaves; sum `actual time` across `loops` (the shown time is per loop). Mismatch between `rows=` (estimated) and actual rows at a node is the smoking gun of bad statistics. `Rows Removed by Filter` counts rows the node read and rejected ([[What is Index Cond versus Filter in EXPLAIN]]). `Heap Fetches` judges index-only scans ([[What is Heap Fetches in an EXPLAIN plan]]).

```d2
tree: "Plan tree" {width: 160; height: 60}
node: "Per node\nestimated rows vs actual rows\nactual time x loops" {width: 340; height: 80}
buf: "BUFFERS\nshared hit/read, temp read/written" {width: 340; height: 80}
verdict: "Slowest subtree +\nworst misestimate =\nyour next action" {width: 330; height: 90}
tree -> node -> verdict
tree -> buf -> verdict
```

**Fig. 1.** Three numbers decide the diagnosis: time, row misestimates, buffer traffic.

## What each anomaly suggests

- Huge `Rows Removed by Filter` on a Seq Scan — needs an index ([[Why might PostgreSQL choose a sequential scan instead of an index]]).
- `actual rows` off by orders of magnitude — stale or absent statistics; run ANALYZE ([[How do stale statistics hurt a query plan]]).
- `temp read/written` in BUFFERS — sorts or hashes spilling; work_mem candidate ([[What are shared_buffers and work_mem in PostgreSQL]]).
- Nested loop with millions of inner iterations — misestimated outer rows flipped the join.

> [!warning] ANALYZE overhead and plan mutation
> EXPLAIN ANALYZE really executes: full cost paid, triggers fired (for writes), and repeated runs may take different plans as caches warm. A cold first run can mislead; look at a couple of runs before concluding. And never EXPLAIN ANALYZE an UPDATE without the BEGIN/ROLLBACK wrapper unless you want the change committed.

> [!tip] Interview answer
> I read EXPLAIN ANALYZE by walking the tree bottom-up, comparing estimated versus actual rows to spot misestimates, summing actual time times loops to find the expensive subtree, and enabling BUFFERS to see page and temp traffic. On write queries I wrap it in a rolled-back transaction. Misestimated rows plus the heaviest node usually name the fix directly.
