<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# How does a bloom filter skip index work in ClickHouse?

> [!abstract] Short answer
> The `bloom_filter` skip index builds one Bloom filter per index block (a group of `GRANULARITY` granules) and stores it in the part. For a query predicate like `user_id = 42`, ClickHouse tests each block's filter: "definitely not present" prunes the block's granules, "maybe present" reads them. The catch is Bloom filters can produce false positives — a few useless block reads — but never false negatives, so results stay correct.

## The mechanism

At part build time (insert or merge), the indexed expression's values are hashed into a bit array per block. With the default false-positive rate of 0.025, about 2.5% of absent values will still be flagged "maybe present"; the parameter `bloom_filter(0.01)` lowers that at the cost of a bigger index. At query time the engine evaluates the predicate's value against every surviving block's filter — cheap hashing against a small bit set — and skips blocks that are certain misses. This is why the index suits high-cardinality equality and IN predicates where a `set` index would be too large and `minmax` is useless — the full type menu is in [[What data skipping indexes exist in ClickHouse]]: user ids, session ids, external correlation ids.

```sql
ALTER TABLE events ADD INDEX user_ix user_id TYPE bloom_filter(0.01) GRANULARITY 1;

SELECT count()
FROM events
WHERE user_id = 7432;   -- blocks whose filter says "no" are not read
```

**Listing 1.** A bloom_filter index over an id column with a 1% false-positive rate.

```d2
q: "WHERE user_id = 42" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
b1: "Block 1 filter:\n42 not in bit array" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
b2: "Block 2 filter:\nmaybe present" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
skip: "Skip block 1\n(0 granules read)" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
read: "Read block 2 granules\nfilter rows normally" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
q -> b1
q -> b2
b1 -> skip: definitely absent
b2 -> read: possible match
```

**Fig. 1.** Filters decide per index block; a "maybe" block is read and its rows filtered as usual.

> [!warning] Bloom indexes are unordered — they cannot serve ranges
> A `bloom_filter` answers "is this value possibly in the block?", so `timestamp >= ...` or `BETWEEN` predicates get nothing from it; ranges belong to `minmax`. The other trap: very selective data distribution or predicates the planner cannot match to the index expression make the index dead weight — the checklist in [[Why might a ClickHouse skip index not help]] covers the failure modes.

> [!tip] Interview answer
> It stores a Bloom filter per group of granules inside each part; queries hash the predicate value and skip blocks whose filter answers "definitely absent". False positives only cost extra reads, never wrong results, and the fpp parameter tunes that trade-off — verify actual pruning with [[How do you verify a ClickHouse index is used]]. Ideal for high-cardinality equality lookups on non-key columns, useless for ranges.
