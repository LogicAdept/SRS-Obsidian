<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is pgvector in PostgreSQL?

> [!abstract] Short answer
> An open-source extension adding a vector data type with up to 16,000 float dimensions, distance operators (L2, inner product, cosine, L1, Hamming, Jaccard), and approximate-nearest-neighbor indexes — HNSW graph and IVFFlat — so embedding search runs in ordinary SQL inside PostgreSQL. It is the default choice when embeddings belong to the same transactional data as everything else; at very large scale or extreme QPS, dedicated vector databases still have room.

## The surface

```sql
CREATE EXTENSION vector;
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(768));

INSERT INTO items (embedding) VALUES ('[0.1, -0.2, ...]');

-- exact search: 5 nearest by cosine distance
SELECT id FROM items ORDER BY embedding <=> '[0.1, -0.2, ...]' LIMIT 5;

-- ANN index: HNSW (better speed-recall, no training step)
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);
-- or IVFFlat (train on data: lists clusters)
CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

**Listing 1.** Type, operators, exact kNN, and the two index families; per the project's documentation HNSW trades slower builds and more memory for better query performance, and can be built on an empty table.

```d2
q: "Query vector" {width: 220; height: 60}
ex: "Exact scan\nevery row, perfect recall" {width: 300; height: 80}
ann: "HNSW / IVFFlat\napproximate, fast, tunable recall" {width: 340; height: 80}
idx: "CREATE INDEX USING hnsw / ivfflat" {width: 330; height: 70}
q -> ex
q -> idx -> ann
```

**Fig. 1.** Small tables answer exactly; at scale you accept approximate recall for speed via the index.

## The operators and types

- Distances: L2, inner product, cosine, L1, Hamming, Jaccard; operators for cosine and L2 in the listings above, inner product in the project docs — all usable in ORDER BY ... LIMIT k queries.
- Types: vector (4 bytes per dim, up to 16,000 dims), halfvec (2 bytes, fp16, up to 16,000), sparsevec (non-zero storage), bit — the half-precision and sparse variants cut index memory substantially.
- Storage is ordinary: `4 * dimensions + 8` bytes per vector; TOAST applies ([[What is TOAST in PostgreSQL]] — wide embedding rows go out of line).

## When it fits

Embeddings live beside the documents they describe; updates and filters ("same tenant, same language, nearest neighbor") are one SQL statement with RLS ([[What is row-level security in PostgreSQL]]) — the join-and-filter story is where standalone vector stores get awkward. Recall/performance tuning (hnsw parameters, lists, probes) is a real tuning exercise ([[How do you decide which database indexes to create]] — the same measure-then-keep discipline).

> [!warning] ANN means approximate — and unindexed means O(n)
> Without an index every query scans all rows; with HNSW/IVFFlat you trade recall for speed and must measure it. The second trap: mixing distance metrics between query and index operator class silently returns wrong nearest neighbors — the index class (vector_cosine_ops versus vector_ip_ops) must match the operator in the query.

> [!tip] Interview answer
> pgvector makes PostgreSQL a vector store: a 16,000-dim float vector type, distance operators for L2, cosine, inner product and friends, and ANN indexes — HNSW graphs and IVFFlat clusters — with half-precision and sparse variants. Exact search for small sets, indexed ANN at scale with tuned recall. It shines when vectors belong to the same transactional data as the rest of the schema.
