<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What happens if you have more Kafka consumers than partitions?

> [!abstract] Short answer
> The surplus consumers idle. Within one consumer group each partition is assigned to exactly one member, so with 4 partitions and 6 consumers, two members receive no partitions at all: they stay joined, keep heartbeating, poll and get nothing — no errors, no duplicates, just no work.

## Why the ceiling exists

Kafka's group model balances partitions so that each partition is assigned to exactly one consumer in the group; that single-owner rule is what makes per-partition offset tracking a single integer and keeps processing deterministic. The assignor has no way around it: whether `RangeAssignor` splits per topic, `RoundRobinAssignor` deals partitions out evenly, or `StickyAssignor` preserves prior placements, the outcome of more members than partitions is a zero-partition assignment for the extras. The same rule holds under the KIP-848 consumer protocol — the server-side `uniform` assignor also never shares a partition between two members of one group.

```d2
direction: right
t: "topic: 4 partitions\np0 p1 p2 p3" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
c1: "consumer 1\n2 partitions" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
c2: "consumer 2\n2 partitions" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
c3: "consumer 3\n0 partitions\nidle, heartbeating" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
t -> c1
t -> c2
t -> c3
```

**Fig. 1.** A group of three on a four-partition topic: two members carry two partitions each and the third one idles at zero.

An idle member is not a broken member. It participates fully in the group protocol — heartbeats, sessions, rebalances — and if the topic's partition count is later raised, the group detects the new partitions through periodic metadata refreshes and a rebalance hands one to the idler. That makes over-provisioned groups a legitimate short-term strategy when a partition-count increase is planned; the arithmetic of sizing is covered in [[What happens when there are more Kafka partitions than consumers]] and [[How do you choose the number of partitions for a Kafka topic]].

## What it costs

The idle members are not free: each one holds a coordinator session, runs fetches against empty partitions, and adds a member to every rebalance — group-wide barriers in the classic protocol get slower as membership grows, which is one of the motivations recorded for the KIP-848 redesign. And throughput does not improve: the maximum useful parallelism of a group is the partition count, so scaling beyond it only burns clients. Cross-group reads are different — a second group gets its own full copy of every partition, which is a fan-out, not extra parallelism; that scenario is [[What happens when a second Kafka consumer reads the same topic]].

> [!warning] Don't confuse "idle member" with "skipped partition"
> A zero-partition member still belongs to the group and will receive partitions on the next rebalance — the symptom of the reverse situation (more partitions than consumers) is unbalanced load, not idleness. Also, the ceiling applies per group, not per topic: nothing stops ten groups from reading the same four partitions, each with its own offset cursor. The partition-count ceiling only caps parallelism inside one group.

> [!tip] Interview answer
> Within a group a partition has exactly one owner, so extra consumers get zero partitions: they stay in the group, heartbeat, and receive nothing. It is harmless but pointless — no throughput gain, plus extra sessions and rebalance participants; adding members pays off only when the partition count grows, since new partitions are picked up through metadata refreshes and reassigned in a rebalance.

