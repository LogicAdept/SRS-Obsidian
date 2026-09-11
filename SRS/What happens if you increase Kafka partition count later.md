<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What happens if you increase Kafka partition count later?

> [!abstract] Short answer
> The change is allowed and immediate, but one-directional — a topic's partition count only grows. New partitions start empty, existing records stay where they are, and the key-to-partition mapping changes for future records, because the hash modulo changes. Per-key ordering is therefore guaranteed only while the partition count stays fixed.

## What happens at the moment of the change

Adding partitions creates new empty partitions with their own leaders and updates the cluster metadata. Producers learn about it on their next metadata refresh — forced at least every `metadata.max.age.ms` (5 minutes by default), and sooner on leadership changes — and start routing through the new count. Nothing is copied or rehashed: old records keep their offsets in the old partitions. From then on the default partitioner computes `murmur2(key) mod N` with the new N, so a key that always mapped to partition 2 of 6 may map to partition 5 of 12 ([[What is the Kafka Partitioner interface for]] has the mapping details). Consumers in a subscribing group pick the new partitions up through a rebalance, since each partition must have exactly one assigned consumer.

```d2
direction: down
change: "partition count 6 -> 12\n(metadata-only change)" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
oldp: "existing partitions keep\ntheir records and offsets" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
fresh: "new partitions\nstart empty" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
prod: "producer refreshes metadata\n(next send, or within 5 min)" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
remap: "murmur2(key) mod 12:\nmost keys choose a new partition" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
order: "per-key order broken\nacross the change boundary" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
change -> oldp
change -> fresh
change -> prod -> remap -> order
```

**Fig. 1.** Storage is untouched; only the routing of future records and the consumer assignments change.

## Why this breaks key-ordering assumptions

Per-key ordering lives in the invariant same-key-same-partition ([[What ordering guarantees does Kafka provide for messages]]). A partition-count change breaks it at the boundary: a key's records written before the change sit in the old partition, records written after may sit in a different one. Any logic that consumes a key's history in order — aggregation, keyed joins, compaction-dependent reads — must bridge two partitions around the transition. Keyless records are unaffected in this respect: they never had per-key order, and sticky routing just spreads them over more partitions.

> [!warning] There is no symmetric "decrease partitions" operation
> Kafka offers no supported way to shrink a topic; the path is creating a new topic with fewer partitions and migrating data — [[Why can you not decrease Kafka partition count]]. That is why partition counts are chosen with headroom up front: growing later is an online but order-breaking event, and the cost of headroom is the extra metadata, replication endpoints, and per-partition buffers every broker carries — [[How do you choose the number of partitions for a Kafka topic]].

> [!tip] Interview answer
> Increasing partitions is an online metadata-level change: empty new partitions appear, old data stays put, consumers rebalance to cover them. The consequence is that the hash modulo changes, so a key's future records can land in a different partition than its history — per-key ordering holds only while the count is fixed. And it is one-way: no supported decrease.
