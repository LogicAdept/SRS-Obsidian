<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What happens when there are more Kafka partitions than consumers?

> [!abstract] Short answer
> One consumer owns several partitions. The group still runs — each member processes its share sequentially — but per-partition ordering is all you keep: records across the partitions owned by one consumer interleave, and one slow partition delays the others behind it in the same loop.

## How the split depends on the assignor

The assignment strategy decides who gets what:

* `RangeAssignor` (first in the default `[RangeAssignor, CooperativeStickyAssignor]`) works on a per-topic basis: partitions in numeric order, consumers in lexicographic order, and if the division is not even, the first few consumers get one extra partition — so with two topics of 3 partitions and 2 consumers, the first consumer carries 2 partitions of **each** topic while the second carries 1 of each.
* `RoundRobinAssignor` deals all subscribed partitions out in round-robin fashion, giving an even split.
* `StickyAssignor` maximizes balance while preserving as many existing assignments as possible.
* `CooperativeStickyAssignor` — same sticky logic, but revokes only partitions that actually move during a rebalance.
* Under the KIP-848 consumer protocol (GA in Kafka 4.0) the choice moves to the broker: server-side `uniform` assignor by default (with `range` available) selected via `group.remote.assignor` or the broker's `group.consumer.assignors`.

```d2
direction: right
t: "topic: 5 partitions" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
c1: "consumer 1\np0 p1 p2\n(own offset per partition)" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
c2: "consumer 2\np3 p4" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
order: "one poll loop\npartitions processed\none at a time" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
t -> c1
t -> c2
c1 -> order
```

**Fig. 1.** Five partitions, two consumers: the imbalance is normal — assignors do their best, and per-partition offsets keep each stream's ordering intact regardless of who owns it.

## What you gain and what you lose

Owning several partitions keeps the single-writer-per-partition contract and per-partition ordering — the ordering story is the same one behind [[What ordering guarantees does Kafka provide for messages]] and producer keys in [[Why do Kafka producer keys matter]]. What disappears is cross-partition ordering: a consumer processing p0 then p3 may see records from p3 first if p0's next record hasn't been fetched yet. A single-threaded loop over many partitions also couples their latencies — a backlog on one partition is drained only as fast as the loop moves through every assigned partition, a head-of-line effect that shows up as uneven consumer lag; when one partition is disproportionately busy, that is the hot-partition problem in [[What is a hot partition in Kafka]]. The throughput ceiling also reverses direction here: extra partitions are capacity in reserve — they activate when you add members, as long as you understand what happens when members exceed partitions ([[What happens if you have more Kafka consumers than partitions]]).

> [!warning] "More partitions per consumer = parallelism" is wrong for a single loop
> One consumer processes its partitions in one poll loop, so six partitions on one member are still sequential work — parallelism comes from more members, not more partitions per member. And do not expect fairness from Range: its per-topic, lexicographic split concentrates the extra partitions on the first consumers, so uneven load across members can be an assignor artifact rather than a data problem.

> [!tip] Interview answer
> Each consumer simply owns multiple partitions — that is the normal state of a group. Ordering survives per partition, offsets are tracked per partition, but cross-partition order is gone and one slow partition stalls the others in the same poll loop. Which member gets more depends on the assignor: Range splits per topic and leaves the first consumers one extra, RoundRobin evens it out, sticky variants preserve previous assignments, and since Kafka 4.0 the assignment can run server-side with the uniform assignor.

