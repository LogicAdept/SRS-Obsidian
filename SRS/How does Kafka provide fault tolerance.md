<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How does Kafka provide fault tolerance?

> [!abstract] Short answer
> Kafka's fault tolerance is replication plus a strict definition of "in sync": every partition has a leader and followers, a record counts as committed only when the whole in-sync replica set has applied it, and only in-sync replicas may be elected leader. The controller detects dead brokers and re-elects leaders automatically; producers opt into stronger durability with `acks=all` and `min.insync.replicas`. With f+1 replicas a partition tolerates f failures without losing committed records.

## The layers, from disk to client

Replication is the foundation: the unit of replication is the topic partition, writes go to the leader, and followers pull from the leader like ordinary consumers, keeping identical logs. The leader maintains the ISR — the set of replicas caught up within `replica.lag.time.max.ms` — and persists membership changes in cluster metadata, which is what makes any in-sync replica a legal leader. The committed region of the log ends at the high watermark, and consumers only ever see committed records, so a leader failure never exposes them to records that might vanish. Above the storage layer sits the controller, which watches broker sessions, removes dead brokers from their ISRs, and elects replacements in one batched pass; since Kafka 4.0 the controller itself is fault-tolerant by construction — a KRaft quorum of 3 or 5 servers where a majority keeps the cluster manageable.

```d2
direction: down
repl: "Replication\nleader + followers, f+1 tolerates f" {
  width: 380
  height: 90
  style.fill: "#e3f2fd"
}
isr: "ISR + high watermark\ncommitted = applied by whole ISR" {
  width: 380
  height: 90
  style.fill: "#e8f5e9"
}
ctl: "Controller (KRaft quorum)\ndetects failures, re-elects leaders" {
  width: 380
  height: 90
  style.fill: "#e3f2fd"
}
client: "Client contract\nacks=all + min.insync.replicas floor" {
  width: 400
  height: 90
  style.fill: "#fff3e0"
}
repl -> isr
isr -> ctl
ctl -> client
```

**Fig. 1.** Each layer assumes the one below: replication provides copies, the ISR defines which copies count, the controller acts on membership changes, and client settings turn it into an end-to-end durability contract.

The client-side contract is what an interviewer usually probes. `acks=all` makes the producer wait for the full ISR, and `min.insync.replicas` sets the floor below which writes are rejected instead of silently landing on one replica — the standard recipe is replication factor 3 with min ISR 2, tolerating one broker loss for both serving and writes. Unclean leader election stays disabled by default, so when no in-sync replica remains the partition prefers to stay unavailable rather than resurrect a stale log. Two less visible pieces complete the picture: followers are not required to have crash-proof disks — a returning replica must fully re-sync before rejoining the ISR, so Kafka needs no fsync-per-write or stable-storage guarantee — and rack-aware replica placement spreads replicas across fault domains so correlated rack failures cannot take out every copy.

## Where the guarantees stop

The loss guarantee for committed records is conditional: it holds as long as at least one in-sync replica of the partition survives. If all replicas of a partition are lost, no replication scheme recovers them, and the choice becomes waiting for a consistent replica or enabling unclean election and accepting loss. Availability for writes is likewise conditional — it degrades whenever the ISR falls below `min.insync.replicas`, by design.

> [!warning] Fault tolerance is a configuration outcome, not a default
> `default.replication.factor` is 1: a cluster that never set it, or topics created with RF 1, have zero tolerance for broker failure. The same trap applies to min ISR left at its default of 1, which lets `acks=all` degrade to single-copy writes. Fault tolerance is therefore the *combination* — replication factor, min ISR, acks, unclean election off — not the fact that replication exists. The failure-recovery flow itself is in [[What happens when a Kafka broker fails]].

```bash
# the health surface of every layer above
kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions  # 0
kafka.controller:type=KafkaController,name=ActiveControllerCount  # exactly one 1
kafka.controller:type=ControllerStats,name=UncleanLeaderElectionsPerSec  # 0
```

**Listing 1.** The gauges that say the machinery is actually engaged, not just configured — the middle one proves a single active controller, the last one proves no stale-log elections. The per-gauge semantics are in [[What are under-replicated partitions in Kafka]].

> [!tip] Interview answer
> Kafka tolerates failures by replicating each partition to f+1 replicas, tracking an in-sync replica set persisted in metadata, committing a record only when the whole ISR has it, and letting the controller — itself a KRaft quorum since 4.0 — re-elect leaders from the ISR when a broker dies. Clients opt into the guarantee with `acks=all` and `min.insync.replicas=2` at RF 3, unclean election stays off, and returning replicas fully re-sync so no stable disk is required.

