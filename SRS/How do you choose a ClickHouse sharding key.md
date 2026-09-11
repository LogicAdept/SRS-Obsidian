<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Replication #SRS

# How do you choose a ClickHouse sharding key?

> [!abstract] Short answer
> The sharding key is the expression a Distributed table uses to route each row to a shard — any expression over the insert block. Choose it for even volume first (often `rand()` or a hash of a high-cardinality id), then for locality: co-locating rows that join or filter together lets queries run local JOIN/IN instead of GLOBAL, which the docs call much more efficient.

## The decision

Two forces pull in opposite directions. Even distribution prevents hot shards — `rand()` spreads uniformly when nothing else matters; `intHash64(user_id)` keeps a user on one shard so their events are co-located; `cityHash64(tenant_id, user_id)` co-locates at tenant grain for bounded cardinality. The locality payoff is concrete: queries joining or filtering on the sharding key resolve on each shard with local IN/JOIN; without co-location, every such query needs GLOBAL variants that broadcast data. Skew is the trap: sharding by a low-cardinality column (country, tenant with one giant customer) puts most rows on few shards; sharding by user_id when one user generates most events has the same effect.

```sql
-- even write load, no locality: analytical scans
CREATE TABLE hits_all AS hits
ENGINE = Distributed(cluster, default, hits, rand());

-- user co-location: per-user queries avoid GLOBAL JOINs
CREATE TABLE events_all AS events
ENGINE = Distributed(cluster, default, events, intHash64(user_id));
```

**Listing 1.** The canonical pair: random sharding for scan workloads, hash-of-id sharding for co-located lookups.

## Consequences to check

The key is fixed at table creation and applies to *new* inserts only — re-sharding means rewriting data, so it deserves the same care as the sort key. Verify balance with per-shard row counts (`clusterAllReplicas` + `system.parts`), and remember the Distributed engine forwards asynchronously: sharding affects where data lands, not delivery guarantees. Replication is orthogonal — each shard independently has its replicas ([[What is ReplicatedMergeTree]]), so the sharding key decides distribution across shards, while replication decides survival within a shard. In ClickHouse Cloud, [[What is SharedMergeTree]] removes the key from your hands entirely.

> [!warning] The sharding key is not the ORDER BY and not the partition key
> Three different layout decisions at one table: shard placement (Distributed), row order per part (ORDER BY), and lifecycle units (PARTITION BY). A common mistake is sharding by date — which also would make writes hot-spot on one shard — or by tenant id without checking tenant sizes. Shard for balance, sort for filters, partition for retention; mixing these up is expensive to undo.

> [!tip] Interview answer
> I pick the sharding key from the query shapes: rand() or a hash when I need even scan throughput, hash of the entity id when queries are per-entity — because co-location turns cross-shard joins into local ones. I check skew against real volumes, accept that re-sharding is a rewrite, and treat replication as a separate decision per shard.
