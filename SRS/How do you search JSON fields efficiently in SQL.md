<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #Databases/Relational/PostgreSQL #SRS

# How do you search JSON fields efficiently in SQL?

> [!abstract] Short answer
> Match the operator to the index. Containment — documents that include this sub-document or value — uses jsonb operators @>, ?, and path queries against a GIN index (jsonb_ops or jsonb_path_ops). Scalar equality on one extracted field uses a B-tree expression index over the accessor. Full lexical search over text inside JSON belongs to full-text search over an extracted tsvector. Plain json cannot be indexed at all — convert to jsonb.

## The three query families

```sql
-- 1. containment (GIN-served)
SELECT * FROM docs WHERE body @> '{"author": "kim", "tags": ["sale"]}';
SELECT * FROM docs WHERE body ? 'isbn';

-- 2. scalar path (B-tree expression-served)
SELECT * FROM docs WHERE body->>'year' = '2026';

-- 3. lexical search inside documents
SELECT * FROM docs
WHERE to_tsvector('english', body->>'abstract')
      @@ websearch_to_tsquery('english', 'index scans');
```

**Listing 1.** Containment, scalar access, and text search are three different index problems ([[How do you index JSONB in PostgreSQL]], [[What is an expression index in PostgreSQL]], [[How does full-text search work in PostgreSQL]]).

```d2
q: "JSON search need" {width: 220; height: 60}
c: "Has this content?\n@>, ?, path" {width: 280; height: 70}
s: "Field equals X\n->> accessor" {width: 260; height: 70}
t: "Text relevance in fields" {width: 280; height: 70}
gin: "GIN over jsonb" {width: 240; height: 60}
bt: "B-tree on expression" {width: 260; height: 60}
fts: "tsvector + GIN" {width: 250; height: 60}
q -> c -> gin
q -> s -> bt
q -> t -> fts
```

**Fig. 1.** The routing table: three needs, three index structures.

## Operator semantics worth naming

- `@>` containment: the left value contains the right as a sub-structure — arrays must contain all listed elements, objects all listed key-value pairs. Direction matters; the mirrored `<@` is "is contained in".
- `?` family: top-level key existence (`?`), any (`?|`), all (`?&`) — jsonb_ops only.
- SQL/JSON path (`jsonb_path_query`, the `@@` and `@?` operators) supports exists-predicates with GIN support via jsonb_path_ops-class machinery for `@?`/`@@` queries.

## Design guidance

Store documents as jsonb ([[What is the difference between JSON and JSONB in PostgreSQL]]); extract high-frequency filter fields into real columns when they become relational facts — columns are cheaper than deep paths, and statistics exist for them ([[How do stale statistics hurt a query plan]]). The trap inventory of mixing operators without indexes is the same as the general "index unused" story ([[Why might PostgreSQL choose a sequential scan instead of an index]]).

> [!warning] JSON path syntax is not an index strategy
> Writing `body->'tags'->'items'->>'name' = 'x'` with a GIN index over body produces a full scan: GIN answers containment, not chained accessors. Either restate as containment (`body @> '{"tags": {"items": [{"name": "x"}]}}'` — mind array semantics) or build a B-tree on the exact accessor. The operator-to-index mismatch is the number-one JSONB performance bug.

> [!tip] Interview answer
> Three families: containment with @>, ? and path-existence operators served by a GIN index over jsonb — jsonb_path_ops when you only need @>; scalar equality on extracted fields served by B-tree expression indexes; and lexical relevance via a tsvector over the field with FTS. Chained accessor paths match none of these indexes — restate as containment or add an expression index.
