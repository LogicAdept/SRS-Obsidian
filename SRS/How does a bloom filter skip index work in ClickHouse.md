<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# How does a bloom filter skip index work in ClickHouse

> [!abstract] Short answer
> The bloom_filter skip index stores, for each block of granules, a compact bit array summarizing the block's values. At query time the predicate value is hashed against that bit array: a negative answer proves the block cannot contain the value and skips its granules; a positive answer is only maybe, so the granules are read. It targets equality on high-cardinality, sparse values outside the sorting key.

## The structure and the parameters

A bloom filter is a space-efficient probabilistic set-membership structure: k hash functions set bits in a bit array per inserted value; membership tests may produce false positives but never false negatives. ClickHouse's bloom_filter index takes a single optional parameter, the false-positive rate between 0 and 1, defaulting to 0.025 — smaller rates need more bits per value. The docs position it precisely: because false positives merely cost a few unnecessary block reads, they are harmless here; because a false negative would corrupt results, the structure guarantees none. Bloom filters shine when the number of candidate values is large, which is why they also apply to arrays (every element tested) and maps via mapKeys/mapValues, per [[What data skipping indexes exist in ClickHouse]].

```sql
CREATE TABLE events
(
    ts      DateTime,
    user_id UInt64,
    INDEX uid_bloom user_id TYPE bloom_filter(0.01) GRANULARITY 4
) ENGINE = MergeTree
ORDER BY ts;

SELECT count() FROM events WHERE user_id = 8675309;
```

**Listing 1.** user_id is not in the ORDER BY, so the primary key cannot help; the bloom index skips blocks whose filter excludes the ID.

## When it pays and when it burns

The economics come from sparsity and correlation: the ideal case is a value that is rare in the data and correlated with the sorting key, so most blocks' filters answer no and whole blocks are skipped — the docs' observability example of rare error codes. The failure case is a value common in every block: every filter answers yes, every granule is read, and you pay index evaluation plus the full scan, dissected in [[Why might a ClickHouse skip index not help]]. Like all skip indexes it is declared with GRANULARITY, must be materialized for existing parts, per [[How do you materialize a skip index on existing ClickHouse data]], and its real effect is the granule delta in EXPLAIN indexes = 1, per [[How do you verify a ClickHouse index is used]]. For string tokens specifically, the text index is now the recommended structure, per [[What is a text index in ClickHouse]].

> [!warning] "Bloom filter = fast lookup" confuses a skip index with a key-value index
> A bloom filter never returns data and never locates rows; it answers one question per block — "could this value be here?" — and a yes means read everything in the block. It also cannot serve ranges (it is unordered) — that is minmax territory. Treating it as a per-row lookup structure like an InnoDB secondary index misses the entire granule model it lives in.

> [!tip] Interview answer
> The bloom_filter skip index keeps a bit array per block of granules summarizing the block's values with a tunable false-positive rate, 2.5 percent by default. Queries hash the predicate against it: no means skip the block, yes means read it, since there are no false negatives. It is for equality on high-cardinality sparse columns outside the ORDER BY, works on arrays and map projections, and only pays off when values are rare and correlated with the key.
