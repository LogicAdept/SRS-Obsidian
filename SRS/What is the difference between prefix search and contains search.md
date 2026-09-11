<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is the difference between prefix search and contains search?

> [!abstract] Short answer
> **Prefix search** (`LIKE 'abc%'`) pins the left edge of the match, so a B-tree can seek the range `['abc', 'abd')` — the engine plans a SEARCH. **Contains search** (`LIKE '%abc%'`) has no left boundary; every key is a candidate, so the plan is a full scan regardless of indexes. The wildcard's *position* is the whole performance story ([[Why does LIKE with a leading wildcard not use a B-tree index]], [[What is sargability in SQL]]).

The verified demo shows both plans on the same table and index: with a NOCASE index on `title`, `LIKE 'U%'` plans as `SEARCH ... (title>? AND title<?)` — a genuine bounded range — while `LIKE '%ook%'` plans as a full `SCAN` over the same index (the index at least supplies a narrow covering read, not table access). PostgreSQL's version of the same law: `text_pattern_ops` operator classes make prefix LIKE seek on a B-tree, and contains-search never does. What remains for contains: accept the scan on small tables (fine — the scan *is* the right plan under a few thousand rows), restructure the query so a prefix is available, or change the machinery — trigram indexes invert the problem by indexing *all substrings* so '%abc%' becomes index-lookup work ([[How does a trigram index help SQL search]]), full-text search switches from substring to token semantics ([[When should you use full-text search instead of LIKE]]), and Elasticsearch moves the problem out of SQL entirely ([[When should you use Elasticsearch instead of SQL search]]). The design habit: ask which searches are hot *before* choosing a search strategy — the schema (reverse columns, trigram indexes, FTS tables) follows the query shapes, not vice versa ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE pr (id INTEGER PRIMARY KEY, price NUMERIC, title TEXT);
INSERT INTO pr VALUES (1, 5, 'Cable'),(2, 10, 'USB Hub'),(3, 30, 'Book'),(4, 250, 'Monitor');
CREATE INDEX idx_pr_title_nc ON pr(title COLLATE NOCASE);

EXPLAIN QUERY PLAN SELECT id FROM pr WHERE title LIKE 'U%';
-- QUERY PLAN
-- `--SEARCH pr USING COVERING INDEX idx_pr_title_nc (title>? AND title<?)
EXPLAIN QUERY PLAN SELECT id FROM pr WHERE title LIKE '%ook%';
-- QUERY PLAN
-- `--SCAN pr USING COVERING INDEX idx_pr_title_nc
```

**Listing 1.** Verified on SQLite 3.53.1. Same index, same operator, different plans: the anchored prefix compiles to a bounded seek; the unanchored pattern must visit every key.

```d2
direction: right
t: "sorted keys
Book Cable Monitor USB Hub" {width: 250; height: 70}
p: "'U%' -> range seek
[Usb...) bounded" {width: 190; height: 90}
c: "'%ook%' -> no left edge
scan all keys" {width: 180; height: 90}
t -> p
t -> c
```

**Fig. 1.** Sorted order serves anchored patterns only: a prefix bounds the interval a seek can navigate; a leading wildcard opens it and the search degrades to a linear pass.

> [!warning] Prefix-like performance dies quietly at collation changes
> The seek form requires the index collation to match the comparison — a case-insensitive LIKE needs the NOCASE (or PG text_pattern_ops) index; on a binary-collated index the same 'U%' falls back to a scan. Verify the plan after any collation or engine migration of search paths ([[How do you implement case-insensitive search efficiently]]).

> [!tip] Interview answer
> Prefix search anchors the match's left edge, so a B-tree seeks the range from 'abc' to 'abd' — my demo shows SEARCH with title bounds. Contains search has no left anchor, so every key is a candidate and the plan scans, index or not. For small tables the scan is the correct plan; for hot contains-search I change machinery: trigram indexes that index substrings, full-text search for token semantics, or Elasticsearch for fuzzy and analytical needs.
