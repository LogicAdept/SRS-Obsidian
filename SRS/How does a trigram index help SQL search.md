<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> A **trigram index** indexes every 3-character sliding window of a string, so *contains* patterns become set intersections: the pattern '%erli%' is decomposed into trigrams (erl, rli, lin), and candidate rows are those whose trigram sets share them. PostgreSQL ships it as the `pg_trgm` extension (`CREATE EXTENSION pg_trgm; CREATE INDEX ... USING GIN (col gin_trgm_ops)`), after which `LIKE '%abc%'`, `ILIKE '%abc%'` and similarity ranking all become index-supported ([[How do you optimize substring search in SQL]]).

The mechanism is worth demonstrating rather than asserting, and SQLite can compute the decomposition itself: a recursive CTE sliding a 3-character window over 'Berlin' produces Ber, erl, rli, lin — exactly the units pg_trgm would index — and the demo's second query counts the shared trigrams between 'Berlin' and the pattern '%erli%': 3. That *sharing* is the search: pg_trgm's GIN index maps trigram -> rows, a pattern turns into "rows having ALL (or most of) these trigrams", and the remaining candidates get a final recheck for exactness — the documented similarity operator `%` and `similarity_threshold` ride the same decomposition. Two honest caveats: strings shorter than 3 characters generate no trigrams (pg_trgm documents fall-back behavior for short patterns — short searches degenerate toward scans), and trigram sharing is *approximate* — it narrows candidates, the recheck decides — so the index accelerates but does not redefine matching. The selection rule: contains-search hot paths on large tables are the trigram's niche; token-shaped questions belong to FTS, and exact prefix lookups never needed it ([[When should you use full-text search instead of LIKE]], [[What is the difference between prefix search and contains search]]).

```sql
WITH RECURSIVE tri(s, p, t) AS (
  SELECT 'Berlin', 1, substr('Berlin', 1, 3)
  UNION ALL
  SELECT s, p + 1, substr(s, p + 1, 3) FROM tri WHERE p + 1 <= length(s) - 2
)
SELECT t FROM tri;
-- Ber
-- erl
-- rli
-- lin
-- (the 3-char sliding windows a trigram index would store for 'Berlin')
WITH RECURSIVE tri(s, p, t) AS (
  SELECT 'Berlin', 1, substr('Berlin', 1, 3)
  UNION ALL SELECT s, p + 1, substr(s, p + 1, 3) FROM tri WHERE p + 1 <= length(s) - 2
)
SELECT COUNT(*) FROM tri WHERE t IN ('erl', 'rli', 'lin');
-- 3
-- (pattern '%erli%' shares 3 trigrams with the word: candidate match)
```

**Listing 1.** Verified on SQLite 3.53.1 (decomposition algorithm; pg_trgm itself is PostgreSQL). The sliding window and the shared-trigram count are the exact mechanism the extension's GIN index implements.

```d2
direction: right
w1: "'Berlin' ->
Ber erl rli lin" {width: 170; height: 80}
w2: "'%erli%' ->
erl rli lin" {width: 170; height: 80}
g: "GIN index
trigram -> rows" {width: 170; height: 80}
m: "intersect candidates
+ exact recheck" {width: 200; height: 80}
w1 -> g
w2 -> g
g -> m
```

**Fig. 1.** Both the data and the pattern decompose into trigram sets; the index intersects them, and the survivors face one exact recheck — contains-search as set algebra.

> [!warning] Trigram matching is approximate until the recheck — and short patterns starve it
> Shared trigrams admit false positives (different words share windows), so the recheck is mandatory for correctness; and one- or two-character patterns have no trigrams, collapsing the index advantage. Size the pattern language before committing to pg_trgm ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> A trigram index slides a 3-character window over every string and indexes the windows — my CTE demo decomposes Berlin into Ber, erl, rli, lin and shows a pattern sharing three of them. PostgreSQL's pg_trgm builds a GIN index over those windows, so LIKE, ILIKE and similarity searches become index lookups with a final recheck. I reach for it on hot contains-search over big tables, with the caveats that matching is approximate until recheck and that patterns shorter than three characters get no help.
