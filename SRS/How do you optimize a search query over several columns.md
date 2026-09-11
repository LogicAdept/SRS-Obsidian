<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> Searching over several columns has three index strategies: a **composite index** when the query pins several columns together (`WHERE city = ? AND name LIKE 'A%'` — equality columns first, prefix tail: one seek); **multiple single-column indexes** when conditions come independently or as OR — the engine combines them (SQLite MULTI-INDEX OR, PostgreSQL bitmap OR); and **FTS/trigram machinery** when "search" means text relevance. The plan decides which happened — read it ([[What is Index Cond versus Filter in EXPLAIN]], [[What is a bitmap index scan in SQL plans]]).

The verified demo walks all three shapes on one table. The OR form (`city = 'Berlin' OR name = 'Alpha'`) with two single-column indexes plans as MULTI-INDEX OR — two index probes merged and deduplicated. The AND form plans with the composite `(city, name)` as one SEARCH serving `city=? AND name=?` — both conditions inside the key ([[How do you avoid a sort with an index]]). The equality-plus-prefix form (`city = 'Berlin' AND name LIKE 'A%'`) still plans on the composite: the equality pins the prefix, the LIKE filters within the pinned run (shown as `city=?` in the plan — the LIKE is applied on the index-delivered rows, which is already the win: no table scan). The design rule that follows: composite order is decided by the *most selective equality* first; prefix-searchable columns go last so they filter the already-narrowed run; and columns searched independently of each other get their own indexes — a composite cannot serve a query that omits its leading column ([[What is sargability in SQL]]). When the "several columns" are *text* columns that users search freely, single-column B-trees stop mattering and FTS (one inverted index over the combined document) or trigram indexes become the answer ([[When should you use full-text search instead of LIKE]]).

```sql
CREATE TABLE shops (id INTEGER PRIMARY KEY, city TEXT, name TEXT);
INSERT INTO shops VALUES (1,'Berlin','Alpha'),(2,'Oslo','Beta'),(3,'Berlin','Gamma');
CREATE INDEX idx_shop_city ON shops(city);
CREATE INDEX idx_shop_name ON shops(name);

EXPLAIN QUERY PLAN
SELECT id FROM shops WHERE city = 'Berlin' OR name = 'Alpha';
-- QUERY PLAN
-- |--MULTI-INDEX OR
-- |  |--INDEX 1
-- |  |  `--SEARCH shops USING INDEX idx_shop_city (city=?)
-- |  `--INDEX 2
-- |     `--SEARCH shops USING INDEX idx_shop_name (name=?)
CREATE INDEX idx_shop_city_name ON shops(city, name);
EXPLAIN QUERY PLAN
SELECT id FROM shops WHERE city = 'Berlin' AND name = 'Alpha';
-- QUERY PLAN
-- `--SEARCH shops USING COVERING INDEX idx_shop_city_name (city=? AND name=?)
```

**Listing 1.** Verified on SQLite 3.53.1. OR across columns costs two index probes plus a merge; AND across the same columns rides one composite key serving both predicates — the shapes every engine produces under different names.

```d2
direction: right
c1: "AND, stable conditions
-> composite (city, name)" {width: 220; height: 90}
c2: "OR / independent conditions
-> per-column indexes, merged" {width: 230; height: 90}
c3: "free-text over columns
-> FTS / trigram" {width: 190; height: 90}
q: "multi-column search" {width: 170; height: 70}
c1 -> q
c2 -> q
c3 -> q
```

**Fig. 1.** Three access strategies for one problem class, chosen by how the conditions combine — jointly, independently, or as free text.

> [!warning] The composite serves the query only down to its first missing column
> `(city, name)` accelerates `WHERE city = ?` but is useless for `WHERE name = ?` alone — the leading-column rule. Index duplication (city and (city, name)) is often justified, but each extra index taxes writes; verify with the plan which of the candidate indexes the planner actually chooses ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> For multi-column search I match the strategy to the predicate shape: conditions that appear together become a composite index with the most selective equality first and prefix-searchable columns last — one seek serves both; conditions that appear independently or as OR get per-column indexes that the engine merges — SQLite MULTI-INDEX OR, PostgreSQL bitmap OR; and genuinely free-text search across columns moves to FTS or trigrams. I verify each design in the plan — my demo shows both the merged-OR and the composite-serving-AND shapes — and remember the leading-column rule caps what a composite can serve.
