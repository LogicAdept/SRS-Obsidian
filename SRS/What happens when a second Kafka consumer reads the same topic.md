<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What happens when a second Kafka consumer reads the same topic?

> [!abstract] Short answer
> It depends entirely on `group.id`. Same group: the partitions are split between the two members and together they drain the topic once — queue-like load balancing. Different group: each consumer gets its own full copy of every partition and advances through its own offset cursor — pub-sub fan-out. The topic itself never changes.

## Same group: work is divided

All consumer instances sharing the same `group.id` form one consumer group, and the group model assigns each partition to exactly one member. When the second consumer calls `subscribe` and joins, the coordinator triggers a rebalance and the assignment is recalculated — each member ends up with a disjoint subset of partitions. For a four-partition topic, two members consume two partitions each. Neither consumer sees the other's partitions again until the next rebalance; the mechanics of that redistribution are in [[What triggers a Kafka consumer group rebalance]] and the arithmetic extremes in [[What happens if you have more Kafka consumers than partitions]].

```d2
direction: right
topic: "orders topic\np0 p1 p2 p3" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
ga: "group A (billing)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
a1: "A-consumer 1\np0 p1" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
a2: "A-consumer 2\np2 p3" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
gb: "group B (audit)\nown offsets" {
  width: 240
  height: 70
  style.fill: "#ffe0b2"
}
b1: "B-consumer\nall partitions, full copy" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
topic -> ga
ga -> a1
ga -> a2
topic -> gb
gb -> b1
```

**Fig. 1.** Inside group A the partitions are divided; group B reads everything independently. The division happens per group, and each group tracks its own committed offsets.

## Different groups: the data is copied

Kafka allows any number of consumer groups for a given topic without duplicating stored data — additional consumers are cheap because each group is just one logical subscriber with its own position. To get queue semantics you put all processes in one group; to get pub-sub semantics each process gets its own group, so each one receives every record. The two groups advance independently: one can lag, rewind, or re-read from the earliest offset without touching the other's progress, because committed offsets are keyed by group — the storage side is described in [[What is the consumer_offsets topic for]].

> [!warning] "Two consumers means duplicate messages" is only true across groups
> Within one group the split guarantees a single owner per partition, so records are delivered once per group — duplicates come from the other source: after a rebalance, a member reprocesses what the previous owner never committed (at-least-once), which is the ladder in [[What are at-most-once at-least-once and exactly-once semantics in Kafka]]. The second trap is mixing subscribe and assign: a consumer that uses `assign()` manually bypasses group coordination entirely — it can read the same partitions as a group member concurrently, because the single-owner rule only binds members that joined through `subscribe`.

> [!tip] Interview answer
> Same group.id means the partitions are divided: one rebalance later, each member owns a disjoint subset and the topic is drained once — that is queue-style balancing. A different group.id means a full independent copy per group, with its own committed offsets in __consumer_offsets, so the two readers can lag or rewind separately — that is pub-sub. Data on disk is not duplicated either way.

