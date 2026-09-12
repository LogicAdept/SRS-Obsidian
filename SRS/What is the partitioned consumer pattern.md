<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messaging #SRS

# What is the partitioned consumer pattern

> [!abstract] Short answer
> Partitioned consumer is the messaging pattern where a consumer group is split across the partitions of a topic: each partition is read by exactly one consumer in the group. It buys you per-partition ordering and parallel scaling bounded by the partition count - the refinement of Competing Consumers used by Kafka-style brokers.

## How the assignment works

The topic is divided into partitions, which behave like independent point-to-point channels. When a consumer joins a group, the broker (or a coordinator) assigns each partition to exactly one member. Consumers do not race for individual messages; the routing decision was made up front by whoever chose the partition - typically a content-based choice on the message key. Senders that use the same key for related messages keep those messages on one partition, so they are processed in order.

```d2
direction: down
producer: "Producer\nkeys each record" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
topic: "Topic: 3 partitions" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
p0: "partition 0" {
  width: 170
  height: 60
  style.fill: "#fff3e0"
}
p1: "partition 1" {
  width: 170
  height: 60
  style.fill: "#fff3e0"
}
p2: "partition 2" {
  width: 170
  height: 60
  style.fill: "#fff3e0"
}
c1: "consumer C1" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
c2: "consumer C2" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
idle: "consumer C3\n(no partitions left)" {
  width: 250
  height: 70
  style.fill: "#ffebee"
}
producer -> topic
topic -> p0
topic -> p1
topic -> p2
p0 -> c1
p1 -> c1
p2 -> c2
p2 -> idle: "nothing left to assign"
```

**Fig. 1.** Two consumers cover three partitions; a third joiner gets no work, because in a group there can never be more active consumers than partitions.

```java
// Conceptual: keying controls co-location and therefore ordering
ProducerRecord<String, OrderEvent> rec =
    new ProducerRecord<>("orders", order.customerId(), event);
producer.send(rec);   // same key -> same partition -> in-order processing
```

**Listing 1.** The key choice is the lever: customer-scoped events keyed by customer id keep each customer's sequence intact while different customers process in parallel.

## Partitioned versus competing consumers

[[What is the Competing Consumers pattern]] puts many consumers on one channel and lets the messaging system hand each message to whichever consumer is free: load balancing is automatic, but per-message ordering is lost. Partitioned consumer reverses the trade-off: assignment is a priori, so related messages keep their order per partition, but an idle partition cannot lend work to a busy consumer's peer, and a membership change triggers rebalancing. The EIP description of Kafka-style consumption makes this exact point: consumers do not really compete, they read independent channels.

> [!warning] "Kafka preserves ordering" is a half-truth
> Kafka guarantees ordering only within a partition. Once you send unkeyed records or add partitions, cross-partition order is undefined. Also, a consumer group with more members than partitions leaves the extra consumers idle instead of sharing work.

> [!tip] Interview answer
> Partitioned consumer means the consumer group is mapped onto the topic's partitions - one reader per partition, assignment decided up front. It gives per-partition ordering and cheap parallelism, with the partition count as the scaling ceiling. Compared to [[What is the Competing Consumers pattern]], it sacrifices dynamic load balancing for order; I use it when sequences matter, keyed by entity id, and keep consumers inside the partition count. Delivery semantics on top of it are a separate question - see [[What are at-most-once at-least-once and exactly-once semantics in Kafka]] and [[What is the difference between Kafka delivery guarantees and application exactly-once]].
