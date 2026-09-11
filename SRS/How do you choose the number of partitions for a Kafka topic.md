<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How do you choose the number of partitions for a Kafka topic?

> [!abstract] Short answer
> Start from three constraints and take the maximum: consumer parallelism you need today (one active consumer per partition), produce/consume throughput you need (partitions times per-partition throughput), and key-ordering stability (the count pins the hash mapping, so you can only grow it later — never shrink). Then add modest headroom for growth instead of planning to resize ([[Why can you not decrease Kafka partition count]]).

## The sizing logic

```d2
direction: down
throughput: "Target throughput\nproducer and consumer GB/s" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
parallel: "Consumer parallelism\nhow many independent workers" {
  width: 290
  height: 90
  style.fill: "#e8f5e9"
}
order: "Ordering horizon\nkeyed order needs a fixed count" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
max: "Take the max,\nadd growth headroom" {
  width: 260
  height: 90
  style.fill: "#f3e5f5"
}
throughput -> max
parallel -> max
order -> max
```

**Fig. 1.** Partition count is a capacity decision, not a tuning knob: every input bounds it from below, and the no-shrink rule means underestimating is expensive to correct.

Throughput: a partition's produce rate is bounded by batch accumulation on the client and replication on the server, and its consume rate by what one consumer can fetch and process — if your target exceeds what one partition sustains, count = target divided by your measured per-partition rate. Parallelism: a consumer group assigns at most one partition to one active member, so the partition count is the hard ceiling on consumption concurrency; sizing below your worker count idles members ([[What happens if you have more Kafka consumers than partitions]], [[What happens when there are more Kafka partitions than consumers]]). Ordering: keyed records are ordered per partition only, so if consumers must see one key's events in order, the key hash must be stable — which freezes the count until a planned, coordinated repartition ([[What ordering guarantees does Kafka provide for messages]], [[Why do Kafka producer keys matter]]).

## The cost curve of going too high

Partitions are cheap but not free: every partition adds replication fetchers, open file handles, and entries in metadata; brokers elect leadership per partition on failure — the controller batches these, but recovery time still grows with the partitions a dead broker hosted ([[What happens when a Kafka broker fails]]). A badly skewed key space makes huge partition counts pointless anyway — traffic piles onto a hot partition no matter how many exist ([[What is a hot partition in Kafka]]). Over-provisioning within reason is the standard answer: pick a count comfortably above today's need, keep a power-of-two style headroom if hash balance matters, and resize by growth — `createPartitions` works, shrinking does not ([[What happens if you increase Kafka partition count later]], [[What is the Kafka AdminClient API for]]).

> [!warning] Partition count is per topic, but broker cost is per cluster
> A cluster-wide habit of generous defaults multiplies: thousands of topics times dozens of partitions each lands on every broker's recovery path and metadata size. New-topic defaults like the broker's `num.partitions` exist so that an unthoughtful default of "lots" does not silently tax every future topic.

> [!tip] Interview answer
> I size partitions as max of three bounds: target throughput divided by realistic per-partition throughput, the consumer parallelism I actually need, and any ordering constraint that demands a stable hash — then add growth headroom, because partitions can only be added, never removed, and adding reshuffles keyed records. Going too high costs file handles, replication, and recovery time, so it is a deliberate number, not a default.

