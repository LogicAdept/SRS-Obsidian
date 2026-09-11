<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What data skipping indexes exist in ClickHouse

> [!abstract] Short answer
> ClickHouse data-skipping indexes are defined per column expression and evaluated per block of granules: minmax stores per-block min/max for range predicates, set(N) stores up to N distinct values for equality, bloom_filter gives probabilistic set membership with a false-positive rate, and the text family covers tokens — with the text (inverted) index now recommended and tokenbf_v1/ngrambf_v1 deprecated.

## The four families and their predicate shapes

The docs' skip-index page organizes them by what they can exclude. minmax stores the minimum and maximum of the expression per block and intersects ranges — cheapest to evaluate and ideal for loosely sorted values like timestamps or IDs that correlate with the key; it never applies to array or map expressions. set(max_size) keeps the distinct values of a block (empty if the count exceeds max_size) and answers equality and IN; it suits columns that are low-cardinality within blocks but higher overall. bloom_filter tests membership with a configurable false-positive rate (default 0.025) and also works on arrays and, via mapKeys/mapValues, on maps. The text structures handle string search: tokenbf_v1 and ngrambf_v1 are bloom filters over tokens or n-grams, both deprecated in favor of the text index — a real inverted index with deterministic token lookups.

```sql
CREATE TABLE events
(
    ts      DateTime,
    user_id UInt64,
    error_code UInt16,
    message String,
    INDEX ts_minmax  ts          TYPE minmax GRANULARITY 3,
    INDEX err_set    error_code  TYPE set(100) GRANULARITY 4,
    INDEX user_bloom user_id     TYPE bloom_filter(0.025) GRANULARITY 4,
    INDEX msg_text   message     TYPE text(tokenizer splitByNonAlpha) GRANULARITY 4
) ENGINE = MergeTree
ORDER BY (toDate(ts), user_id);
```

**Listing 1.** One index per predicate shape: ranges, low-cardinality equality, high-cardinality sparse membership, token search.

## How they are evaluated and verified

A skip index is attached with GRANULARITY — how many granules per index block — and its job is strictly to exclude blocks: if the block's structure cannot rule out a match, every granule in the block is read. That is why usefulness depends on correlation between the indexed expression and the sorting key, the failure analysis in [[Why might a ClickHouse skip index not help]], and why added indexes need MATERIALIZE INDEX to cover old parts, per [[How do you materialize a skip index on existing ClickHouse data]]. Effectiveness is measured, not assumed: EXPLAIN indexes = 1 reports granules before and after each Skip index, per [[How do you verify a ClickHouse index is used]], and the primary-key side of the pruning story is [[What is a sparse primary index in ClickHouse]].

> [!warning] "One index per column and the query is fast" is B-tree thinking
> Skip indexes do not locate rows and have no seek; they only allow skipping. The wrong type for the predicate shape excludes nothing — minmax on shuffled random strings, set(100) on a column with thousands of distinct values per block, bloom on a value present in every block — and you pay evaluation cost plus the full read anyway. The docs' own best practice is test on real data with variations of type, granularity, and parameters.

> [!tip] Interview answer
> The families are minmax for range predicates on correlated columns, set(N) for equality on block-local low cardinality, bloom_filter for membership on sparse high-cardinality values including arrays and maps, and the text index — the recommended inverted index for tokens — which deprecated tokenbf_v1 and ngrambf_v1. All of them only exclude blocks of granules, chosen by GRANULARITY, and their real effect is read from EXPLAIN indexes = 1.
