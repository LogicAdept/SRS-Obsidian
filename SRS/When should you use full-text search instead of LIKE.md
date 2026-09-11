<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# When should you use full-text search instead of LIKE

> [!abstract] Short answer
> Use full-text search when the query is about words: natural-language documents, stemming (running matches run and ran), ranking by relevance, language-aware tokenization, boolean combinations, and phrase or prefix operators over a GIN-indexed tsvector. Use LIKE for exact or prefix patterns on codes, emails, and identifiers — deterministic substrings with no language in them.

## What LIKE cannot give you

LIKE and ILIKE answer "does this string contain this literal substring". They have no concept of word boundaries, word forms, or importance: '%run%' matches 'runs', 'runtime', and 'brunch' indiscriminately, every match weighs the same, and there is no way to ask for "documents about database performance". PostgreSQL's text search model was built for exactly the opposite requirements: it parses documents into lexemes with a language configuration, removes stopwords, matches queries against normalized lexemes, and ranks results with ts_rank, with the whole pipeline documented in its text search chapters. The index that powers it is GIN over the tsvector column (or an expression index), which stays small relative to trigram indexes on the same text and is maintained on writes.

```sql
ALTER TABLE articles ADD COLUMN tsv tsvector
    GENERATED ALWAYS AS (to_tsvector('english', title || ' ' || body)) STORED;
CREATE INDEX idx_articles_tsv ON articles USING gin (tsv);

SELECT title, ts_rank(tsv, query) AS rank
FROM articles, to_tsquery('english', 'database & performance') query
WHERE tsv @@ query
ORDER BY rank DESC
LIMIT 10;
```

**Listing 1.** A generated tsvector column plus GIN index: stemmed, ranked, boolean-capable search inside PostgreSQL.

## The decision boundary in both directions

Switch to FTS when matches should respect words, forms, and relevance — search boxes, knowledge bases, log message word lookups. Stay with LIKE when the pattern is an identifier fragment: SKU prefixes, domain suffixes, email domains; there the exact-substring semantics are the requirement and trigram (for contains) or the plain B-tree (for prefixes) is cheaper and simpler, per [[What is the difference between prefix search and contains search]] and [[How do you optimize substring search in SQL]]. pg_trgm remains the bridge for typo-tolerant LIKE-style search on short strings. The external-engine boundary — relevance tuning, facets, scale beyond a database node — is its own decision in [[When should you use Elasticsearch instead of SQL search]].

> [!warning] "FTS replaces LIKE" and "FTS is only for big documents"
> FTS does not do literal substring matching — to_tsquery normalizes both sides, so searching for a code fragment like 'ERR_42' can behave surprisingly; that job belongs to LIKE with an appropriate index. In the other direction, FTS pays off on short fields too (titles, tags) whenever stemming or ranking matter, not just on long documents. The real criterion is whether the query is linguistic or literal.

> [!tip] Interview answer
> I use full-text search when matching is linguistic: stemmed words, relevance ranking, boolean queries, language configs — a tsvector with a GIN index inside PostgreSQL. I use LIKE when the match is literal: codes, emails, prefixes, suffixes, with a B-tree or trigram index as appropriate. The tell is whether 'run' should match 'running' — if yes, FTS; if the string must contain exactly 'run', LIKE.
