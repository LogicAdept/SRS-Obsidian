<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# What data skipping indexes exist in ClickHouse?

> [!abstract] Short answer
> MergeTree supports four classic data skipping index types — `minmax`, `set(max_rows)`, `bloom_filter([fpp])`, and the bloom-based string indexes `ngrambf_v1`/`tokenbf_v1` (both deprecated in current docs) — plus the newer dedicated `text` (inverted) index for full-text search. Each stores compact statistics per block of `GRANULARITY` granules so a query can skip blocks its predicate cannot match.

## The types and their use cases

A `minmax` index stores per-block min/max of the indexed expression and is ideal for ranges and timestamps; `set(max_rows)` stores up to max_rows distinct values per block for equality/IN checks on low-distinction data; `bloom_filter` tests membership with a configurable false-positive rate (default 0.025) for high-cardinality equality lookups; `tokenbf_v1` and `ngrambf_v1` split strings into tokens or character n-grams for word and substring predicates. The index block size is set by `GRANULARITY` — with `index_granularity = 8192` and `GRANULARITY 4`, one index block covers 32768 rows, so coarser granularity means cheaper indexes but coarser skipping.

```sql
CREATE TABLE skip_table
(
    timestamp DateTime,
    client_id UInt32,
    url String
)
ENGINE = MergeTree ORDER BY (client_id, timestamp);

ALTER TABLE skip_table
    ADD INDEX ts_ix timestamp TYPE minmax GRANULARITY 4,
    ADD INDEX cid_ix client_id TYPE set(100) GRANULARITY 2,
    ADD INDEX url_ix url TYPE text GRANULARITY 1;
```

**Listing 1.** Adding skipping indexes to an existing table; only future parts build them until you [[How do you materialize a skip index on existing ClickHouse data]].

## Choosing between them

Primary-key pruning is free but only covers the sort key; skip indexes are for columns outside the key. Timestamps and ordered numerics get `minmax`; IDs filtered by equality with moderate distinct counts get `set`; huge-cardinality equality gets `bloom_filter`; text predicates get the [[What is a text index in ClickHouse]]. All of them share a limitation: they are per-block summaries, so they help when predicates are *selective within the table* — otherwise they just cost storage, as [[Why might a ClickHouse skip index not help]] details.

> [!warning] Skip indexes are not applied to every predicate automatically
> A skip index is consulted only when the query's condition matches the indexed expression — an index on `lower(url)` will not serve `url LIKE ...` directly. And with `use_skip_indexes` disabled (default is on) or non-selective filters, they are ignored. Always verify with `EXPLAIN indexes = 1` instead of assuming ([[How do you verify a ClickHouse index is used]]).

> [!tip] Interview answer
> ClickHouse skip indexes are per-block statistics beside the sparse primary index: minmax for ranges, set for equality on modest cardinality, bloom_filter for membership, plus token/ngram bloom variants for strings and the modern text index for full text. GRANULARITY controls how many granules one index block covers, trading index size against skip precision.
