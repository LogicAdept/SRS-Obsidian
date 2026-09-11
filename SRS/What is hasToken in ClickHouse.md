<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is hasToken in ClickHouse

> [!abstract] Short answer
> hasToken(haystack, token) checks whether a whole token — the longest run of characters [0-9A-Za-z_] — appears in the string, using splitByNonAlpha as the tokenizer. It exists so word-equality predicates can use token-based text indexes or tokenbf_v1 skip indexes; a plain LIKE '%token%' cannot use those structures.

## Semantics and the tokenizer contract

The function returns 1 if the token is present as a complete token and 0 otherwise, with tokens bounded by anything that is not a letter, digit, or underscore. So hasToken('clickhouse test', 'test') returns 1, while searching 'tes' does not match the token 'test' — the boundary matters and is the whole point: unlike contains-style matching, token matching is deterministic and indexable. Case matters; the case-insensitive variant is hasTokenCaseInsensitive. The docs add an operational caveat for index users: hasToken has pitfalls with text indexes using non-default tokenizers or preprocessor/postprocessor expressions, and they recommend the hasAnyTokens / hasAllTokens (and hasPhrase) family for those setups, since those functions express the semantics the index can serve directly.

```sql
SELECT hasToken('clickhouse test', 'test');   -- 1
SELECT hasToken('clickhouse test', 'tes');    -- 0 (not a full token)

SELECT count() FROM logs
WHERE hasToken(message, 'Timeout');           -- pairs with token text indexes
```

**Listing 1.** Token boundaries make the predicate exact — 'tes' does not match — which is what lets the index participate.

## Relationship to indexes and to LIKE

On a table with a tokenbf_v1 skip index, hasToken predicates can exclude granules that cannot contain the token; with the modern text (inverted) index, token lookups resolve through the inverted structure, and hasAnyTokens/hasAllTokens generalize to sets of tokens, per [[What is a text index in ClickHouse]]. A LIKE '%timeout%' predicate has no token boundary and therefore cannot use those structures — it degrades to the column-scan or n-gram path described in [[How does ClickHouse accelerate LIKE and substring search]]. The vocabulary matters in interviews too: hasToken is word-equality inside text, not substring matching, and not the boolean hasTokenFs variants of file functions; its granule-exclusion effect is verified with EXPLAIN indexes = 1, per [[How do you verify a ClickHouse index is used]].

> [!warning] "hasToken is an indexed LIKE" — it is not
> hasToken matches whole tokens under a fixed tokenizer; it will not find substrings inside tokens ('Error' inside 'Error500' does not match token 'Error'... actually 'Error500' is one token, so 'Error' is not a token of it). And an index only helps when the tokenizer of the index matches the tokenizer the function implies; mismatched tokenizer or preprocessors silently drop the benefit. The docs' recommendation to prefer hasAnyTokens/hasAllTokens exists precisely because of these pitfalls.

> [!tip] Interview answer
> hasToken checks for a complete word bounded by non-alphanumeric characters, with splitByNonAlpha semantics and case-sensitive matching (plus a case-insensitive variant). Its job is to pair with token-based indexes — the modern text index or the older tokenbf_v1 — because whole-token predicates are the ones those structures can prune. For substring semantics you need LIKE with trigram-style structures; for sets of words the hasAnyTokens/hasAllTokens family is the documented path.
