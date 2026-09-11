<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS

# What is the difference between GIN and GiST indexes in PostgreSQL?

> [!abstract] Short answer
> Both are extensible secondary indexes, but they solve different shapes: GIN is an inverted index — for each element (array item, lexeme, jsonb key) it stores the list of rows containing it, so containment queries are fast and exact. GiST is a balanced tree of lossy signatures — it indexes "regions" of values and answers with candidates that need a heap recheck. GIN is slower to update, GiST is slower to search.

## Mechanism difference

- GIN: value-to-rows inverted lists. A containment query `@>` looks up the elements and intersects row lists. Results are exact — no recheck of the heap for the index condition itself.
- GiST: each entry is a fixed-length signature or bounding shape; overlapping signatures mean the index may report false matches, which PostgreSQL then rechecks against the real row (lossy). For trigram and FTS the signature is a hash-OR bitmap; for range types it is interval overlap structure.

```d2
gin: "GIN\nfast lookups, exact\nslow inserts (pending list)\nbig, build with maintenance_work_mem" {width: 360; height: 120}
gist: "GiST\nlossy candidates + recheck\nfast inserts\nsmaller, supports kNN distance" {width: 340; height: 120}
```

**Fig. 1.** The tradeoff in one picture: GIN pays on writes to win on reads; GiST pays a recheck on reads to stay cheap on writes.

## Where each is used

- GIN: jsonb containment ([[How do you index JSONB in PostgreSQL]]), arrays, `tsvector` full-text search (the documentation calls GIN the preferred text-search index), trigram similarity ([[What is pg_trgm]]).
- GiST: geometric types, range types and exclusion constraints ([[What is an exclusion constraint in PostgreSQL]]), nearest-neighbor `ORDER BY point <-> query` searches, trigram when updates dominate, and SP-GiST-like partitioned variants.

Both methods are extensible — operator classes decide which types they can index — so the comparison is really about two implementation strategies: inverted lists trading update cost for exact lookups, versus signature trees trading rechecks for cheap maintenance. The same fork reappears across the ecosystem: jsonb and arrays default to GIN, geometry and kNN default to GiST, and text search sits in between ([[How does full-text search work in PostgreSQL]]).

Practical tie-breaker for interviews: if the workload is read-mostly and the queries are containment-shaped, GIN's exact lookups win; if the table takes constant updates or you need distance ordering, GiST's cheap maintenance and kNN support win. Neither is "the faster index" in general — the write-read balance decides, and pg_stat_user_tables' update counters plus EXPLAIN timing will tell you which side of the fork you are on.

## Build and maintenance costs

GIN builds benefit strongly from maintenance_work_mem — raising it shortens build time substantially; GiST build time is not sensitive to that parameter. Ongoing GIN writes accumulate in the pending list (fastupdate, bounded by gin_pending_list_limit) and flush as a batch, so occasional reads pay a backlog; GiST writes go straight into the tree while searches pay rechecks. For text search GiST's signature length (siglen) tunes precision against size, and the core verdict stands: GIN first for pure tsvector columns, GiST when update pressure or GiST-only features (kNN, range operators) dominate.

## Practical cost knobs

GIN update cost is smoothed by the pending list (`gin_pending_list_limit`, 4 MB): fastupdate accumulates changes and a later operation flushes them, so reads can occasionally pay the flush. GIN builds benefit strongly from `maintenance_work_mem`. GiST build time is insensitive to that parameter; its precision is tuned via signature length.

> [!warning] GIN pending list can stall reads
> With fastupdate on, one unlucky query may trigger flushing a full pending list and suddenly take seconds. If GIN latency spikes correlate with write bursts, that is the pending list — bound it, or accept periodic flush cost. Also never assume GIN speeds up `SELECT count(*)`: it answers containment, not row counts.

> [!tip] Interview answer
> GIN is an inverted index: exact containment lookups over composite values, heavy writes and larger builds, ideal for jsonb, arrays and full-text search. GiST is a lossy balanced tree of signatures or shapes: cheap updates, candidate results with recheck, and features GIN lacks like kNN and exclusion constraints. Choose by read-write balance and operator set.
