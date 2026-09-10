<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What are the main components of Apache Kafka?

> [!abstract] Short answer
> A Kafka deployment has four moving parts: **brokers** (the storage layer that holds partition logs), a **KRaft controller quorum** that keeps cluster metadata (ZooKeeper was removed in 4.0), **producers and consumers in consumer groups** that read and write records, and the **topic-partition** layout that spreads and replicates data across brokers. Everything else — Streams, Connect, Admin — is a client API on top of the same wire protocol.

## Brokers and the metadata layer

Kafka runs as a cluster of one or more servers communicating over a TCP protocol. Servers in the storage layer are **brokers**: each hosts partition replicas of many topics and serves fetch and produce requests. Since 4.0 metadata lives only in **KRaft**: an internal Raft-based quorum (controller nodes) maintains the metadata log — topics, configs, partition leadership — so there is no ZooKeeper to run or migrate. In a combined-mode single node, like a laptop dev cluster, one process plays both roles.

## Topics, partitions, replicas

Data is replicated at the topic-partition level. Every partition has one **leader** broker that takes all writes and reads for it, and follower replicas on other brokers that only copy. The set of replicas currently in sync is the **ISR**, and [[What is min.insync.replicas in Kafka]] turns it into a write guard. A common production setting is replication factor 3 — three copies of each partition.

```d2
direction: down
broker1: "broker 1\nP0 leader\nP1 follower" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
broker2: "broker 2\nP0 follower\nP1 leader" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
kr: "KRaft controller quorum\nmetadata log (no ZooKeeper)" {
  width: 320
  height: 60
  style.fill: "#fff3e0"
}
prod: "producers" {
  width: 150
  height: 44
  style.fill: "#e8f5e9"
}
cons: "consumer groups" {
  width: 190
  height: 44
  style.fill: "#e8f5e9"
}
prod -> broker1
broker1 -> cons
broker2 -> cons
kr -> broker1
kr -> broker2
```

**Fig. 1.** Producers and groups talk to broker leaders; the KRaft quorum tracks who leads what. Followers on other brokers copy partitions for fault tolerance.

## Clients

**Producers** publish records; **consumers** subscribe as a **consumer group**, whose members split the partitions of a topic so each partition is handled by one consumer in the group at a time. Group membership is coordinated by a broker-side group coordinator, and a rebalance redistributes partitions when members join or leave. Management and stream processing are not broker features but client APIs ([[What core Kafka APIs exist]]): AdminClient for operations, Kafka Streams for stateful processing, Connect for source and sink integration — all ordinary clients from the broker's point of view.

> [!warning] A broker is not a topic
> A topic never lives on one machine: its partitions are spread over brokers, and each partition can be led by a different one. Capacity, skew, and failure questions must be asked per partition, not per topic.

> [!tip] Interview answer
> The core is brokers storing replicated partition logs, a KRaft controller quorum owning metadata since ZooKeeper removal in 4.0, and client applications: producers, consumer groups that share partitions, plus Admin, Streams, and Connect APIs. Each partition has one leader with in-sync follower replicas, and replication factor 3 is the typical production shape. Scaling and fault tolerance come from spreading partitions, not from bigger machines.

