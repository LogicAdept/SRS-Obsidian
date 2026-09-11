<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Replication #SRS

# What is SharedMergeTree?

> [!abstract] Short answer
> SharedMergeTree is the cloud-native replacement for the Replicated* engines that powers ClickHouse Cloud: parts live once in shared object storage (S3/GCS/Azure), coordination and metadata go through clickhouse-keeper, and replicas stop copying data to each other entirely — asynchronous leaderless replication with hundreds of compute nodes per table.

## What changed versus ReplicatedMergeTree

In [[What is ReplicatedMergeTree]], every replica holds a full copy of [[What is a data part in ClickHouse]] *and* a copy of the metadata, so every write, merge, and mutation must be replicated replica-to-replica. SharedMergeTree stores data parts once in object storage and keeps metadata in Keeper; replicas communicate only through shared storage plus Keeper, so adding compute copies no data and no metadata. The documented benefits follow directly: higher insert throughput, faster background merges and mutations, faster scale up/down, and "more lightweight strong consistency for SELECT queries". Every MergeTree variant has a Shared analog (SharedReplacingMergeTree, SharedAggregatingMergeTree, ...), and it is enabled by default in Cloud — you write plain `CREATE TABLE ... ENGINE = MergeTree` and the platform maps it.

```d2
rpt: "ReplicatedMergeTree\nN full copies of parts\n+ N copies of metadata" {
  width: 340
  height: 100
  style.fill: "#ffebee"
}
smt: "SharedMergeTree\n1 copy of parts in object storage\nmetadata in Keeper" {
  width: 360
  height: 100
  style.fill: "#e8f5e9"
}
compute1: "compute node 1" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
compute2: "compute node 2" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
compute3: "compute node N...\nhundreds of replicas" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
smt -> compute1
smt -> compute2
smt -> compute3: stateless compute reads shared parts
```

**Fig. 1.** Storage-shared versus copy-everywhere: compute scales without replicating parts or metadata.

## Introspection differences

Most ReplicatedMergeTree system tables exist, but the replication queues are gone — there is nothing to replicate. `system.virtual_parts` replaces `system.replication_queue` (current and in-progress parts: merges, mutations, dropped partitions), and `system.shared_merge_tree_fetches` replaces `system.replicated_fetches` (primary key/checksum fetches into memory). Operational muscle memory changes accordingly: instead of watching replication lag, you watch part states and fetch activity; recovery semantics change because data is never lost with a node — it is lost only if object storage is.

> [!warning] SharedMergeTree is a Cloud architecture, not a self-hosted flag
> The engine family is how ClickHouse Cloud works; self-managed deployments still use ReplicatedMergeTree over Keeper. Interview answers that propose "turning on SharedMergeTree" in a self-hosted cluster misunderstand the model — the equivalent self-hosted move is object-storage disks plus [[What is ReplicatedMergeTree]], which still replicates metadata per replica.

> [!tip] Interview answer
> SharedMergeTree is the decoupled-storage evolution of ReplicatedMergeTree: parts stored once in object storage, metadata in Keeper, no replica-to-replica copying — async leaderless replication that lets Cloud scale to hundreds of compute replicas per table with faster inserts, merges, and mutations. Same MergeTree semantics, different replication architecture.
