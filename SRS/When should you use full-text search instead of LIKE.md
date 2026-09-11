<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# When should you use full-text search instead of LIKE?

> [!abstract] Short answer
> Prefer **full-text search** over LIKE when the requirement is word-shaped: find documents *containing words* (any of / all of / phrase), rank by relevance, handle morphology (stemming), scale beyond a few thousand rows. Keep **LIKE** for exact substring semantics: codes, IDs, partial words, completion-as-you-type on anchored prefixes. The signal is the query language itself — FTS exposes boolean operators and ranking; LIKE exposes wildcards ([[What is the difference between LIKE ILIKE and full-text search]]).

The verified demo is the ranking half — the thing LIKE structurally cannot do. Three articles, one with 'sql' three times, one once: FTS5's `bm25()` orders them by relevance (the triple-hit document first, its score lower = better in SQLite's sign convention) — with LIKE, both rows are just "matches", and the application would hand-craft relevance from scratch. The rest of FTS's side: an inverted index (token -> rows) makes word queries index-supported at any scale, while LIKE '%..%' scans ([[How do you optimize substring search in SQL]]); stemming groups 'index', 'indexes', 'indexed' (engine-configured); boolean composition (`a OR b`, `a AND NOT c`, phrase "exact words") is part of MATCH syntax. LIKE's side needs no advocacy: it is exact, transactional, indexable when anchored, and zero-machinery — the right answer whenever the pattern is a *string fragment*, not a word concept ([[What is the difference between prefix search and contains search]]). The migration judgment: teams usually start with LIKE, feel the pain as data grows (scans) or as users demand ranking — at that point the semantic shift (substring to token) must be piloted on real queries, not just deployed ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE VIRTUAL TABLE articles USING fts5(title, body);
INSERT INTO articles VALUES ('SQL', 'sql sql sql basics'),
 ('Java', 'java and sql integration'),
 ('Cookbook', 'pasta and sauces');

SELECT title, bm25(articles) AS score FROM articles
WHERE articles MATCH 'sql' ORDER BY score;
-- SQL|-1.6716417910447762e-06
-- Java|-9.71608832807571e-07
-- (bm25: lower = better; the document with 3 hits ranks above the 1-hit one)
```

**Listing 1.** Verified on SQLite 3.53.1 (FTS5). Two documents both "contain sql", yet relevance orders them — ranking by term frequency is FTS-native and impossible to express in LIKE at all.

```d2
direction: right
a: "requirement:
substring / code / prefix" {width: 230; height: 80}
b: "requirement:
words, relevance, morphology" {width: 240; height: 80}
l: "LIKE
(+ prefix-index when anchored)" {width: 210; height: 80}
f: "FTS: inverted index
MATCH + bm25 rank" {width: 200; height: 80}
a -> l
b -> f
```

**Fig. 1.** Two requirement families, two tools: string-fragment questions stay with LIKE; word-and-relevance questions need FTS's token index and ranking.

> [!warning] FTS is an additional index to feed — plan its writes
> An FTS table (or tsvector column with GIN) must be kept in sync with the source text; sync failures surface as "search finds nothing" rather than errors. Decide the update mechanism at design time (triggers, generated tsvector, FTS5 external-content tables), not after the first desync incident ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> I choose by requirement shape: substring needs — codes, IDs, anchored prefixes — stay with LIKE, which is exact and indexable when anchored. The moment the requirement is words — any-of, phrases, stemming, relevance ordering — full-text search wins: its inverted index makes word queries scale, and bm25 ranking is native; my demo shows a 3-hit document ranking above a 1-hit one, which LIKE cannot express. The cost I name is operational: FTS is another index that must stay in sync, so the update mechanism is a design decision, not an afterthought.
