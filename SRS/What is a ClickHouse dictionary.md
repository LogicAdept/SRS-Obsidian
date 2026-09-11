<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is a ClickHouse dictionary?

> [!abstract] Short answer
> A dictionary is a server-side in-memory lookup object loaded from an external source — ClickHouse, PostgreSQL, MySQL, HTTP, a local file — defined with `CREATE DICTIONARY` via `SOURCE`, `LAYOUT`, `LIFETIME`, and `PRIMARY KEY`. Queries enrich rows with `dictGet('dict', 'attr', key)` at milliseconds cost, avoiding JOINs against remote dimension tables — the co-location alternative is sharding by the join key ([[How do you choose a ClickHouse sharding key]]).

## Mechanics

`LAYOUT` picks the in-memory structure: `FLAT` (dense UInt64 keys, fastest), `HASHED`/`COMPLEX_KEY_HASHED` (arbitrary keys, everything in RAM), `CACHE` (bounded cache with misses hitting the source), `RANGE_HASHED` (range lookups on dates/numbers), `DIRECT` (pass-through to the source), among others. `LIFETIME(MIN 600 MAX 900)` sets the refresh interval window (jittered); `INVALIDATE_QUERY` can refresh only on real changes. The source query loads the whole dictionary at startup/refresh — the docs' worked example loads a multi-million-row dimension in tens of seconds and GBs of RAM, which is why layouts and key types are chosen deliberately. Dictionaries also join implicitly: a `JOIN` against a dictionary uses its layout instead of a hash-join build.

```sql
CREATE DICTIONARY users_dict
(
    id UInt64,
    location String
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(QUERY 'SELECT Id, Location FROM users'))
LIFETIME(MIN 600 MAX 900)
LAYOUT(HASHED());

SELECT Id, dictGet('users_dict', 'location', toUInt64(Id)) AS location
FROM posts;
```

**Listing 1.** A hashed dictionary over a ClickHouse source with a 10–15 minute refresh window, and its point-lookup usage.

## When they beat JOINs

Dimension lookups at insert time (enriching event streams), per-row enrichment in dashboards, and id-to-name resolution across distributed queries — cases where a JOIN would shuffle the big table or run a remote subquery per shard ([[What is GLOBAL JOIN in ClickHouse]]). On self-managed clusters the dictionary must be created on every node; in ClickHouse Cloud it replicates automatically. The introspection tables (`system.dictionaries`, `system.dictionaries_*`) expose memory, load times, and hit/miss counters for cache layouts.

> [!warning] A HASHED dictionary is a full copy in RAM — on every node
> The docs' example: a 36-second load and tens of GB resident, multiplied by every server that queries it. Unbounded growth is the failure mode: dimensions that keep growing turn dictionaries into the cluster's memory ceiling, and CACHE layouts trade that for miss latency that can exceed a JOIN. Size the dimension first (`SELECT uniqExact(id)`), and keep refresh windows realistic — a stale dictionary silently serves old values within its LIFETIME.

> [!tip] Interview answer
> Dictionaries are managed in-memory lookup tables from external sources, chosen by LAYOUT — flat/hashed for full-in-RAM speed, cache for big dimensions, range for temporal validity — refreshed on a LIFETIME window and read with dictGet. They replace distributed dimension JOINs for enrichment, at the cost of RAM per node and refresh lag.
