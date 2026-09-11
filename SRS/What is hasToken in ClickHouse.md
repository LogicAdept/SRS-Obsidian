<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #Databases/SQL #SRS

# What is hasToken in ClickHouse?

> [!abstract] Short answer
> `hasToken(haystack, token)` reports whether a string contains the given token — a substring split from surrounding non-alphanumeric characters. It exists specifically to partner with token-based string indexes (`text`, `tokenbf_v1`): `hasToken` is one of the few partial-match functions such indexes can evaluate, unlike a generic `LIKE`.

## Semantics and the index contract

`hasToken('clickhouse test', 'test')` returns 1: tokens are maximal runs separated by non-alphanumeric characters, so `'test'` matches but `'te'` does not — there is no partial-word matching. The case-sensitive pair is `hasTokenCaseInsensitive`; the family extends to `hasAnyTokens`, `hasAllTokens`, and ordered `hasPhrase` (which additionally requires tokens to appear in the same order). With a `text` or `tokenbf` index on the column, the engine uses the index to prune granules whose token sets exclude the needle; without an index it degrades to scanning — the raw scalar functions are SIMD-vectorized, but they read every granule ([[How do you search logs in ClickHouse]] shows the indexed setup). The documented pitfall: with custom tokenizers or pre/postprocessor expressions, `hasToken` may not match index tokens — the docs recommend `hasAnyTokens`/`hasAllTokens` there, since they tokenize the needle with the same tokenizer the index used.

```sql
SELECT hasToken('clickhouse test', 'test');      -- 1
SELECT hasToken('clickhouse test', 'tes');       -- 0: no substring match
SELECT hasTokenCaseInsensitive('ClickHouse', 'clickhouse');  -- 1

-- indexed usage
ALTER TABLE logs ADD INDEX msg_ix msg TYPE text(tokenizer = 'splitByNonAlpha') GRANULARITY 1;
SELECT count() FROM logs WHERE hasToken(msg, 'timeout');
```

**Listing 1.** Token-boundary semantics first, then the indexed pattern over [[What is a text index in ClickHouse]].

> [!warning] hasToken is not LIKE and not substring search
> Three different questions: `hasToken(msg, 'err')` needs token boundaries; `msg LIKE '%err%'` needs substrings — served by n-gram indexes or accelerated with [[How does ClickHouse accelerate LIKE and substring search]]; and `position(haystack, needle)` is raw substring with no index support at all. Answering a "find the error id" interview question with hasToken, or vice versa, signals you have never debugged why the index was not used.

> [!tip] Interview answer
> hasToken checks for a whole token — substring boundaries enforced by non-alphanumeric separators — and it is the function that token-based string indexes can actually evaluate, pruning granules before row filtering. Case-insensitive work goes through hasTokenCaseInsensitive or a lower() preprocessor, and hasAnyTokens/hasAllTokens handle multi-term and custom-tokenizer cases.
