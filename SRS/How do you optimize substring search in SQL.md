<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How do you optimize substring search in SQL?

> [!abstract] Short answer
> Substring search in SQL is `LIKE '%str%'`, and the string functions around it — `SUBSTR`/`SUBSTRING`, `INSTR`/`POSITION`/`STRPOS`, `LOCATE` — locate or extract pieces. Performance law: no B-tree index can serve an unanchored substring, so it is a full scan by construction; the upgrades are trigram indexes (index every 3-char window), full-text search (token semantics), or external engines ([[How does a trigram index help SQL search]], [[What is the difference between prefix search and contains search]]).

The verified demo shows the functional layer: `instr(title, 'oo')` returns the 1-based position of the first occurrence (2 in "Book", 0 when absent — the portable emptiness test), `substr(title, 2, 2)` slices by position, and `LIKE '%oo%'` finds the row the functions would locate. These functions compose into search features — normalized comparisons, token splitting — but every *unanchored* form keeps the same plan shape: a linear pass with per-row evaluation. The index-based answers, in escalating machinery: trigram (PostgreSQL's pg_trgm GIN index serves `LIKE '%abc%'` by intersecting trigram lookups — the documented approach for substring search at scale); FTS5/textsearch when "contains the *word*" is the real requirement (word-boundary semantics, stemming, ranking); reverse-string indexes when it is suffix-shaped ([[How do you search for a suffix efficiently in SQL]]). The honest sizing note: substring scans are not automatically wrong — a weekly admin query scanning 100k rows is fine; the *hot* search path with unbounded growth is where the machinery upgrade pays ([[What is sargability in SQL]], [[When should you use Elasticsearch instead of SQL search]]).

```sql
CREATE TABLE pr (id INTEGER PRIMARY KEY, price NUMERIC, title TEXT);
INSERT INTO pr VALUES (3, 30, 'Book'),(4, 250, 'Monitor');

SELECT instr(title, 'oo') AS pos, substr(title, 2, 2) AS sub
FROM pr WHERE id = 3;
-- 2|oo
-- (instr: first occurrence at position 2; substr: slice from position 2)
SELECT title FROM pr WHERE title LIKE '%oo%';
-- Book
-- (unanchored pattern: full scan by construction, whatever the indexes)
```

**Listing 1.** Verified on SQLite 3.53.1. Position lookup, positional slice, and the pattern form of the same search — the functional toolkit whose unanchored uses are all plan-level scans.

```d2
direction: right
s1: "LIKE '%str%'
scan, per-row eval" {width: 190; height: 80}
s2: "trigram index
substring windows indexed" {width: 210; height: 80}
s3: "full-text search
word tokens + rank" {width: 190; height: 80}
s4: "external engine
fuzzy, analytics, scale" {width: 200; height: 80}
s1 -> s2 -> s3 -> s4
```

**Fig. 1.** The substring-search ladder: from the always-correct scan through indexing every substring window to token and external-engine semantics — each step buys speed by narrowing what "match" means.

> [!warning] Functions that *locate* are not functions that *search at scale*
> instr/strpos in a predicate (`WHERE instr(col, 'x') > 0`) is the same scan as LIKE '%x%' wearing a costume — the plan never changes. Reach for the machinery when the query is hot; do not micro-optimize the function choice inside an O(N) pass ([[Why does a function on a column prevent index use]]).

> [!tip] Interview answer
> Substring search is LIKE with both wildcards, supported by SUBSTR for slicing and INSTR or STRPOS for locating — my demo shows instr returning the position and the LIKE form finding the same row. The plan law: an unanchored substring cannot use a B-tree, so it scans by construction. For hot searches I escalate: trigram indexes that index 3-character windows serve contains-search, full-text search when word tokens are the real requirement, reverse indexes for suffixes, or an external engine when fuzzy matching and analytics enter.
