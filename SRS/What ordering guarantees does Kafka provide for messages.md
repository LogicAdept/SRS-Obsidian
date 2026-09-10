<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What ordering guarantees does Kafka provide for messages?

> [!abstract] Short answer
> Exactly one: **order within a partition**. A partition is an append-only log, so consumers read it in exactly the write order. A producer that keys its records sends them all to one partition, which yields **per-key order**. There is **no global order across partitions**, and without an idempotent producer, retries can silently reorder records even within the partition.

## Why per-partition order holds

The broker appends each record after the last one in the partition log and stamps sequential offsets, so the log *is* the order — reading it back cannot scramble anything. For keyed records the producer's partitioner maps equal keys to equal partitions, and the docs guarantee a consumer reads a topic-partition in exactly the order records were written. This is what [[Why do Kafka producer keys matter]] is about: the key, not the broker, decides where order exists.

A live check on a 5-partition topic (Kafka 4.3.1, default partitioner, synchronous sends):

```console
$ java KeyPartitionDemo
key=alice  -> partition=4 offset=0
key=bob    -> partition=3 offset=0
key=alice  -> partition=4 offset=1
key=carol  -> partition=2 offset=0
key=alice  -> partition=4 offset=2
```

**Listing 1.** Every alice record landed on partition 4 with consecutive offsets 0, 1, 2 — same key, same partition, same order. bob and carol were placed independently.

```d2
direction: down
alice: "records keyed alice" {
  width: 200
  height: 44
  style.fill: "#e3f2fd"
}
p4: "partition 4 log\n0: alice  1: alice  2: alice" {
  width: 290
  height: 60
  style.fill: "#e8f5e9"
}
p3: "partition 3 log\n0: bob" {
  width: 220
  height: 56
  style.fill: "#e8f5e9"
}
bob: "record keyed bob" {
  width: 170
  height: 44
  style.fill: "#e3f2fd"
}
alice -> p4
bob -> p3
```

**Fig. 1.** Keys pin records to partitions; order is readable inside one log, but nothing orders partition 3 against partition 4.

## Where order breaks

Multiple producers (or an unsynchronized one) appending to one partition have no defined order between each other — the log interleaves them by arrival. Retries are the silent killer inside one producer: with idempotence off, a retried batch can land after a later batch, as covered in [[Why can Kafka retries break ordering without idempotence]]. And resizing a topic re-buckets keys, breaking per-key order around the change — see [[What happens if you increase Kafka partition count later]].

> [!warning] Per-key order is only as strong as the key
> Order holds for records with the same key on the same topic-partition. If a partition count change rehashes keys mid-stream, or an application routes related events under different keys (or without keys), consumers will see interleavings that look like a Kafka bug but are a keying choice.

> [!tip] Interview answer
> Kafka guarantees order only within a partition: the log preserves append order and consumers read it in that order. Same key means same partition, so per-key order holds as long as keying and the partition count stay stable. Across partitions there is no ordering, and retries without idempotence can reorder even a single partition's stream.

