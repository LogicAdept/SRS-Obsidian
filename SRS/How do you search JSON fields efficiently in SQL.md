<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> JSON in SQL is queried with a path language, not LIKE: `json_extract(col, '$.city')` (SQLite/MySQL), the `->`/`->>` operators (PostgreSQL/SQLite), `JSON_VALUE` (SQL Server). Efficient search means **indexing the extracted path** — an expression index on the path, or a generated column with an index — turning `WHERE json_extract(data, '$.city') = 'Berlin'` into a seek. Scanning raw JSON text per row is the anti-pattern ([[What is sargability in SQL]]).

The verified demo covers the full arc on SQLite: `json_extract(data, '$.city')` pulls the scalar from a TEXT-stored JSON document; creating an expression index on that *same expression* upgrades the equality search to `SEARCH profiles USING COVERING INDEX idx_city (<expr>=?)` — the JSON path behaves like any other indexed key because the extraction ran once per row at index build time ([[Why does a function on a column prevent index use]]). PostgreSQL's production equivalents: `->` returns json(b), `->>` returns text; GIN indexes over the jsonb document (`CREATE INDEX ON t USING GIN (data)` with jsonb_ops or jsonb_path_ops) answer containment queries (`data @> '{"city": "Berlin"}'`) from the index — the documented approach for "search inside JSON" at scale; expression indexes on `data->>'city'` serve equality seeks. The design trade worth stating: JSON columns trade schema for flexibility — validation moves to application or CHECK(json_valid(...)) constraints, and every indexed path is a hand-maintained schema decision; the moment paths multiply and dominate queries, the columns want promotion to real columns ([[How do you alter a table in a relational database]], [[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE profiles (id INTEGER PRIMARY KEY, data TEXT);
INSERT INTO profiles VALUES
 (1, '{"city": "Berlin", "age": 30}'), (2, '{"city": "Oslo", "age": 25}');

SELECT id, json_extract(data, '$.city') FROM profiles ORDER BY id;
-- 1|Berlin
-- 2|Oslo
CREATE INDEX idx_city ON profiles(json_extract(data, '$.city'));
EXPLAIN QUERY PLAN
SELECT id FROM profiles WHERE json_extract(data, '$.city') = 'Berlin';
-- QUERY PLAN
-- `--SEARCH profiles USING COVERING INDEX idx_city (<expr>=?)
SELECT data -> '$.city' FROM profiles WHERE id = 1;
-- "Berlin"
```

**Listing 1.** Verified on SQLite 3.53.1. Path extraction, its indexed (seekable) form, and the `->` operator spelling — JSON search upgraded from per-row parsing to an index probe.

```d2
direction: right
j: "JSON document
TEXT / jsonb" {width: 170; height: 80}
p: "path extraction
$.city -> 'Berlin'" {width: 190; height: 80}
i: "expression index / GIN
path value -> rows" {width: 200; height: 80}
q: "WHERE path = x
-> index seek" {width: 160; height: 70}
j -> p -> i -> q
```

**Fig. 1.** JSON search efficiency is an indexing decision on the *extracted* value: parse once at index time, seek thereafter — instead of parsing every document on every query.

> [!warning] Every indexed JSON path is an implicit schema — unowned and drifting
> Without a registry, five services index five spellings of the same path and the "flexible" document model accretes shadow columns nobody owns. Treat indexed paths as schema objects: named, documented, migration-managed — or promote the field to a real column when it becomes load-bearing ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> JSON fields are searched with path extraction — json_extract or the arrow operators — and made efficient by indexing the extracted value: my demo shows an expression index on $.city turning the equality into a covering-index seek, and PostgreSQL offers the same via expression indexes or GIN over jsonb for containment queries. The caveat I add: each indexed path is an implicit, drifting schema — I register them like columns and promote hot ones to real columns, because JSON's flexibility is for the tail of the schema, not its spine.
