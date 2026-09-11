<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DataTypes #SRS

# What is the difference between JSON and JSONB in PostgreSQL?

> [!abstract] Short answer
> json stores the exact input text — whitespace, key order and duplicate keys preserved — and reparses it on every operation; jsonb stores a decomposed binary representation — normalized, no key order, last duplicate wins — which is slower to write but much faster to query and the only one that supports indexing. The documentation's advice: most applications should use jsonb.

## The two representations

| | json | jsonb |
|---|---|---|
| Storage | exact text copy | decomposed binary |
| Whitespace, key order | preserved | discarded |
| Duplicate keys | all kept (last wins in functions) | last wins |
| Query speed | reparse per operation | direct access |
| Indexing | none | GIN (jsonb_ops, jsonb_path_ops) |
| Number limits | unlimited text | PostgreSQL numeric range |

```sql
SELECT '{"b": 2,  "a": 1, "a": 3}'::json;
-- {"b": 2,  "a": 1, "a": 3}          -- text as sent
SELECT '{"b": 2,  "a": 1, "a": 3}'::jsonb;
-- {"a": 3, "b": 2}                   -- normalized: sorted, last duplicate kept
```

**Listing 1.** The canonical demo: same literal, two results. Querying and indexing mechanics are in [[How do you index JSONB in PostgreSQL]]; searching patterns in [[How do you search JSON fields efficiently in SQL]].

```d2
in: "Input JSON text" {width: 220; height: 60}
j: "json\nverbatim text\nreparse on every read" {width: 300; height: 80}
jb: "jsonb\nbinary tree of elements\nparse once at input" {width: 310; height: 80}
idx: "GIN index support\n@> containment, ?, path queries" {width: 340; height: 80}
in -> j
in -> jb -> idx
```

**Fig. 1.** jsonb pays conversion at write time to buy query and index speed at read time.

## Why jsonb usually wins

Containment operators (`@>`, `?`), SQL/JSON path queries, and GIN indexes only work on jsonb. Reads avoid reparsing. The normalization also makes equality comparisons meaningful (`'{"a":1,"b":2}'::jsonb = '{"b":2,"a":1}'::jsonb` is true). The costs are slightly slower input, loss of key order, and numeric-range limits (jsonb maps numbers onto PostgreSQL numeric — a very large or precisely formatted number may still fit, but NaN-style input is rejected).

## When json still fits

- You must store the document byte-for-byte (legal, auditing, external system payloads) and only ever fetch it whole.
- Logs of raw payloads where content preservation matters and no in-database querying happens.

> [!warning] jsonb does not preserve everything you sent
> Key order, duplicate keys and whitespace are gone by design. Code that round-trips jsonb and compares strings, or that relies on key order of the original document, breaks. And mixing the two types in one column family produces plans where indexes silently cannot exist ([[Why might PostgreSQL choose a sequential scan instead of an index]]).

> [!tip] Interview answer
> json keeps the exact input text and reparses it per operation; jsonb parses once into a normalized binary form — no key order, last duplicate wins — enabling fast operators and GIN indexing. Storage: jsonb is the default choice; json only for verbatim archival where you never query inside the document.
