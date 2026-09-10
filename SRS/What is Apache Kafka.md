<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is Apache Kafka?

> [!abstract] Short answer
> A **distributed event streaming platform**: a cluster of **brokers** stores **topics** as append-only, partitioned logs; **producers** append records, **consumers** read them at their own pace by **offset**, and records stay until **retention** removes them. It combines three capabilities in one system: publish/subscribe, durable storage, and stream processing.

## Publish, store, process

Producers and consumers are **fully decoupled**: producers never wait for consumers, and a topic is multi-producer and multi-subscriber. Unlike a classic queue, a record is **not deleted when a consumer reads it** — you configure per-topic retention (time, size, or compaction), and performance stays effectively constant as data grows, so keeping history is normal. Any number of independent consumer groups can each read the same log from their own offset, which is what makes Kafka replayable. See also [[When should you use Redis Streams versus Apache Kafka]] for the boundary with lighter stream tools.

## First contact

```console
$ kafka-topics.sh --bootstrap-server localhost:9092 \
    --create --topic orders --partitions 1 --replication-factor 1
Created topic orders.
$ printf 'u1\torder-created\nu2\tpayment-authorized\nu1\torder-shipped\n' \
  | kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders \
    --reader-property parse.key=true
$ kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders \
    --from-beginning --timeout-ms 10000 --formatter-property print.key=true
u1	order-created
u2	payment-authorized
u1	order-shipped
```

**Listing 1.** A roundtrip on a single-broker KRaft cluster (Kafka 4.3.1): three keyed records go in and come back in log order with their keys.

```d2
direction: right
p1: "producer" {
  width: 130
  height: 44
  style.fill: "#e3f2fd"
}
topic: "topic orders\npartition 0, 1, 2\n(append-only logs)" {
  width: 250
  height: 74
  style.fill: "#fff3e0"
}
g1: "consumer group billing" {
  width: 210
  height: 44
  style.fill: "#e8f5e9"
}
g2: "consumer group audit" {
  width: 200
  height: 44
  style.fill: "#e8f5e9"
}
p1 -> topic
topic -> g1
topic -> g2
```

**Fig. 1.** Producers append to partition logs; two independent groups read the same records from their own offsets without touching each other.

## What it is not

Kafka is not a work queue: there is no per-record delete on ack, no built-in priority lanes, and order is only **per partition**. It is not a database either — there are no secondary indexes or ad-hoc queries; lookups mean reading the log or maintaining a state store built from it.

> [!warning] Retention, not consumption, removes data
> Newcomers expect a record to disappear once handled. It does not: the same record can be re-read for the whole retention window by anyone who can reach the topic. Anything sensitive needs topic-level cleanup plus [[How do you secure a Kafka cluster]].

> [!tip] Interview answer
> Kafka is a distributed, partitioned, replicated commit log: producers append records to topic partitions, consumers pull them by offset and track their own position. Records are kept by retention policy, not deleted on read, so replay and multiple independent readers are built in. Order is guaranteed only within a partition, and scaling means adding partitions.

