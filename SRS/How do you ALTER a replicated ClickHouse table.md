<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Replication #SRS

# How do you ALTER a replicated ClickHouse table?

> [!abstract] Short answer
> Schema changes (`ADD COLUMN`, `MODIFY COLUMN`, `ADD INDEX`, TTL changes) are metadata operations: issue the ALTER on any replica, ClickHouse stores the command in Keeper, and every replica applies it to its own parts — no data rewrite for additive changes. Data-changing ALTERs (mutations like `UPDATE`/`DELETE`, `MATERIALIZE INDEX`) also replicate, running asynchronously on each replica.

## What replicates and how

Replication is per-table through [[What is ReplicatedMergeTree]] and [[What is ClickHouse Keeper]]: for schema ALTERs, the command is logged in Keeper and each replica applies it locally — adding a column is instant because new columns are virtual defaults until parts are rewritten. Heavy operations — mutations ([[What are mutations in ClickHouse]]) and materializations — enter the `replication_queue` on every replica and rewrite parts independently, visible in `system.mutations` per node. The non-replicated exceptions matter operationally: `CREATE`, `DROP`, `ATTACH`, `DETACH`, and `RENAME` execute on a single server only — to create or drop a table everywhere you use `ON CLUSTER` distributed DDL, which itself is delivered through Keeper.

```sql
-- schema change: run on ONE replica, applies everywhere
ALTER TABLE hits ON CLUSTER main ADD COLUMN region LowCardinality(String);

-- data change: a replicated mutation, tracked per replica
ALTER TABLE hits ON CLUSTER main UPDATE region = 'unknown' WHERE region = '';

SELECT hostName(), command, is_done
FROM clusterAllReplicas('main', system.mutations)
WHERE table = 'hits' AND NOT is_done;
```

**Listing 1.** Metadata ALTER versus replicated mutation, and the cross-replica check of mutation progress.

## Design so ALTERs stay cheap

The cost profile follows from the mechanism: additive schema changes (`ADD COLUMN`, adding an index definition, relaxing a TTL) are metadata-only — the new column exists virtually and materializes only when a merge or a `MATERIALIZE COLUMN` mutation rewrites the part, exactly the pattern [[How do you add a column to a large PostgreSQL table without downtime]] implements with defaults on the row-store side. Narrowing types, changing the sort key, or dropping columns with data force part rewrites, so they inherit every constraint of [[What are mutations in ClickHouse]] — schedule them, scope them per partition where possible, and keep the queue short. On sharded clusters, run DDL with `ON CLUSTER` and idempotent guards (`IF NOT EXISTS` / `IF EXISTS`) so retries after a partial apply are safe.

> [!warning] ALTERs need Keeper — and they queue behind it
> When Keeper is unreachable, replicated tables are read-only, so ALTERs fail along with INSERTs; and because mutations are asynchronous per replica, a "done" ALTER on the node you queried can still be running elsewhere — always check `system.mutations`/`replication_queue` cluster-wide before assuming completion. Also remember `RENAME` is single-server on replicated tables: renaming everywhere is a DROP/CREATE dance, not a replicated statement.

> [!tip] Interview answer
> On ReplicatedMergeTree, schema ALTERs are replicated metadata commands applied by every replica from Keeper — additive columns are instant since parts keep defaults until rewritten. Mutations and MATERIALIZE operations replicate as per-replica part rewrites tracked in system.mutations, while CREATE/DROP/RENAME never replicate and need ON CLUSTER. And all of it depends on Keeper being alive.
