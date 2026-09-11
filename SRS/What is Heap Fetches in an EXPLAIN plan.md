<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes/Covering #SRS

# What is Heap Fetches in an EXPLAIN plan?

> [!abstract] Short answer
> `Heap Fetches` is the EXPLAIN (ANALYZE) counter on Index Only Scan nodes: how many times the executor had to visit the heap because the visibility map could not prove the row visible. It is the honest measure of whether an index-only scan is actually saving you I/O — zero is the goal, thousands mean the "index-only" plan is reading the heap almost per row.

## Where the number comes from

An index-only scan reads candidate rows from the index, then must guarantee MVCC visibility ([[What is MVCC in PostgreSQL]]). Visibility exists only in heap tuples, so the scan consults the visibility map per page: all-visible pages pass without a heap visit; anything else produces heap fetches — one per row whose page is not marked. See [[What is an index-only scan in PostgreSQL]] for the mechanism and [[What is a dead tuple in PostgreSQL]] for why churn breaks the bits.

```d2
good: "VACUUMed table\nall-visible pages\nHeap Fetches ~ 0" {width: 300; height: 80}
bad: "Just loaded / heavily updated\nbits cleared\nHeap Fetches ~= rows" {width: 330; height: 80}
fix: "VACUUM (or autovacuum pass)\nresets bits to all-visible" {width: 330; height: 80}
bad -> fix -> good
```

**Fig. 1.** Heap Fetches is a vacuum-state metric as much as an index metric.

## How to act on it

- Fetches high and table is write-hot: expected; consider whether the covering index still pays for its write cost.
- Fetches high and the table is quiet: autovacuum is not reaching the table — check `last_autovacuum` and thresholds ([[What is autovacuum in PostgreSQL]]).
- Comparing plans over time: Heap Fetches is one of the few plan numbers that reflects table maintenance, not just the query shape ([[How do you debug a slow PostgreSQL query]]).
- Trend, not point: after a bulk load the number is huge and self-heals with the next vacuum; a chronically rising baseline on a quiet table means maintenance is falling behind ([[How do you monitor database health and load]]).
- When comparing candidate indexes, remember a covering index that mostly runs with high Heap Fetches is paying write cost for little read benefit — an ordinary narrower index may serve better ([[What is the difference between a composite index and an INCLUDE covering index]]).

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT user_id, status FROM orders WHERE user_id = 42;
-- Index Only Scan ...  Heap Fetches: 4321  <- investigate vacuum
```

**Listing 1.** Read Heap Fetches together with BUFFERS: `shared hit/read` shows the actual page traffic the fetches caused.

> [!warning] The node name is a promise, the counter is the delivery
> An "Index Only Scan" with Heap Fetches in the tens of thousands can be slower than a plain Index Scan. Plans chosen by cost estimation before the run cannot know future fetch counts; measure with ANALYZE output, not the plan label.

> [!tip] Interview answer
> Heap Fetches counts heap visits an index-only scan still had to make because visibility-map bits were not set — the gap between the plan's name and its real cost. Zero after a good vacuum; per-row fetches on freshly written pages. If it is chronically high on a quiet table, the fix is vacuum tuning, not a new index.
