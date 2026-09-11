<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> **LIKE** is the portable pattern operator (case rules per engine: SQLite folds ASCII, PostgreSQL is case-sensitive). **ILIKE** is PostgreSQL's case-insensitive LIKE — same wildcards, folding built in, same index-hostility for leading wildcards. **Full-text search** (PostgreSQL textsearch, SQLite FTS5) is a different *model*: text is tokenized into words (with stemming, stop words, positions), queries select by token (`MATCH`), and results can be ranked. LIKE asks "does this substring occur"; FTS asks "does this document contain these *words*" ([[When should you use full-text search instead of LIKE]]).

The decision axis is semantics, not speed — though speed follows. Verified on SQLite: `LIKE '%and%'` over a body matches because the *substring* "and" occurs (even inside another word if it did — 'android' would match '%and%'), while FTS5's `MATCH 'indexes'` matches whole tokens only — 'indexes' matches, 'dex' does not. That boundary is the product decision: user-facing "search" almost always means words (token model, ranking, typo tolerance at scale), while substring LIKE remains correct for codes, IDs, and partial-word completion ([[What is the difference between prefix search and contains search]]). The performance corollary: ILIKE/LIKE with leading wildcards scan; FTS5 stores an inverted index (token -> rows), so MATCH is index-supported by construction, and prefix queries inside FTS (`post*`) are supported too — the demo shows 'post*' matching 'PostgreSQL' ([[How does a trigram index help SQL search]]). Case rules complete the trio: SQLite LIKE folds ASCII only, GLOB never folds; PostgreSQL LIKE folds nothing, ILIKE folds everything — portability of case behavior is *not* transitive across engines ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE VIRTUAL TABLE docs USING fts5(title, body);
INSERT INTO docs VALUES ('SQL Guide', 'PostgreSQL indexes and joins'),
 ('Cookbook', 'recipes for pasta');

SELECT title FROM docs WHERE docs MATCH 'indexes';
-- SQL Guide
SELECT title FROM docs WHERE docs MATCH 'post*';
-- SQL Guide
-- (FTS: token lookup and prefix tokens via the inverted index)
SELECT title FROM docs WHERE body LIKE '%and%';
-- SQL Guide
-- (LIKE: raw substring over the original text -- 'android' would match too)
```

**Listing 1.** Verified on SQLite 3.53.1 (FTS5). MATCH finds the token 'indexes' and the prefix token 'post*'; LIKE finds the substring 'and' — word semantics versus character semantics on the same data.

```d2
direction: right
l: "LIKE / ILIKE
character substring
case per engine" {width: 200; height: 90}
f: "FTS
inverted token index
words, prefixes, ranking" {width: 210; height: 90}
q: "is the requirement
'substring' or 'word'?" {width: 220; height: 80}
l -> q
f -> q
```

**Fig. 1.** The trio differs first in meaning — characters versus words — and only then in performance; the question being asked picks the operator.

> [!warning] LIKE '%word%' and FTS MATCH disagree on purpose
> '%and%' matches 'android'; MATCH 'and' does not. Switching an app from LIKE to FTS silently changes every result set — plurals, stems and compound words all shift. Pilot the semantic change on real queries before migrating the storage ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> LIKE is the portable substring operator with engine-dependent case rules — SQLite folds ASCII, PostgreSQL folds nothing; ILIKE is PostgreSQL's case-insensitive LIKE with identical wildcards and identical index hostility to leading wildcards. Full-text search changes the model: text becomes tokens in an inverted index, MATCH queries select words or prefix tokens, and results rank. My demo shows MATCH finding 'indexes' and 'post*' while LIKE '%and%' matches substrings. The choice is semantic: codes and partial strings stay LIKE; anything users call "search" belongs to FTS.
