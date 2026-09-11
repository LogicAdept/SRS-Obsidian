<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# What is the difference between Nested Loop Hash Join and Merge Join

> [!abstract] Short answer
> Nested loop probes the inner side once per outer row — cheap when the outer is small and an index makes each probe a seek. Hash join builds an in-memory hash of one side and probes it with the other — the default for large, unordered inputs and equality joins. Merge join walks both sides in key order — nearly sorted-friendly, but it needs both inputs ordered, which indexes provide.

## Mechanism and when each wins

Nested loop is the oldest strategy: for each row of the outer input, find matching inner rows. Without an index that is O(N x M); with an index on the inner join column each probe is a seek, so a small outer over a huge indexed inner is fast and the plan streams with almost no memory. Hash join reads the (usually smaller) build side, hashes the join keys into buckets, then probes with the other side; it needs equality predicates and memory (or a spill), but it turns two large unordered scans into one pass each. Merge join consumes both inputs simultaneously in join-key order, so it is non-blocking and produces sorted output, but it must sort any input not already ordered — an index on the join keys replaces that sort. PostgreSQL's planner documentation describes these three strategies and their cost trade-offs, and MySQL exposes roughly the same split: it historically implemented only nested-loop-style joins (with Block Nested Loop/Hash variants in its executor) and shows them in EXPLAIN.

```d2
direction: right
nl: "Nested Loop\nsmall outer, indexed inner" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
hj: "Hash Join\nbig x big, equality, memory-bound" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
mj: "Merge Join\nboth inputs sorted, streams out sorted" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}```

**Fig. 1.** The three plans side by side: probe-per-row, build-and-probe, and synchronized ordered walks.

## Where indexes enter the picture

An index on the inner side converts nested loop from quadratic to linear-ish, which is why the FK-index advice in [[Why should you index foreign keys]] is not cosmetic: un-indexed FK columns push joins toward hash builds or seq scans. Merge join is effectively "two index range scans in lockstep" when both keys are indexed, connecting it to [[What is the leftmost prefix rule for composite indexes]] because the join keys must form a usable prefix. Reading the actual choice, with row estimates that explain why the planner picked it, is the EXPLAIN skill in [[How do you read EXPLAIN ANALYZE in PostgreSQL]].

> [!warning] "Hash join is always fastest" and "nested loop is always bad" are both false
> For a 50-row outer into a 100-million-row indexed inner, nested loop crushes hash join because the build itself may spill and the probe touches everything. For two 10-million-row unordered inputs, nested loop is catastrophic without an index. The planner compares estimated costs under current statistics; a misestimate flips the choice, which is the stale-stats failure in [[How do stale statistics hurt a query plan]].

> [!tip] Interview answer
> Nested loop probes the inner side per outer row and wins with a small outer plus an indexed inner. Hash join builds a hash table of one side and probes it, winning for large equality joins without useful order. Merge join walks both sides in key order, streaming sorted output, but pays to sort inputs unless indexes already provide the order. Indexes are what make nested loop and merge join viable at scale.
