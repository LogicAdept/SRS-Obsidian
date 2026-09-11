<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Replication #SRS

# What is GLOBAL JOIN in ClickHouse?

> [!abstract] Short answer
> With a distributed table, a plain JOIN sends the query to every shard, and each shard runs the right-hand subquery *itself* — producing per-shard right tables that may miss data. `GLOBAL ... JOIN` fixes correctness: the initiating server runs the subquery once, collects the result into a temporary table, and broadcasts that table to every shard — trading network transfer and initiator memory for a complete join.

## The mechanics

On a Distributed table, the planner rewrites the query per shard. Without GLOBAL, the right-hand subquery executes on each shard against that shard's local data — correct only if the right table is fully replicated on every shard or sharded by the join key; otherwise each shard joins against a partial right side, and results are silently wrong. With GLOBAL, the initiator evaluates the subquery against the whole cluster, materializes the result as a temporary table, ships it to every remote server, and each shard joins its local data against the shipped snapshot — one broadcast copy per shard, paid on the initiator's memory and the network. For LEFT and INNER joins the right table is computed by the subquery; for RIGHT joins the left table is computed instead, since the preserved side must be read from shards.

```sql
-- per-shard subquery: each shard sees only its local users
SELECT count()
FROM events_all e JOIN users_all u ON e.user_id = u.id;

-- initiator computes users once, broadcasts temp table
SELECT count()
FROM events_all e GLOBAL JOIN users_all u ON e.user_id = u.id;
```

**Listing 1.** Same query, two execution models — the GLOBAL version is the correct one when `users_all` is itself sharded.

> [!warning] GLOBAL JOIN is a memory and network bomb at scale
> The entire right side is materialized on the initiator and shipped to every shard — a billion-row dimension table means that table replicated N times through one node. Mitigations in order: co-locate by the join key so a plain local JOIN suffices ([[How do you choose a ClickHouse sharding key]]), filter the subquery aggressively before it becomes a temp table, or use dictionaries ([[What is a ClickHouse dictionary]]) for small dimension lookups. Replicated tables under the join also matter — each shard may itself have replicas, so prefer_localhost_replica and shard-local dimension copies keep the fan-out cheap ([[What is ReplicatedMergeTree]]). The docs' warning "be careful when using GLOBAL" is about exactly this cost model.

> [!tip] Interview answer
> Plain JOIN on a distributed table runs the right-side subquery per shard against local data — fast but incomplete when the right table is sharded. GLOBAL JOIN computes the subquery once on the initiator, broadcasts the temporary result to every shard, and joins locally — correct but O(N) network and initiator memory. The real fix is sharding by the join key to avoid needing GLOBAL at all.
