<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> A B-tree finds values by **range navigation**: `LIKE 'abc%'` is equivalent to `col >= 'abc' AND col < 'abd'` — a seekable range. `LIKE '%abc'` specifies *no leading boundary*: every key in the tree is a potential match start, so no range exists to seek and the plan must scan. The wildcard's position, not LIKE itself, decides index usability.

The boundary is the whole mechanism: a prefix fixes the left edge of the matching interval in sorted order; a leading wildcard leaves the interval unbounded, so B-tree navigation has nothing to descend to. The verified demo shows all three outcomes on SQLite: with a NOCASE index, `LIKE 'a%'` plans as `SEARCH ... (name>? AND name<?)` — a genuine range seek; `LIKE '%a'` plans as a full `SCAN` even though the same index exists. PostgreSQL's variant is worth naming: B-tree seeks for LIKE work only when the index collation is binary-compatible — the documented solution is `text_pattern_ops` / `varchar_pattern_ops` operator classes for non-C locales, or a `COLLATE "C"` index ([[How do you optimize substring search in SQL]]). And when the requirement truly is "contains", the honest answers are trigram indexes (pg_trgm), full-text search, or a reverse-string index for suffix search — each a real index answer to a wildcard problem ([[How does a trigram index help SQL search]], [[How do you search for a suffix efficiently in SQL]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE INDEX idx_name_nc ON customers(name COLLATE NOCASE);

EXPLAIN QUERY PLAN SELECT name FROM customers WHERE name LIKE 'a%';
-- QUERY PLAN
-- `--SEARCH customers USING COVERING INDEX idx_name_nc (name>? AND name<?)
EXPLAIN QUERY PLAN SELECT name FROM customers WHERE name LIKE '%a';
-- QUERY PLAN
-- `--SCAN customers USING COVERING INDEX idx_name
```

**Listing 1.** Verified on SQLite 3.53.1. The prefix pattern compiles to a bounded range on the index; the leading wildcard turns the same index into a mere scan vehicle — no range to seek, so every key must be examined.

```d2
direction: right
t: "sorted keys
ab bot botte box by" {width: 240; height: 70}
p: "LIKE 'bo%'
range [bo, bp)
seek" {width: 170; height: 90}
c: "LIKE '%te'
no left boundary
scan all keys" {width: 170; height: 90}
t -> p
t -> c
```

**Fig. 1.** A prefix pins the interval's left edge and the seek navigates; a leading wildcard leaves the edge open, collapsing the search into a linear pass.

> [!warning] "Works on my prefix search" breaks silently on locale and case
> A binary-collation index serves case-sensitive prefix seeks only; a case-insensitive `LIKE 'Al%'` on it falls back to a scan (SQLite: use a NOCASE index; PostgreSQL: text_pattern_ops). The plan, not the syntax, is the contract — verify after every collation or engine change ([[How do you implement case-insensitive search efficiently]]).

> [!tip] Interview answer
> LIKE with a leading wildcard cannot use a B-tree because a B-tree seeks ranges and '%abc' has no left boundary — every key could start a match, so the plan scans. 'abc%' is fine: it is a range seek, equivalent to col >= 'abc' AND col < 'abd', with the caveat that the index collation must match the case behavior — SQLite needs a NOCASE index, PostgreSQL text_pattern_ops. For true contains-search I switch tools: trigram indexes, full-text search, or a reversed-string index for suffixes.
