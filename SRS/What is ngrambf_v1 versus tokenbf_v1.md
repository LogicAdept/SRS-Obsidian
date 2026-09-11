<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is ngrambf_v1 versus tokenbf_v1

> [!abstract] Short answer
> Both are deprecated ClickHouse bloom-filter data-skipping indexes for text. tokenbf_v1 splits values into tokens separated by non-alphanumeric characters and serves word-level predicates (hasToken, LIKE on words); ngrambf_v1 indexes overlapping n-character substrings and serves substring-style patterns, useful for languages without word breaks. Both only exclude granules, and the docs now point to the text index as the recommended replacement.

## The mechanical difference

tokenbf_v1 takes three bloom parameters — filter size in bytes, number of hash functions, and seed — and feeds it the tokens of each value: 'This is a candidate for a "full text" search' becomes the tokens This, is, a, candidate, for, full, text, search. It works with String, FixedString, and Map, and supports equality, IN, LIKE, and hasToken-style word lookups. ngrambf_v1 takes one extra first parameter, the n-gram size: with n=4, 'A short string' is indexed as 'A sh', ' sho', 'shor', 'hort', ... — overlapping windows of characters, which lets it answer substring predicates but also makes the filter larger and denser. Both are attached with GRANULARITY and evaluated per block of granules; both are probabilistic, so false positives only cost extra granule reads, per the skip-index mechanics in [[What data skipping indexes exist in ClickHouse]].

```sql
ALTER TABLE logs ADD INDEX msg_tok   message TYPE tokenbf_v1(65536, 4, 1237) GRANULARITY 4;
ALTER TABLE logs ADD INDEX msg_ngram message TYPE ngrambf_v1(3, 65536, 4, 0)  GRANULARITY 4;
```

**Listing 1.** Token bloom for word lookups; n-gram bloom for substring patterns — both historical, both superseded by the text index.

## Deprecation and the modern path

The current documentation marks both types deprecated and directs full-text workloads to the dedicated text index — a true inverted index with deterministic token indexing, better performance, and support for hasAnyTokens/hasAllTokens/hasPhrase semantics, per [[What is a text index in ClickHouse]]. The deprecation logic follows the skip-index economics: bloom filters over very common tokens rarely exclude granules, and tuning bytes/hashes/seed is a black art, while the inverted index resolves tokens exactly. For the function side of the migration, hasToken remains the word-lookup primitive but the docs recommend the hasAnyTokens/hasAllTokens family, per [[What is hasToken in ClickHouse]]; the overall LIKE-acceleration picture is in [[How does ClickHouse accelerate LIKE and substring search]] and the verification method in [[How do you verify a ClickHouse index is used]].

> [!warning] "Bloom filter index = inverted index" is the conflation to avoid
> A bloom filter answers "maybe present" per granule and never locates rows or tokens; an inverted index maps tokens to locations. Saying ngrambf is "an inverted index for substrings" fails the follow-up: n-gram bloom filters grow with alphabet diversity and cannot prune as precisely, which is exactly why the text index replaced them. Also both bloom types are irrelevant when the filtered value is common in every granule — correlation governs usefulness, per [[Why might a ClickHouse skip index not help]].

> [!tip] Interview answer
> tokenbf_v1 indexes whole tokens split on non-alphanumerics and suits word-level lookups; ngrambf_v1 indexes overlapping n-character windows and suits substring patterns, including languages without spaces. Both are bloom-filter skip indexes that exclude granules probabilistically, and both are now deprecated in favor of ClickHouse's text (inverted) index, which resolves tokens deterministically and supports the hasAnyTokens/hasAllTokens function family.
