<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Partitioning #SRS

# Why do too many partitions hurt ClickHouse?

> [!abstract] Short answer
> Because background merges never combine parts from different partitions. With thousands of partitions, each partition holds only a few small parts that cannot be merged into bigger ones; part counts per partition then hit the limits (`parts_to_throw_insert`, `parts_to_delay_insert`), inserts start failing with "Too many parts", and both storage and query efficiency degrade.

## The mechanism, step by step

Every `INSERT` writes one part per distinct partition value in the block — ten partitions in a block mean ten parts, not one. Merging is the mechanism that turns many small parts into few big, well-compressed, well-indexed ones; the cross-partition merge ban exists to keep partition semantics (drop, TTL, min-max pruning) sharp. With a high-cardinality key (per-user, per-id partitioning), each partition accumulates dust parts that never merge: more open files and marks to track, worse compression (small parts compress poorly), slower queries that must scan many part headers, and finally the parts-per-partition error that starts rejecting inserts. The docs' sizing rule: keep partition cardinality under 1000..10000.

```d2
ok: "Monthly partitions\n202601: parts merge into one" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
bad: "PARTITION BY user_id\n1M partitions x 1 tiny part" {
  width: 340
  height: 90
  style.fill: "#ffebee"
}
nomerge: "No cross-partition merges\nparts stay tiny forever" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
limit: "parts_to_throw_insert reached\n'Too many parts' - inserts fail" {
  width: 380
  height: 90
  style.fill: "#ffebee"
}
fix: "Fix: toYYYYMM(date) + user_id in ORDER BY" {
  width: 400
  height: 80
  style.fill: "#e3f2fd"
}
bad -> nomerge
nomerge -> limit
ok -> fix
```

**Fig. 1.** Monthly partitioning merges fine; per-user partitioning strangles merging and ends in rejected inserts.

## When partitions genuinely help queries

Partition pruning via MinMax indexes shines when queries filter onto a few partitions and the partition key is not the leading sort-key column — otherwise the sort key already prunes granules and partitioning adds management value only. If the motivation is retention, prefer monthly partitions plus [[What is TTL in ClickHouse]] and [[How do you drop old data quickly in ClickHouse]] over finer buckets; if the motivation is per-tenant isolation, order by tenant first ([[How do you choose ORDER BY in ClickHouse]]) rather than partitioning by tenant.

> [!warning] "More partitions = faster queries" is a PostgreSQL instinct
> In PostgreSQL, more partitions can prune better with little downside; in ClickHouse the trade is inverted because merge capacity is the budget you are spending. The correct reflex here is: default to no partitioning at all (the MergeTree reference says most tables don't need one), add monthly partitioning for retention, and measure granule pruning with EXPLAIN before adding anything finer.

> [!tip] Interview answer
> Parts never merge across partitions, so a high-cardinality partition key leaves thousands of unmergeable dust parts, degrades compression, and eventually trips the Too many parts limit and rejects inserts. Partition by month at most, keep total partitions in the low thousands, and express high-cardinality dimensions in ORDER BY or with skip indexes instead.
