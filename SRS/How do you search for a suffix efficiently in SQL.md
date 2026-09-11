<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> A suffix search (`LIKE '%pdf'`) has the same unseekable shape as contains-search — no left anchor. The classic B-tree-compatible trick: store a **reversed copy** of the string in an indexed column and search the reversed pattern as a *prefix* (`WHERE rname LIKE 'fdp%'` — here as GLOB on a binary index), which converts the unanchored suffix into a seekable range. pg_trgm serves the same need with a GIN index without the extra column ([[How does a trigram index help SQL search]]).

The verified demo runs the trick end to end: a `files` table keeps `rname` = reversed name, indexes it, and the suffix query "name ends with .pdf" becomes `rname GLOB 'fdp*'` — planned as `SEARCH files USING INDEX idx_files_rname (rname>? AND rname<?)`, a bounded B-tree range over the reversed keys. The mechanics: reversal mirrors the string, so "ends with X" on the original equals "starts with reverse(X)" on the copy, and prefix-matching is exactly what B-trees do ([[What is the difference between prefix search and contains search]]). Maintenance is the cost column: the reversed column must be written on every insert and update (a generated column in PostgreSQL: `ALTER TABLE ... ADD COLUMN rname TEXT GENERATED ALWAYS AS (reverse(name)) STORED`, then index it — the documented pattern; SQLite supports generated columns too), and case rules must match the comparison operator (GLOB is case-sensitive on binary indexes; NOCASE indexes pair with case-insensitive LIKE). When suffix search is hot *and* combined with other fuzzy patterns, pg_trgm's substring indexing usually replaces the trick — the reverse column is the zero-extension-dependency answer ([[What is the difference between LIKE ILIKE and full-text search]]).

```sql
CREATE TABLE files (name TEXT, rname TEXT);
CREATE INDEX idx_files_rname ON files(rname);
INSERT INTO files VALUES ('report.pdf', 'fdp.troper'), ('photo.jpg', 'gpj.otohp');

EXPLAIN QUERY PLAN SELECT name FROM files WHERE rname GLOB 'fdp*';
-- QUERY PLAN
-- `--SEARCH files USING INDEX idx_files_rname (rname>? AND rname<?)
SELECT name FROM files WHERE rname GLOB 'fdp*';
-- report.pdf
-- (suffix search became a prefix range on the reversed, indexed copy)
```

**Listing 1.** Verified on SQLite 3.53.1. The reversed column turns "ends with .pdf" into a bounded seek (`rname > 'fdp' AND < 'fdq'`-style) and returns exactly the PDF — suffix search with B-tree machinery.

```d2
direction: right
o: "'report.pdf'
original" {width: 150; height: 70}
r: "'fdp.troper'
reversed, indexed" {width: 160; height: 70}
q: "ends with .pdf?
= starts with 'fdp'?" {width: 220; height: 80}
s: "prefix range seek
on rname" {width: 160; height: 70}
o -> r -> q -> s
```

**Fig. 1.** Reversal mirrors the anchoring: the unanchored suffix of the original is the anchored prefix of the copy — and prefixes are what B-trees seek best.

> [!warning] The mirrored column is a consistency liability if maintained by hand
> Application code writing `name` without `rname` poisons search silently; generated columns (stored + auto-maintained) or write-path triggers remove the drift. And the index on the *original* column does nothing for suffix queries — only the reversed copy's index serves them ([[How do you alter a table in a relational database]]).

> [!tip] Interview answer
> Suffix search is unanchorable for a B-tree — '%pdf' has no left edge — so the classic trick is a stored reversed copy: index `reverse(name)` and search the reversed pattern as a prefix; my demo shows GLOB 'fdp*' planning as a bounded index seek and returning report.pdf. In PostgreSQL the reversed column is a one-line generated column, kept consistent by the engine; pg_trgm is the alternative that indexes substrings directly. Either way, only the mirrored column's index serves suffix queries.
