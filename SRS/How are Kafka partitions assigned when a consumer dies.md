<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How are Kafka partitions assigned when a consumer dies?

> [!abstract] Short answer
> Nothing moves until the group notices: after `session.timeout.ms` without heartbeats the coordinator declares the member dead and rebalances the group, and the assignor distributes the orphaned partitions among the survivors. Processing then resumes from the last committed offsets, so the replacement member re-reads whatever the dead one processed but never committed.

## The takeover timeline

```d2
direction: down
crash: "consumer dies\nheartbeats stop" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
session: "session.timeout.ms (45 s default)\nexpires on coordinator" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
rebalance: "coordinator triggers rebalance\nsurvivors rejoin" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
assign: "assignor places orphaned partitions\non remaining members" {
  width: 340
  height: 90
  style.fill: "#fff3e0"
}
resume: "new owners fetch from last\ncommitted offsets in __consumer_offsets" {
  width: 360
  height: 90
  style.fill: "#e8f5e9"
}
crash -> session -> rebalance -> assign -> resume
```

**Fig. 1.** Failover latency is the detection time plus the rebalance itself; the work lost is bounded by what was processed after the last commit.

Which member ends up with which partitions depends on the assignment strategy. `RangeAssignor` (first in the default client list `[RangeAssignor, CooperativeStickyAssignor]`) works per topic and, if the surviving member count makes the division uneven, gives the first consumers one extra partition. `CooperativeStickyAssignor` follows the same sticky logic but only revokes partitions that actually move — the survivors keep everything they already own, which is why it is the usual choice for reducing failover churn. Under the KIP-848 consumer protocol (GA in Kafka 4.0) the coordinator computes the target assignment server-side and moves only the affected partitions incrementally, without a global revoke barrier.

## What the survivors inherit

The new owner starts from the committed offset recorded for the group in `__consumer_offsets` — not from the position the dead member had actually reached. Records that were polled and processed but not yet committed are therefore consumed again, which is why a consumer failure under default commit behavior is an at-least-once event; the semantic ladder is spelled out in [[What are at-most-once at-least-once and exactly-once semantics in Kafka]] and the commit mechanics in [[What are Kafka commitSync and commitAsync for]]. Lag also redistributes: the survivor now drains both its own partitions and the adopted ones, which is visible as a jump in consumer lag after every crash.

> [!warning] "Partitions move instantly" is wrong
> Detection takes up to a full `session.timeout.ms` (45 s by default), and only then does the rebalance begin — so a crash can leave a partition unowned for tens of seconds, not milliseconds. If a static member died, its `group.instance.id` seat is kept for the whole session timeout on purpose, stretching the gap further. And with an eager assignor the failover pause touches the entire group, not just the dead member's partitions — see [[What triggers a Kafka consumer group rebalance]].

> [!tip] Interview answer
> The dead member's partitions stay untouched until the session timeout expires without heartbeats; then the coordinator rebalances and the assignor spreads the orphaned partitions over the survivors — sticky-cooperative moves only those, eager revokes everything first. The new owner resumes from the last committed offset, so uncommitted work is reprocessed, and total failover time is detection plus rebalance, roughly the session timeout by default.

