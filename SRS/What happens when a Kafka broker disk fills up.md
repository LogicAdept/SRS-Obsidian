<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What happens when a Kafka broker disk fills up?

> [!abstract] Short answer
> Retention is what normally keeps a broker's disk bounded — old segments are deleted once they age out — so a full disk means data is arriving faster than retention reclaims it. When the broker can no longer write to a log directory it stops serving the replicas that live in that directory, the partitions whose logs were there go offline, and the controller moves their leadership to in-sync replicas on other brokers. The partition keeps working only if in-sync replicas survive elsewhere.

## Why a full disk is an incident and not steady state

In normal operation disk usage plateaus: retention discards old log data after a fixed period or when the log reaches a configured size, so the disk holds roughly the retention window of data. Usage runs away when producers outrun that window — a burst of oversized traffic, a new heavy topic, or a retention setting that was never set to match the workload. Placement then decides the blast radius: with multiple data directories, partitions are assigned round-robin and each partition lives entirely inside one of them, so one full disk affects exactly the partitions placed on it, not the whole broker evenly.

```d2
direction: down
full: "data dir D1 hits disk limit\nappends to D1 fail" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
stop: "broker stops serving replicas in D1\nOfflineLogDirectoryCount rises" {
  width: 360
  height: 90
  style.fill: "#fff3e0"
}
move: "controller notified\nleadership moves to ISR replicas on other brokers" {
  width: 380
  height: 90
  style.fill: "#e3f2fd"
}
aftermath: "URP rises for affected partitions\nacks=all may hit NotEnoughReplicas" {
  width: 380
  height: 90
  style.fill: "#ffebee"
}
full -> stop
stop -> move
move -> aftermath
```

**Fig. 1.** The documented handling chain for a failed log directory: stop serving it, take its partitions offline, let the controller relocate leadership.

When a log directory fails, the broker logs that it is stopping serving the replicas in that directory and marks it offline — visible in monitoring as `OfflineLogDirectoryCount`, whose expected value is 0. The controller is notified, leadership for the affected partitions moves to their remaining in-sync replicas, and the partitions show up as under-replicated while the data re-replicates. Where the durability story lands next depends on the ISR floor: with `min.insync.replicas` above the shrunken ISR, producers with `acks=all` get `NotEnoughReplicas` instead of a false ack — the interplay is in [[What is min.insync.replicas in Kafka]].

## Recovery and prevention

Kafka's durability model expects this failure: durability does not require syncing to local disk because a failed node recovers from its replicas, and the documented practice after a single-broker disk failure is to wipe the disk and rebuild the replicas from the cluster. A returning follower must fully re-sync with the leader before rejoining the ISR, even if it lost unflushed data. Prevention is mostly configuration discipline: cap the data with `log.retention.bytes` / `log.retention.ms`, alert on disk free space *before* the limit and on `UnderReplicatedPartitions`, and spread data across multiple directories. One special case deserves its own care: in KRaft mode the metadata log directory of the controllers is irreplaceable in the ordinary sense, and its disk replacement is a deliberate quorum-aware procedure, not a wipe-and-rebuild.

> [!warning] Do not "fix" a full disk by shrinking retention on the live broker
> Deleting retention or raising limits makes the disk fill faster and pushes the failure onto every replica placed there, which is the path from one degraded broker to partitions with no in-sync replica left — at which point the choice is unavailability or unclean leader election and real data loss. The failure-handling sequence around leadership moves is in [[What happens when a Kafka broker fails]], and the alert that should have fired first is in [[What are under-replicated partitions in Kafka]].

```properties
# bound the growth so retention, not the disk edge, decides deletion
log.retention.bytes=1099511627776
log.retention.ms=604800000
```

**Listing 1.** Retention caps per partition make disk usage predictable; without them a hot topic can outrun any disk, and the first symptom is failed appends on the directory that holds it.

> [!tip] Interview answer
> A broker disk filling up first breaks appends on the directories that hit the limit; when the broker treats a directory as failed it stops serving the replicas living there, their partitions go offline and their leadership moves to in-sync replicas on other brokers, showing up as under-replicated partitions and possibly `NotEnoughReplicas` for `acks=all` writers. Recovery is wipe-and-rebuild from replicas, and prevention is retention caps plus disk alerting — Kafka's durability model explicitly expects a node to be rebuilt from its replicas.

