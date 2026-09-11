<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS

# How do you index JSONB in PostgreSQL?

> [!abstract] Short answer
> For containment queries build a GIN index over the jsonb column: plain `USING gin (col)` supports the default `jsonb_ops` operator class (containment, key and path existence), while `jsonb_path_ops` supports only `@>` but is smaller and faster for it. For scalar lookups on a specific field use a B-tree expression index on `col->>'field'`. jsonb is the type that supports indexing — plain json does not.

## The two patterns

```sql
-- 1. containment: "documents having this nested content"
CREATE INDEX docs_body_gin ON docs USING gin (body);
CREATE INDEX docs_body_gin_path ON docs USING gin (body jsonb_path_ops);

-- queries served:  body @> '{"tags": [{"name": "sale"}]}'
--                  body ? 'user_id'            (jsonb_ops only)

-- 2. scalar equality on one field
CREATE INDEX docs_sku_idx ON docs ((body->>'sku'));
SELECT * FROM docs WHERE body->>'sku' = 'A-17';   -- B-tree
```

**Listing 1.** Containment goes to GIN; exact-value lookups on one accessor go to a B-tree over the expression ([[What is an expression index in PostgreSQL]]).

```d2
q: "Query style" {width: 200; height: 60}
cont: "Containment / existence\n@>, ?, @?, @@ path queries" {width: 330; height: 80}
scal: "Single scalar field\nequality / range" {width: 300; height: 80}
gin: "GIN (body)\njsonb_ops or jsonb_path_ops" {width: 300; height: 80}
btree: "B-tree on (body->>'field')" {width: 300; height: 80}
q -> cont -> gin
q -> scal -> btree
```

**Fig. 1.** The decision is by operator: containment operators live in GIN; scalar comparisons live in B-tree.

## jsonb_ops versus jsonb_path_ops

`jsonb_ops` (default) indexes every key and value, supports `?` existence operators and `@>`; `jsonb_path_ops` indexes only hashes of full value paths, supports only `@>`, but produces a substantially smaller index and faster lookups when keys are many and queries are pure containment. Write cost and pending-list behavior of GIN apply to both ([[What is the difference between GIN and GiST indexes in PostgreSQL]]). The language-side query tooling for these operators is in [[How do you search JSON fields efficiently in SQL]] and the storage type comparison in [[What is the difference between JSON and JSONB in PostgreSQL]].

## Limits

- `json` (not jsonb) cannot be indexed this way — no containment operators, no GIN support; convert to jsonb ([[What is the difference between JSON and JSONB in PostgreSQL]]).
- A GIN index cannot answer "rows where field X is missing" efficiently nor range scans on values; those need expression B-trees or a relational redesign.
- Wide documents make fat GIN indexes; the write amplification on insert-heavy jsonb tables is a real cost ([[How do you decide which database indexes to create]]).

> [!warning] The operator must match the index, not just the JSON path
> `body->>'sku' = 'A-17'` does not use the GIN index, and `body @> '{"sku": "A-17"}'` does not use the B-tree expression index. Mixing them up produces a seq scan over your whole document table ([[Why might PostgreSQL choose a sequential scan instead of an index]]).

> [!tip] Interview answer
> Two patterns: GIN over the jsonb column for containment and existence — default jsonb_ops for full operator support, jsonb_path_ops when you only need the @> operator and want a smaller, faster index; and B-tree expression indexes on single accessors like body-field for scalar lookups. Plain json cannot be indexed at all, and the query operator must match the index type.
