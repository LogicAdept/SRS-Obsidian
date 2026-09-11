<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How do you design a Kafka order event pipeline?

> [!abstract] Short answer
> An order event pipeline — orders placed, paid, shipped, cancelled flowing through Kafka into services and analytics — stands on five decisions: key by order id for per-order ordering, fix the partition count with growth headroom, pick delivery semantics explicitly (idempotent producer, explicit commits, transactions where atomicity spans topics), version schemas with a compatibility gate, and make lag and dead letters observable from day one ([[What are the main components of Apache Kafka]]).

## The decisions in order

```d2
direction: down
key: "Key = order id\nall order events in\none partition, ordered" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
parts: "Partition count\nsized with headroom,\nnever shrunk" {
  width: 260
  height: 100
  style.fill: "#e3f2fd"
}
delivery: "Delivery\nacks=all, idempotence,\nread_committed downstream" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
schema: "Schema registry\nBACKWARD compatibility" {
  width: 260
  height: 90
  style.fill: "#f3e5f5"
}
obs: "Lag, DLQ, watermarks\nalerted" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
key -> parts -> delivery -> schema -> obs
```

**Fig. 1.** Each decision constrains the next: keys fix ordering, partition count fixes the hash mapping, delivery settings fix failure behavior, schemas fix evolution.

Keying by order id is the load-bearing choice: all events for one order land in one partition and inherit its ordering, so a downstream service sees placed-before-paid-before-shipped within the order without global coordination ([[Why do Kafka producer keys matter]], [[What ordering guarantees does Kafka provide for messages]]). Partition count follows: sized from throughput and consumer parallelism with headroom, because growing remaps the hash and interleaves an order's new events onto a different partition than its history — acceptable at a planned cutover, chaotic when accidental ([[How do you choose the number of partitions for a Kafka topic]], [[What happens if you increase Kafka partition count later]]). Delivery: producers run with `acks=all` and idempotence so retries cannot duplicate or reorder within a partition; consumers disable auto-commit and commit after processing for at-least-once, or use transactions with `read_committed` when an atomic hand-off across topics is required ([[What is the difference between Kafka acks 0 1 and all]], [[What happens during a Kafka consume-transform-produce transaction]]).

## The edges that decide quality

Schema evolution with a compatibility gate — registering new versions under a subject, BACKWARD by default — keeps producers from breaking consumers mid-rollout ([[What is a Schema Registry for in Kafka]]). Failure handling is explicit: bounded retries per record, then a dead-letter topic with origin metadata, with the business owner agreeing to the skip policy ([[How do you handle a poison pill message in Kafka]]). Retention matches replay expectations — enough time to rebuild a downstream store from the log, compaction where the topic is a state snapshot ([[What is Kafka log compaction]]). Observability closes the loop: consumer lag per group, dead-letter rates, and produce error rates are the pipeline's vital signs, and they are configured before the first incident, not after ([[What is Kafka consumer lag and how do you debug it]], [[What Kafka metrics do you monitor in production]]).

> [!warning] The pipeline is not "a producer, a topic, and a consumer"
> The failure patterns are all at the seams: unkeyed events that scramble per-order order, auto-commit that loses orders on crash, a hot seller whose key skews every partition, a schema bumped without a gate that blinds consumers on deploy. An order pipeline designed only for the happy path is a ledger that loses pages precisely when traffic peaks ([[What is a hot partition in Kafka]], [[Why is Kafka enable.auto.commit dangerous]]).

> [!tip] Interview answer
> I key events by order id so each order is ordered within a partition, size the partition count with growth headroom since shrinking is impossible and growing remaps keys, run producers with acks=all and idempotence, and consume with explicit commits or transactions for the atomic cases. Schemas go through a registry with compatibility checks, failures route through bounded retries to a dead-letter topic, and lag plus DLQ rates are alerted from day one.

