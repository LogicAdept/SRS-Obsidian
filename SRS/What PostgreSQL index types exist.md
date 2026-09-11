<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS

# What PostgreSQL index types exist?

> [!abstract] Short answer
> Six access methods ship with PostgreSQL: B-tree (default, ordered equality and range), hash (fast equality only), GiST (extensible tree for geometric, ranges, nearest-neighbor), SP-GiST (space-partitioned trees for non-balancing structures like quadtrees and radix trees), GIN (inverted index for containment in composite values like jsonb, arrays, tsvector), and BRIN (compact block-range summary for huge append-only tables).

## The six methods at a glance

| Method | Fits | Typical ops |
|---|---|---|
| B-tree | scalars, sortable types | =, <, >, BETWEEN, LIKE prefix, sorting |
| hash | scalars | = only |
| GiST | geometric, range types, trigram, kNN | &&, @>, distance ORDER BY |
| SP-GiST | partitions of space, IP prefixes, text | non-overlapping structures |
| GIN | jsonb, arrays, tsvector | containment @>, ?, match |
| BRIN | huge append-only, physical correlation | min/max per block range |

```sql
CREATE INDEX ON products (name);                        -- B-tree by default
CREATE INDEX ON products USING hash (code);             -- equality-heavy code lookups
CREATE INDEX ON meetings USING gist (during);           -- range overlap
CREATE INDEX ON docs USING gin (body jsonb_path_ops);   -- jsonb containment
CREATE INDEX ON telemetry USING brin (ts);              -- 10+ TB time series
```

**Listing 1.** The same table can carry indexes of different methods; the planner picks per query ([[What is a query plan in a relational database]]).

```d2
bt: "B-tree\nordered, versatile, unique support" {width: 320; height: 80}
gin: "GIN\ninverted: value -> row list" {width: 300; height: 80}
gist: "GiST / SP-GiST\nextensible trees, lossy recheck" {width: 320; height: 80}
brin: "BRIN\nblock-range min/max, tiny" {width: 300; height: 80}
```

**Fig. 1.** Mental buckets: ordered (B-tree), inverted (GIN), extensible (GiST/SP-GiST), compressed summary (BRIN).

## Choosing in practice

Default to B-tree; it is the only method supporting unique constraints and the broadest operator set. Reach for GIN when containment inside documents or arrays is the query ([[What is the difference between GIN and GiST indexes in PostgreSQL]]), GiST for ranges, geometry and kNN, BRIN when the physical order of a giant table tracks the indexed column (append-only time series). Hash earns its keep only for pure equality on very wide keys. The generic decision process lives in [[How do you decide which database indexes to create]] and [[How do database indexes work at a high level]].

> [!warning] "Index" does not mean B-tree everywhere
> The planner can only use an index for operators that the method's operator class supports: a GIN index does not answer range queries, a BRIN index cannot find arbitrary rows (only block ranges, with a recheck), and a hash index never helps ORDER BY. Creating "an index" on the right column with the wrong method answers nothing.

> [!tip] Interview answer
> PostgreSQL has six index methods: B-tree as the ordered default, hash for equality, GiST and SP-GiST as extensible trees for geometry, ranges and kNN, GIN as the inverted index for containment on jsonb, arrays and tsvector, and BRIN as a tiny block-range summary for huge append-only tables. The query operators decide the method, not habit.
