<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is keyset pagination?

> [!abstract] Short answer
> **Keyset pagination** fetches the next page with a *seek*: remember the last row's sort key and ask for rows strictly after it — `WHERE (at, id) > (:last_at, :last_id) ORDER BY at, id LIMIT :n`. The plan is an index seek per page regardless of page number; no skipped-row walk. It replaces `OFFSET`, whose cost grows linearly with page depth, and requires a deterministic, unique-able sort key ([[Why is OFFSET pagination slow]]).

The verified demo shows the mechanics and the plan: page one is `ORDER BY at, id LIMIT 2` returning rows (1, '2024-01-01') and (2, '2024-01-02'); page two asks `(at, id) > ('2024-01-02', 2)` and returns exactly the following two — and the plan reads `SEARCH events USING COVERING INDEX idx_events_at ((at,rowid)>(?,?))`: a bounded range scan on the index, the same shape whether it is page 2 or page 20,000 ([[What is Index Cond versus Filter in EXPLAIN]]). The tuple comparison (row values, SQL-standard, SQLite 3.15+/PostgreSQL) is what makes compound keys clean; spelled out it is `(at > :a) OR (at = :a AND id > :i)` — and that expansion is why the *unique tiebreaker* is not optional: ties on `at` would otherwise duplicate or skip rows across page boundaries ([[What harmful SQL patterns or pitfalls do you know]]). The trade to state: keyset cannot jump to "page 7" (no absolute page numbers — only next/prev), and the key must be immutable in the sort order (a rising timestamp changing value moves rows between pages). Reverse direction uses `<` with the first row's key and reversed ORDER BY ([[How does LIMIT interact with ORDER BY and indexes]]).

```sql
CREATE TABLE events (id INTEGER PRIMARY KEY, at TEXT, label TEXT);
INSERT INTO events VALUES (1,'2024-01-01','a'),(2,'2024-01-02','b'),
 (3,'2024-01-02','c'),(4,'2024-01-03','d'),(5,'2024-01-05','e');
CREATE INDEX idx_events_at ON events(at);

SELECT id, at, label FROM events ORDER BY at, id LIMIT 2;
-- 1|2024-01-01|a
-- 2|2024-01-02|b
SELECT id, at, label FROM events
WHERE (at, id) > ('2024-01-02', 2) ORDER BY at, id LIMIT 2;
-- 3|2024-01-02|c
-- 4|2024-01-03|d
EXPLAIN QUERY PLAN
SELECT id FROM events WHERE (at, id) > ('2024-01-02', 2) ORDER BY at, id LIMIT 2;
-- QUERY PLAN
-- `--SEARCH events USING COVERING INDEX idx_events_at ((at,rowid)>(?,?))
```

**Listing 1.** Verified on SQLite 3.53.1. Page two continues exactly where page one ended — no double, no gap — and the plan is a bounded index range seek, identical in shape at any page depth.

```d2
direction: right
p1: "page 1
ORDER BY key LIMIT n
remember last key" {width: 220; height: 90}
p2: "page 2
WHERE key > last
LIMIT n" {width: 190; height: 90}
p3: "page k
same seek, same cost" {width: 180; height: 90}
p1 -> p2 -> p3
```

**Fig. 1.** Pagination becomes a chain of seeks: each page resumes from the previous page's last key — constant cost per page, instead of OFFSET's growing walk.

> [!warning] Keyset without a unique tiebreaker silently loses and duplicates rows
> Two events share `at` (rows 2 and 3 in the demo): paginate on `at` alone and the tie's membership in page 1 versus page 2 depends on the plan's whim, so rows jump pages or vanish. The composite `(at, id)` is the contract; `id` alone is the degenerate case that always works ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> Keyset pagination replaces OFFSET with a seek: each page asks for rows strictly after the previous page's last sort key — WHERE (at, id) is greater than the remembered tuple, ORDER BY the same keys, LIMIT n. My demo shows page two continuing exactly after page one, and the plan is an index range search identical at any depth. The requirements: an index on the sort keys, a unique tiebreaker in the key so ties cannot jump pages, and accepting that you get next/prev navigation rather than jump-to-page-N.
