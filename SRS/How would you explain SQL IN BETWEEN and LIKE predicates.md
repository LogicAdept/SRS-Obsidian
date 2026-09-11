<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> Three row predicates from the standard's toolbox: `IN (list | subquery)` — membership against explicit values or a subquery result; `BETWEEN a AND b` — a range *inclusive on both ends* (exactly `col >= a AND col <= b`); `LIKE` — pattern matching where `%` matches any run of characters and `_` exactly one. All three are sargable when the left side is a bare indexed column and the shape cooperates (BETWEEN and LIKE-prefix seek; IN seeks per value) ([[What is sargability in SQL]]).

The verified demo pins the semantics people get wrong. BETWEEN's inclusivity: `price BETWEEN 5 AND 30` returns 5, 10 **and** 30 — both boundary rows belong (the classic missed-off-by-one bug is assuming an exclusive end; a NOT BETWEEN or explicit `>` `<` is the escape when bounds must exclude). IN lists values positionally with no range meaning, and with a subquery it becomes the membership operator whose NULL behavior differs radically under negation ([[Why is NOT IN dangerous with NULL]]). LIKE's two wildcards: `'U%'` matches USB Hub (any tail), `'_able'` matches Cable (exactly one character then "able") — and the pattern language is where engines differ subtly: case sensitivity (SQLite LIKE is ASCII-case-insensitive, GLOB is not; PostgreSQL LIKE is case-sensitive with ILIKE for the insensitive form) and escaping with `ESCAPE` ([[What is the difference between LIKE ILIKE and full-text search]]). Plan-wise all three can drive an index: BETWEEN compiles to one inclusive range seek, IN to a seek per listed value, prefix-LIKE to a range ([[Why does LIKE with a leading wildcard not use a B-tree index]]) — functions or wildcards on the *left* of the column are what break them, not the operators themselves.

```sql
CREATE TABLE pr (id INTEGER PRIMARY KEY, price NUMERIC, title TEXT);
INSERT INTO pr VALUES (1, 5, 'Cable'),(2, 10, 'USB Hub'),(3, 30, 'Book'),(4, 250, 'Monitor');

SELECT id, price FROM pr WHERE price BETWEEN 5 AND 30 ORDER BY id;
-- 1|5
-- 2|10
-- 3|30
-- (inclusive on BOTH ends: 5 and 30 are returned)
SELECT id FROM pr WHERE id IN (1, 3) ORDER BY id;
-- 1
-- 3
SELECT title FROM pr WHERE title LIKE 'U%' OR title LIKE '_able' ORDER BY title;
-- Cable
-- USB Hub
```

**Listing 1.** Verified on SQLite 3.53.1. BETWEEN keeps both boundaries, IN selects positional members, and LIKE demonstrates both wildcards — `%` swallowing any tail, `_` standing for exactly one character.

```d2
direction: right
i1: "IN (1, 3)
membership, seek per value" {width: 210; height: 80}
i2: "BETWEEN 5 AND 30
inclusive range, one seek" {width: 220; height: 80}
i3: "LIKE 'U%'
pattern; % any run, _ one char
prefix form is seekable" {width: 230; height: 90}
```

**Fig. 1.** Three predicate shapes with three plan stories: set membership, closed range, and prefix pattern — all index-friendly until the pattern leads with a wildcard.

> [!warning] BETWEEN on mixed-type or negated forms surprises
> `BETWEEN '2024-01-01' AND '2024-01-02'` on a timestamp column excludes most of January 2nd (the string bound is midnight) — the inclusive *string* end is not the inclusive *day* end. And NOT IN with a subquery is the NULL trap; prefer NOT BETWEEN deliberately and NOT EXISTS for negated membership ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> IN tests membership in a list or subquery result, BETWEEN is a closed range equivalent to >= AND <= — inclusive on both ends, which my demo shows by returning both boundary prices — and LIKE matches patterns with percent for any run and underscore for one character. All three drive indexes when the column is bare: IN seeks per value, BETWEEN is one range seek, prefix LIKE is a range; a leading wildcard or a function on the column is what kills them. I also mention engine quirks: LIKE case rules differ, and timestamp BETWEEN bounds are midnight-exact.
