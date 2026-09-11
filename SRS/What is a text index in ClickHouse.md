<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is a text index in ClickHouse

> [!abstract] Short answer
> The text index is ClickHouse's inverted index for full-text search: it tokenizes string values and maps each token to the granules containing it, so word and phrase predicates resolve through the index instead of scanning columns. It is the recommended structure for text search workloads, replacing the deprecated tokenbf_v1 and ngrambf_v1 bloom-filter skip indexes.

## What it is and how it is declared

A text index is defined on a column with a tokenizer and optional preprocessor/postprocessor expressions, created like other indexes (ALTER TABLE ... ADD INDEX ... TYPE text(...) ) and materialized on data. Unlike bloom-filter skip indexes, which only say "this granule might contain a match", the inverted index maps tokens deterministically to the granules containing them, which the docs cite as the reason it gives better search performance and more predictable behavior for tokenized lookups. It integrates with the search functions: hasAnyTokens, hasAllTokens, and hasPhrase express word-set and phrase semantics directly, and common text search functions can be optimized through it.

```sql
CREATE TABLE logs
(
    ts DateTime,
    message String,
    INDEX idx_msg message TYPE text(tokenizer splitByNonAlpha) GRANULARITY 4
) ENGINE = MergeTree
ORDER BY (ts);

SELECT count() FROM logs WHERE hasAnyTokens(message, ['timeout', 'refused']);
```

**Listing 1.** A tokenized text index on message; the query resolves tokens through the inverted index rather than scanning the column.

## Where it sits in the toolbox

It belongs to the skipping-index family conceptually — its job is granule elimination, not row location, and it still depends on correlation and granularity like every skip structure, per [[Why might a ClickHouse skip index not help]]. Its predecessors illustrate the difference: tokenbf_v1 indexed whole tokens in a bloom filter and ngrambf_v1 indexed overlapping n-grams for substring-style patterns, but both answer probabilistically and are now deprecated in the docs, per [[What is ngrambf_v1 versus tokenbf_v1]]; hasToken pairs with them or with the text index, per [[What is hasToken in ClickHouse]]. For analytics over free text at web scale with relevance ranking, the comparison against a dedicated engine is in [[When should you use a ClickHouse text index instead of Elasticsearch]], and verification of actual granule elimination is via EXPLAIN indexes = 1 per [[How do you verify a ClickHouse index is used]].

> [!warning] "Inverted index means document-store semantics"
> The trap is expecting scoring, stemming bundles, or tf-idf ranking from the text index: it is a granule-skip structure integrated with search functions, not a Lucene replacement. Tokenizer choice matters too — a non-default tokenizer or preprocessor changes which functions can use the index efficiently, which is why the docs steer hasToken users toward hasAnyTokens/hasAllTokens for non-splitByNonAlpha setups.

> [!tip] Interview answer
> The text index is ClickHouse's inverted index: it tokenizes the column and maps tokens to granules, so hasAnyTokens, hasAllTokens, and phrase-style predicates skip straight to relevant granules. It is the docs' recommended full-text structure and supersedes the deprecated tokenbf and ngrambf bloom filters. It still only skips granules — correlation and granularity decide whether it pays, and EXPLAIN indexes = 1 shows the elimination.
