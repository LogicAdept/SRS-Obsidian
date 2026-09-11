<!--
reps: 0
priority: 0
-->
#Databases/Sharding #SystemDesign/Scalability #DistributedSystems #SRS

# How would you explain horizontal database sharding

> [!abstract] Short answer
> Horizontal sharding splits a table's rows across independent database servers by a shard key: each shard holds a disjoint subset of rows with the same schema, and a routing layer maps each query to the shard(s) owning its key range or hash. Shards are typically replicated for availability; the shard key — a user id, tenant, or hash of it — is the design decision everything else hangs on.

## Mechanics: key, routing, replication

Two splitting schemes dominate. Range sharding assigns contiguous key ranges to shards (users 1–1M to shard A) — range scans stay local and hotspots follow the data distribution; MongoDB chunks are exactly non-overlapping key ranges, and it supports both ranged and hashed shard keys, warning that monotonic keys concentrate inserts on one shard. Hash sharding applies a hash to the key and distributes by hash value — uniform spread and even write load, at the cost of losing key adjacency (range scans become scatter-gather). Routing happens in a coordinator (proxy or query router), at the driver level, or via partition metadata the client resolves — the same client-side-vs-coordinator split as service discovery. Because a shard is an ordinary server that can die, each is replicated (primary + replicas per shard); the sharded fleet combines [[How would you explain database replication strategies]] per shard with [[What problem does database sharding solve]]'s row-splitting across shards.

```text
shard key = user_id
hash(user_id) % N  (or consistent hashing)  -> shard id
shard A: user_id in [1..1M)      range sharding
shard B: user_id in [1M..2M)
query WHERE user_id = 42        -> 1 shard (fast, key-routed)
query WHERE country = 'DE'      -> all shards (scatter-gather)
```

**Listing 1.** Key-based routing: one shard for keyed lookups, full fan-out without the key.

## Relational sharding in practice

On engines without native sharding, the pattern is application-managed: a sharding middleware or library holds the key-to-shard map, each shard is a normal PostgreSQL/MySQL primary with its replicas, and schemas embed the key. Costs to state explicitly: cross-shard JOINs move to the application or become ETL jobs; global uniqueness needs composite keys (shard id embedded) or a coordinator; cross-shard transactions need 2PC or are redesigned as per-shard transactions plus saga-style compensation; rebalancing moves ranges while serving. Purpose-built engines take these costs on themselves — MongoDB routes and rebalances chunks automatically, Citus spreads PostgreSQL tables across nodes declaratively, and ClickHouse distributes inserts over a cluster by sharding key ([[How do you choose a ClickHouse sharding key]]). [[How do you design good database partitioning]] treats the pre-sharding question of whether partitioning within one node already suffices.

> [!warning] Hashing alone does not save a hot entity
> A celebrity user, a viral tenant or a time-monotonic key concentrates load on one shard regardless of how even the hash is across users. Mitigations — salting the key, splitting hot ranges, caching the hot row — must be planned, because the shard owning the hot key is the ceiling of the whole system.

> [!tip] Interview answer
> Horizontal sharding splits rows by a shard key across independent, replicated servers: ranges keep scans local, hashes spread load evenly, and a router sends keyed queries to one shard. It scales writes and working set linearly, while un-keyed queries fan out and cross-shard transactions need coordination — so the shard key is chosen from the dominant queries first.
