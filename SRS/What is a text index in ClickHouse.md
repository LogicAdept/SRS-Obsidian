<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# What is a text index in ClickHouse?

> [!abstract] Short answer
> A `text` index (also called an inverted index) is a MergeTree skip index that maps each token of a text column to the granules containing it. Unlike the deprecated `tokenbf_v1`/`ngrambf_v1` Bloom filters, it is a true inverted index: deterministic token indexing, no false positives, and it accelerates `hasToken`, `hasAllTokens`, `hasAnyTokens`, `hasPhrase`, `LIKE`, `IN`, `equals`, and `startsWith`-style predicates.

## Definition and structure

Declared like any skip index — `INDEX name col TYPE text(tokenizer = ...) GRANULARITY 1` — it tokenizes the column with the chosen tokenizer (`splitByNonAlpha` by default, `splitByString`, `splitByRegexp`, plus CJK options like `chinese` and `japanese`), and stores per-block token lists instead of probabilistic bit arrays. A `preprocessor` expression (for example `caseFoldUTF8`, `lower`, or `removeDiacriticsUTF8(normalizeUTF8NFKC(col))`) normalizes values before tokenization — and then queries must run the same functions over the search terms, because matching happens against preprocessed tokens. ClickHouse docs recommend versions >= 26.2 for production text-index use.

```sql
CREATE TABLE docs
(
    id UInt64,
    body String,
    INDEX body_idx lower(body) TYPE text(tokenizer = 'splitByNonAlpha') GRANULARITY 1
)
ENGINE = MergeTree ORDER BY id;

SELECT id FROM docs WHERE hasToken(body, 'clickhouse');
SELECT id FROM docs WHERE hasAllTokens(lower(body), ['clickhouse', 'test']);
```

**Listing 1.** A case-folded text index and token queries; the query must mirror the preprocessor ([[Why might a ClickHouse skip index not help]]).

> [!warning] It is still a skip index, not a search engine
> The text index prunes granules; matching rows are then read and filtered like any scan, so it is not a scoring/relevance engine and does not replace Elasticsearch for ranked search ([[When should you use a ClickHouse text index instead of Elasticsearch]]). Tokenizer choice is the sharp edge: `hasToken` splits needles on ASCII separators only, so CJK columns need the matching tokenizer and `hasAnyTokens`/`hasAllTokens` instead ([[What is hasToken in ClickHouse]]), and unlike Bloom filters the index must be [[How do you materialize a skip index on existing ClickHouse data]] for old parts.

> [!tip] Interview answer
> The text index is ClickHouse's inverted index for full-text predicates: per-block token lists built with a pluggable tokenizer and optional preprocessor like lower(). It gives exact, false-positive-free pruning for hasToken/hasAllTokens/hasPhrase and LIKE, replacing the deprecated token and n-gram Bloom filters. Same skip-index rules apply — matching expressions, GRANULARITY 1, and materialization for existing parts.
