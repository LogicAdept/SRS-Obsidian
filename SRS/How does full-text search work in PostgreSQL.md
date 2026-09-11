<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS

# How does full-text search work in PostgreSQL?

> [!abstract] Short answer
> PostgreSQL full-text search pre-processes documents into tsvector — lexemes with positions — and queries into tsquery, matches them with the @@ operator, ranks with ts_rank, and accelerates matching with a GIN index over the tsvector column (or an expression). Dictionaries handle stemming and stop words per text-search configuration, so matching is linguistic, not literal.

## The pipeline

```sql
SELECT to_tsvector('english', 'The cats sat on the mats') AS doc;
-- 'cat':3 'mat':6 'sat':4
SELECT to_tsquery('english', 'cats & sitting');
SELECT to_tsvector('english', body) @@ websearch_to_tsquery('english', 'fat cats')
FROM articles
ORDER BY ts_rank(to_tsvector('english', body), query) DESC;
```

**Listing 1.** Document to lexemes (stemming: cats->cat), query to tsquery, `@@` to match, `ts_rank` to order. `websearch_to_tsquery` parses user-style input safely.

1. **Parser** splits text into tokens (words, numbers, URLs...).
2. **Dictionary** (per configuration, e.g. english) stems and drops stop words.
3. **tsvector** stores surviving lexemes plus positions (positions enable phrase queries).
4. **tsquery** combines lexemes with AND/OR/NOT and phrase distance operators.

```d2
doc: "Document\ntext" {width: 180; height: 60}
vec: "to_tsvector\ntsvector lexemes + positions" {width: 320; height: 70}
gin: "GIN index over tsvector\nor over the expression" {width: 300; height: 70}
qr: "User query" {width: 180; height: 60}
tq: "to_tsquery / websearch_to_tsquery" {width: 330; height: 70}
match: "@@ match + ts_rank" {width: 260; height: 60}
doc -> vec -> gin
qr -> tq -> match
gin -> match
```

**Fig. 1.** Both sides go through the same linguistic pipeline; the index serves the lexeme lookups.

## Indexing and scaling

The production pattern is a stored generated column holding the tsvector plus a GIN index — GIN is documented as the preferred text-search index type ([[What is the difference between GIN and GiST indexes in PostgreSQL]]):

```sql
ALTER TABLE articles ADD COLUMN tsv tsvector
  GENERATED ALWAYS AS (to_tsvector('english', body)) STORED;
CREATE INDEX articles_tsv_idx ON articles USING gin (tsv);
```

**Listing 2.** The generated column keeps the transformation out of every query ([[How do generated columns work in PostgreSQL]]). For substring or typo search, combine with pg_trgm ([[What is pg_trgm]]).

> [!warning] FTS is not a substring engine
> `@@` matches lexemes: "manufactur" does not find "manufacturer" unless the dictionary stems it, and prefix search needs the `:*` syntax (`manufac:*`). Queries with leading wildcards belong to trigram indexes. The split of responsibilities is in [[What is the difference between LIKE ILIKE and full-text search]].

> [!tip] Interview answer
> Documents become tsvectors — stemmed, stop-word-free lexemes with positions — and queries become tsqueries; the @@ operator matches, ts_rank orders, and a GIN index over the tsvector makes it fast. Configuration controls the language pipeline. Use it for ranked linguistic search; use pg_trgm for substring and typo search.
