<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# How do you decide which database indexes to create

> [!abstract] Short answer
> Work backward from measured queries, not from tables: capture the hot predicates and sorts, index the selective access paths with composite order following equality-then-sort, prefer covering when it removes heap hops, verify with plans, and keep auditing so unused or write-costly indexes get dropped. One index per frequent query shape beats a column-per-index scatter.

## The workflow that survives review

Start from evidence: slow query logs, pg_stat_statements, or EXPLAIN on the endpoints that matter. For each hot query, extract the predicate shape (equality columns, range columns, sort columns) and build the minimal index that serves it: equality columns first, range/sort column last, per [[How do you optimize ORDER BY with a filter]] and [[What is the leftmost prefix rule for composite indexes]]; add INCLUDE payload when the query can then skip the heap, per [[How would you explain Covering index]]; reach for partial indexes when a stable filter (status = 'open') defines the hot subset, per [[What is a partial index in PostgreSQL]]. MySQL's optimization manual gives the same guidance in one line: create a small number of concatenated indexes rather than a large number of single-column indexes, and prefer covering so the query avoids the table entirely.

```sql
-- 1) find the actual hot queries
SELECT query, calls, mean_exec_time
FROM pg_stat_statements ORDER BY mean_exec_time * calls DESC LIMIT 20;

-- 2) index the shape, not the table
CREATE INDEX idx_orders_cust_created ON orders (customer_id, created_at DESC);

-- 3) verify the plan, then keep auditing
EXPLAIN ANALYZE SELECT ... ;
SELECT indexrelname, idx_scan FROM pg_stat_user_indexes
WHERE relname = 'orders' AND idx_scan = 0;
```

**Listing 1.** Evidence, one index per shape, plan verification, and the unused-index audit loop.

## The counterweight: write costs and diminishing returns

Every index taxes every write touching its columns, and the planner's overhead grows with index count, so the decision is a budget: index the access paths with real frequency and selectivity, and decline speculative ones — the failure mode of indexing everything is its own card in [[What goes wrong with indexing every field combination for flexible search]], and the situations where indexing is a net loss are in [[When are database indexes a bad idea]]. Statistics freshness closes the loop, because plans justify indexes only under honest estimates, per [[How do stale statistics hurt a query plan]]; and the selection criteria lean on selectivity concepts from [[What is selectivity and cardinality for indexes]]. Vendor guidance is explicit about the multi-query case: PostgreSQL's docs walk the two-columns-two-workloads trade (separate indexes plus bitmap combination versus multicolumn plus skip scan), per [[How do you combine several indexes in one query]].

> [!warning] "Index every column in every WHERE" is the anti-workflow
> The scattergun rule produces write-heavy tables with dozens of near-unused indexes and no plan improvements where it matters. The subtler version of the same mistake: creating single-column indexes for a query that needs a composite, so the planner can only fall back to bitmap combination — legal but usually weaker than the purpose-built index. The index set is derived from measured query shapes, and anything not justified by a real plan gets dropped.

> [!tip] Interview answer
> I start from measured hot queries, not schema. For each, I build the minimal index matching its shape — equality columns first, sort column last, INCLUDE or partial variants when they shrink the work — and I verify with EXPLAIN that the plan uses it. Then I keep the loop honest: audit unused indexes, watch write amplification, and drop anything that no plan justifies. Few well-shaped composite indexes beat a column-per-index scatter.
