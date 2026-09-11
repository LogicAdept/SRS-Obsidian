<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# What is ngrambf_v1 versus tokenbf_v1?

> [!abstract] Short answer
> Both are Bloom-filter-based [[What data skipping indexes exist in ClickHouse]] string indexes: `tokenbf_v1` splits the column into word tokens on non-alphanumeric characters and indexes whole tokens, while `ngrambf_v1` splits into fixed-length character n-grams (size `n` given first) and indexes those — which is what lets it serve substring and LIKE predicates. In current docs both are deprecated in favor of the dedicated `text` index for full-text workloads.

## Token versus n-gram splitting

`tokenbf_v1(size_of_bloom_filter_in_bytes, number_of_hash_functions, random_seed)` indexes the tokens of "This is a candidate for a full text search" — so `hasToken`, word `LIKE '%word%'`, `IN`, and equality checks can prune blocks. `ngrambf_v1(n, size_of_bloom_filter_in_bytes, number_of_hash_functions, random_seed)` with `n = 4` breaks the same string into overlapping 4-character pieces, so a needle like `'text sea'` matches its n-grams against the block's filter — substring search without tokens. The n-gram approach also powers its classic secondary use: filtering `arrayJoin`-style searches over values that contain no token structure at all.

Sizing is not guesswork: the MergeTree reference ships helper functions — `bfEstimateBmSize(elements, false_positive)` for filter bytes and `bfEstimateFunctions(elements, bytes)` for hash-function count — so a 4300-ngram granule at a 0.0001 false-positive target computes its filter size in SQL instead of folklore. As a rule from [[How does ClickHouse accelerate LIKE and substring search]]: token indexes serve whole-word needles cheaply; n-gram indexes buy substring reach with proportionally bigger filters.

```sql
-- word-oriented search over log lines
ALTER TABLE logs ADD INDEX tok_ix msg TYPE tokenbf_v1(1024, 3, 0) GRANULARITY 1;

-- substring-oriented search
ALTER TABLE logs ADD INDEX ngr_ix msg TYPE ngrambf_v1(3, 1024, 3, 0) GRANULARITY 1;

SELECT count() FROM logs WHERE hasToken(msg, 'timeout');
SELECT count() FROM logs WHERE msg LIKE '%tion of the%';   -- ngram territory
```

**Listing 1.** Tokens serve whole-word predicates; n-grams serve partial matches.

> [!warning] Deprecated — the text index replaced them
> Current documentation marks both types "(Deprecated)" and recommends the [[What is a text index in ClickHouse]] for full-text workloads: a true inverted index with deterministic token indexing, better performance, and support for `hasAnyTokens`/`hasAllTokens`. Also remember n-gram indexes multiply with string length — a short `n` over long strings bloats the filter, while a long `n` misses short needles; both failure modes disappear only by choosing the right splitting model, not by tuning one parameter.

> [!tip] Interview answer
> Same Bloom-filter machinery, different splitting: tokenbf indexes whole words split on non-alphanumerics — good for hasToken and word LIKE — while ngrambf indexes fixed-length character n-grams, enabling substring matching at the cost of bigger filters and an extra size parameter. Both are legacy now; new designs use the text index, but understanding token versus n-gram explains what each can and cannot match.
