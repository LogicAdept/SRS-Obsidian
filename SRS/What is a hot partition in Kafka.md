<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is a hot partition in Kafka?

> [!abstract] Short answer
> A hot partition is one partition that takes a disproportionate share of a topic's traffic because a few keys dominate the stream. Hash partitioning is working correctly — the data is skewed. The cost lands on the one consumer assigned to that partition and on the broker leading it, while the rest of the cluster idles.

## Why one partition concentrates traffic

The default partitioner maps each key to a fixed partition, so when one tenant, bot, or product id produces most of the records, its partition takes most of the traffic. The bottleneck is structural, twice over: a partition is served by exactly one leader broker that handles all produce and fetch traffic for it, and within a subscribing consumer group exactly one member processes it — one consumer per partition is the scalability unit ([[What happens when there are more Kafka partitions than consumers]]). If per-key volume exceeds what a single consumer can process, the excess shows up as lag on that partition alone, while the others sit near zero — [[What is Kafka consumer lag and how do you debug it]] is where this surfaces operationally.

```d2
direction: right
keys: "keys: tenant A ~70%,\nB, C, D minor" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
p0: "partition 0\n70% of records\nconsumer saturated" {
  width: 230
  height: 90
  style.fill: "#ffebee"
}
p1: "partition 1\n10%" {
  width: 150
  height: 70
  style.fill: "#e8f5e9"
}
p2: "partition 2\n10%" {
  width: 150
  height: 70
  style.fill: "#e8f5e9"
}
p3: "partition 3\n10%" {
  width: 150
  height: 70
  style.fill: "#e8f5e9"
}
keys -> p0: hash("tenant-A")
keys -> p1
keys -> p2
keys -> p3
```

**Fig. 1.** A correct hash cannot fix volume skew: the dominant key still owns exactly one partition, and the consumer of that partition is the throughput ceiling for it.

## Mitigations and their costs

Fix the key, not the cluster. Choose a higher-cardinality key — order id instead of tenant id — when per-entity ordering allows it; or salt the hot key by appending a randomizing suffix so its records spread across partitions, then strip the salt and re-aggregate downstream; or write a custom partitioner encoding the routing you need ([[What is the Kafka Partitioner interface for]]). Key choice drives all of this — [[Why do Kafka producer keys matter]]. Capacity planning still matters: sizing the partition count for peak per-key throughput is the other half — [[How do you choose the number of partitions for a Kafka topic]].

> [!warning] More partitions is the popular non-fix
> Increasing the partition count spreads total load but never splits one key's traffic: the dominant key still hashes to exactly one partition, so the hottest consumer stays just as hot. Salting does fix throughput, but deliberately gives up per-key ordering — everything downstream must re-order the salted streams, and code that assumed order starts producing wrong results quietly.

> [!tip] Interview answer
> A hot partition is key-volume skew: the hash puts a dominant key's whole stream on one partition, one consumer processes it serially, one broker leads it. The symptom is asymmetric lag — one partition growing while the rest are idle. Fixes live at the key level: better keys, or salting with downstream re-aggregation; adding partitions never splits a single key.
