<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS

# What is pg_trgm?

> [!abstract] Short answer
> pg_trgm is a contrib extension that splits words into trigrams — three-character sliding windows — and measures text similarity by counting shared trigrams. It gives functions and operators (`similarity`, `word_similarity`, `%`), and GIN/GiST operator classes that make `LIKE '%substr%'`, `ILIKE`, and fuzzy matching fast, where a B-tree is useless.

## The model

A trigram is three consecutive characters; the module pads each word with spaces (" cat ") so short words still produce trigrams, and it drops non-alphanumeric characters. Two strings are similar when they share enough trigrams; the threshold default is 0.3 (`pg_trgm.similarity_threshold`).

```sql
CREATE EXTENSION pg_trgm;
SELECT show_trgm('cat');          -- {"  c"," ca","cat","at "}
SELECT similarity('kitten', 'sitting');          -- ~0.3
SELECT * FROM products WHERE name % 'aple';      -- similarity >= threshold
CREATE INDEX products_name_trgm ON products USING gin (name gin_trgm_ops);
```

**Listing 1.** Extension, introspection, fuzzy operator, and the GIN index that accelerates it ([[What is the difference between GIN and GiST indexes in PostgreSQL]]).

## What the index accelerates

With a GIN or GiST `gin_trgm_ops`/`gist_trgm_ops` index, the planner can use it for:

- `LIKE '%middle%'` and `ILIKE '%Middle%'` — the classic "leading wildcard kills my index" problem ([[What is the difference between LIKE ILIKE and full-text search]]);
- `~` / `~*` regex searches with a literal part long enough to produce trigrams;
- `%` similarity and `word_similarity()` fuzzy lookups — typo tolerance without an external search engine.

```d2
like: "LIKE '%abc%'\nB-tree: useless" {width: 280; height: 80}
trgm: "pg_trgm index\ntrigram lookup of 'abc'" {width: 300; height: 80}
fuzzy: "Typos / similarity\n% and word_similarity" {width: 320; height: 80}
like -> trgm
fuzzy -> trgm
```

**Fig. 1.** One index structure serves both substring search and fuzzy matching.

## Where it sits among search tools

pg_trgm is the tool for short strings, autocomplete and typo tolerance inside PostgreSQL. For ranked retrieval over documents use full-text search ([[How does full-text search work in PostgreSQL]]); for large-scale substring workloads the same trigram idea exists outside the RDBMS ([[How does ClickHouse accelerate LIKE and substring search]]). The substring-specific SQL techniques are collected in [[How do you optimize substring search in SQL]].

> [!warning] Trigram indexes are big and the threshold is per-session
> Every trigram of every value is indexed, so GIN trigram indexes on wide text are several times larger than the column. And `%` uses `pg_trgm.similarity_threshold`, which is session-settable — "why did my query stop using the index" is often a changed threshold or a too-short search term with too few trigrams.

> [!tip] Interview answer
> pg_trgm breaks words into three-character windows and scores similarity by overlap; the extension adds operators plus GIN and GiST operator classes. With such an index even LIKE with a leading wildcard, ILIKE, regex fragments and typo-tolerant matching become index lookups. Cost: a large index; sweet spot: short-string fuzzy search in PostgreSQL.
