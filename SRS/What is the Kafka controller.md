<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka controller?

> [!abstract] Short answer
> The controller is the cluster role responsible for managing broker registration and reacting to topology changes: it tracks broker liveness through sessions, persists ISR changes, and when a broker dies elects new leaders for its partitions from the remaining in-sync replicas, batching the notifications. Since Kafka 4.0 the controller always runs in KRaft mode — a Raft-style metadata quorum of typically 3 or 5 servers with one active leader and hot standbys.

## Responsibilities in one sentence each

Brokers register with the controller and keep the session alive with periodic heartbeats; when the session times out (`broker.session.timeout.ms`), the broker is treated as offline. The leader of each partition keeps its own ISR up to date, and the controller persists those sets in the cluster metadata so that every in-sync replica stays a valid promotion candidate. When a broker failure is detected, the controller elects one of the remaining ISR members as the new leader for each affected partition and ships the resulting leadership changes out as a batch — the design point that makes election cost scale with the number of *changed* partitions rather than triggering one election storm per partition. If the controller itself fails, another controller takes over.

```d2
direction: down
quorum: "controller quorum (3 or 5 servers)\none active + hot standbys" {
  width: 360
  height: 90
  style.fill: "#e3f2fd"
}
b1: "broker 1" {
  width: 150
  height: 70
  style.fill: "#e8f5e9"
}
b2: "broker 2" {
  width: 150
  height: 70
  style.fill: "#e8f5e9"
}
b3: "broker 3\nsession lost" {
  width: 170
  height: 70
  style.fill: "#ffebee"
}
act: "elect new leaders from ISR\nbatch notifications to brokers" {
  width: 380
  height: 90
  style.fill: "#fff3e0"
}
b1 -> quorum: heartbeats
b2 -> quorum: heartbeats
b3 -> quorum: session timeout
quorum -> act
```

**Fig. 1.** All servers discover the quorum through `controller.quorum.bootstrap.servers`; the active controller both receives broker heartbeats and pushes batched leadership changes.

## The KRaft quorum underneath

In KRaft mode each server declares its role with `process.roles` — `broker`, `controller`, or both (a "combined" server). Controllers participate in the metadata quorum, where each is either the active controller or a hot standby for it; a majority must stay alive for the cluster to keep working, so three controllers tolerate one failure and five tolerate two. All brokers and controllers learn about the quorum from `controller.quorum.bootstrap.servers`, and the active controller serves as the source the brokers sync metadata from. This is the only mode since 4.0 — ZooKeeper-based clusters are gone, and the migration path runs through the KRaft machinery rather than a hybrid runtime.

> [!warning] Combined broker+controller nodes are a development shortcut, not a production topology
> The documentation is explicit: combined servers are simpler to operate for small use cases, but the controller loses isolation from the rest of the system and you cannot roll or scale controllers separately from brokers — combined mode is not recommended in critical deployments. Monitoring picks up the quorum state as `ActiveControllerCount`, and exactly one server in the cluster should report 1. The failure-recovery flow this role drives is in [[What happens when a Kafka broker fails]].

```properties
# a dedicated controller node (KRaft)
process.roles=controller
node.id=1
controller.listener.names=CONTROLLER
controller.quorum.bootstrap.servers=c1:9093,c2:9093,c3:9093
```

**Listing 1.** A standalone controller declares its role, its listener, and the full quorum bootstrap list — the same bootstrap property must be set on every broker too. The quorum's election discipline is what keeps ISR bookkeeping, described in [[What is the Kafka in-sync replica set]], consistent across failovers.

> [!tip] Interview answer
> The controller is Kafka's cluster manager: it holds broker sessions, persists ISR changes into the metadata log, and on broker failure re-elects leaders from the surviving in-sync replicas in one batched notification set. Since Kafka 4.0 it is a KRaft metadata quorum — 3 or 5 servers, one active plus hot standbys, majority required — and exactly one controller is active cluster-wide at any moment.

