<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# How does ClickHouse accelerate LIKE and substring search

> [!abstract] Short answer
> Without help, LIKE over a column scans that column across all selected granules — there is no B-tree prefix seek in ClickHouse. Acceleration comes from the primary key (restrict granules first), then data-skipping indexes: minmax/set for structured values, and for text either the text (inverted) index or the deprecated token-based bloom filters. Correlation between the filter column and the ORDER BY is what makes any skip index pay.

## The default is a column scan, by design

ClickHouse reads data in granules and is built for full-scan-style analytics with very high throughput, so an unindexed `LIKE '%error%'` over a log column streams the whole column of every selected granule and applies the match — often still fast in rows per second, but linear. The first acceleration layer is therefore the same as anywhere: make the WHERE match the ORDER BY so the primary index prunes granules, the design approach in [[How do you choose ORDER BY in ClickHouse]]. For columns outside the key, data-skipping indexes decide whether whole granules can be skipped before reading, which is the mechanism behind [[What data skipping indexes exist in ClickHouse]].

```sql
-- classic log table shape
CREATE TABLE logs
(
    ts DateTime,
    service LowCardinality(String),
    message String,
    INDEX msg_ngram message TYPE ngrambf_v1(3, 65536, 4, 0) GRANULARITY 4
) ENGINE = MergeTree
ORDER BY (service, ts);
```

**Listing 1.** The ORDER BY prunes by service and time; the skip index on message then lets granules whose n-gram bloom excludes the pattern be skipped.

## The text-search structures and their current guidance

For token-level search the modern answer is the text index — a real inverted index documented as the recommended choice for full-text search, with deterministic token indexing and functions like hasAnyTokens and hasAllTokens, per [[What is a text index in ClickHouse]]. The older bloom-filter skip indexes ngrambf_v1 and tokenbf_v1 still appear in the wild — n-grams for substring-style patterns, tokens for word equality via hasToken — but ClickHouse's docs now mark both deprecated in favor of the text index, per [[What is ngrambf_v1 versus tokenbf_v1]]. Whatever the structure, the economics are unforgiving: if a value occurs even once in a granule, that granule is read in full, so usefulness depends on data correlation and granularity, as [[Why might a ClickHouse skip index not help]] explains, and verification is via EXPLAIN indexes = 1 per [[How do you verify a ClickHouse index is used]].

> [!warning] "Add a bloom filter and LIKE becomes indexed" is the wrong mental model
> A skip index never returns rows; it only excludes granules, and any false positive costs a full granule read. With a message column whose values are spread across every granule, the bloom filter excludes nothing and you pay both index evaluation and the full scan. The design fix is ordering and correlation first, structure second — the inverse of the B-tree instinct from [[Why does LIKE with a leading wildcard not use a B-tree index]].

> [!tip] Interview answer
> ClickHouse has no B-tree seek for LIKE, so an unaided substring match scans the column of every selected granule. You accelerate it in layers: match the primary key so granules are pruned, then add skipping structures — minmax or set for structured columns, and for text the modern text (inverted) index; ngrambf_v1 and tokenbf_v1 exist but are deprecated. Because a skip index only excludes granules, usefulness depends entirely on correlation and granularity, verified with EXPLAIN indexes = 1.
