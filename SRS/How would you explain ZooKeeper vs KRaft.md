<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How would you explain ZooKeeper vs KRaft?

> [!abstract] Short answer
> Two generations of Kafka's metadata layer. In ZooKeeper mode, brokers store cluster metadata in an external coordination service and elect a controller through it. In KRaft mode, Kafka embeds the metadata: a quorum of controller nodes runs the Raft protocol over an internal metadata log — no ZooKeeper process, and Kafka 4.x runs KRaft only ([[What is the Kafka controller]]).

## Where metadata lives in each mode

```d2
direction: right
zk: "ZooKeeper mode\nbrokers + external ZK ensemble\nznodes hold metadata" {
  width: 300
  height: 110
  style.fill: "#ffebee"
}
k: "KRaft mode\nbrokers + controller quorum\nmetadata log via Raft" {
  width: 300
  height: 110
  style.fill: "#e8f5e9"
}
ctrl: "Controller\nactive + hot standbys" {
  width: 240
  height: 100
  style.fill: "#e3f2fd"
}
zk -> ctrl: watches/ephemerals
k -> ctrl
```

**Fig. 1.** ZooKeeper mode splits the cluster across two systems with two failure domains; KRaft folds coordination into Kafka itself, with controllers as first-class server roles.

In ZooKeeper mode the controller was elected via ZooKeeper, and brokers registered there; the metadata (topic configs, partition assignments, ISR state, ACLs) lived in znodes, so operating Kafka meant operating two distributed systems, and controller failover had to reconstruct state from the external store. KRaft replaces this with an event-sourced design: controllers append metadata records to an internal log replicated by Raft, one controller is active and the rest are hot standbys that keep replaying the log, and every broker fetches metadata from the quorum — the same log-based machinery Kafka already uses for data ([[What is the consumer_offsets topic for]]). Roles are configured per server — broker, controller, or combined — and brokers and controllers discover the quorum through `controller.quorum.bootstrap.servers`; quorum membership can change dynamically, with a new controller added after it has caught up ([[How is a Kafka broker structured]]).

## What actually changes in practice

Operationally the ZooKeeper dependency disappears: no separate ensemble to size, secure, monitor, or version-match, and a class of split-brain and consistency issues between two systems goes away with it. Scalability of metadata improves because the metadata log is a replicated, snapshot-able log rather than a hierarchy of znodes; KRaft mode is documented as supporting far larger partition counts than ZooKeeper mode could manage, which matters for clusters with many topics ([[How does Kafka achieve horizontal scalability]]). Configuration semantics changed with it: some ZooKeeper-era settings are gone, password encryption moved into Kafka's own mechanisms, and the cluster-wide feature level is governed by `metadata.version` rather than broker protocol versions. Migration from ZK-based clusters is a documented offline path — and for fresh deployments the question is settled: KRaft is the only mode ([[What Kafka broker settings matter in practice]]).

> [!warning] KRaft is not "ZooKeeper inside Kafka"
> The Raft quorum manages Kafka metadata only; it is not a general-purpose coordination service and cannot host your locks, leader elections, or service registry. Teams that used ZooKeeper as free infrastructure lose those uses when Kafka drops it — and should have moved them to purpose-built tooling long before.

> [!tip] Interview answer
> ZooKeeper mode kept metadata in an external ensemble and elected a controller through it — two systems to run. KRaft embeds coordination: a quorum of controller servers replicates a metadata log with Raft, one active controller plus hot standbys, brokers consume metadata from it, and roles are per server. It removes the second system, scales metadata better, and since Kafka 4.0 KRaft is the only mode.

