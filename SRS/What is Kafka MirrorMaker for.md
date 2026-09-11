<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is Kafka MirrorMaker for?

> [!abstract] Short answer
> Replicating data between Kafka clusters: MirrorMaker 2 consumes from a source cluster and produces into a target one, copying topics, topic configs, ACLs, and — through checkpoint connectors — consumer group offsets, with translated positions. Typical shapes: active-passive disaster recovery and active-active aggregation across regions ([[What are the main components of Apache Kafka]]).

## How MM2 is built

```d2
direction: right
src: "Source cluster" {
  width: 210
  height: 80
  style.fill: "#e3f2fd"
}
mm: "MM2 (Connect-based)\nMirrorSource\nMirrorCheckpoint\nMirrorHeartbeat" {
  width: 280
  height: 120
  style.fill: "#e8f5e9"
}
dst: "Target cluster\nremote topics: src.topic" {
  width: 250
  height: 100
  style.fill: "#fff3e0"
}
cp: "Checkpoints\ngroup offsets translated" {
  width: 230
  height: 100
  style.fill: "#f3e5f5"
}
src -> mm
mm -> dst
mm -> cp
```

**Fig. 1.** MirrorMaker 2 runs as a set of Connect connectors: the source connector copies records, the checkpoint connector translates consumer offsets, the heartbeat connector measures liveness end to end.

MM2 is implemented on the Connect framework: MirrorSourceConnector replicates topics (by name or regex, with exclusion filters), MirrorCheckpointConnector emits checkpoints that translate consumer group offsets from source to target, and MirrorHeartbeatConnector produces heartbeats you can alert on. Replicated topics are renamed by the replication policy — by default the source alias becomes a prefix (`src.topic`), with a customizable separator, which prevents loops and lets the same topic name exist on both sides of an active-active pair; an identity policy keeps names unchanged where the topology allows it. The source connector also syncs topic configs and ACLs periodically and can auto-discover new topics, so a target mirrors not just records but the topics' shape ([[What is the Kafka AdminClient API for]]).

## Offsets and failover — the part that matters

Consumers cannot reuse source offsets on the target: partition leaders and segment layouts differ, so positions must be translated — checkpoints record `source offset → target offset` per group and partition, and can even write translated offsets into the target's `__consumer_offsets` while the group is not actively consuming there, so a failover restarts near where the source left off ([[What is the consumer_offsets topic for]]). Lag monitoring runs through the same machinery: the checkpoint and heartbeat records quantify how far the target trails, which is the metric a DR decision actually reads ([[What Kafka metrics do you monitor in production]]). For active-active topologies, the default prefix naming plus cycle detection keeps each cluster's copy distinct; cycles of clusters mirroring each other are supported but demand careful topic filter design ([[What is Kafka MirrorMaker for]]).

> [!warning] MM2 does not give you a consistent snapshot or zero RPO
> Replication is asynchronous: the target always trails the source by some lag, and offsets translation is per group and best-effort — a failover can reprocess or skip the few records in flight. Teams that expect "the DR cluster is the source, just later" get burned by exactly-once assumptions that MM2 never promised ([[What are at-most-once at-least-once and exactly-once semantics in Kafka]]).

> [!tip] Interview answer
> MirrorMaker 2 is the built-in cluster-to-cluster replication tool, built on Connect: three connectors copy records into prefixed remote topics, translate consumer group offsets into checkpoints, and emit heartbeats for lag monitoring. It serves active-passive DR and active-active aggregation; the key interview point is that offsets are translated, not copied, and replication is asynchronous — failover trades a small window of loss or duplication for survival.

