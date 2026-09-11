<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is a Kafka consumer group leader?

> [!abstract] Short answer
> In the classic rebalance protocol the group leader is one of the consumers — not a broker — that the coordinator picks to compute the partition assignment. When all members have joined, the coordinator sends the leader the full member list with subscriptions, the leader runs the client-side assignor, and every member collects its share through SyncGroup.

## Where the leader appears in the protocol

The classic flow runs in two phases: members send `JoinGroup`; the coordinator waits for the batch of joiners, then picks a leader and sends back the `JoinGroup` response to all members — but only the leader's response carries the group's membership and subscription data. The leader is responsible for computing the assignment, using the `PartitionAssignor` configured on the client (`RangeAssignor`, `RoundRobinAssignor`, `StickyAssignor`, `CooperativeStickyAssignor`). In the second phase all members call `SyncGroup`, and the coordinator distributes the leader's plan to everyone. Only after that do members start fetching from their assigned partitions. This ceremony is what a rebalance executes — the trigger list is in [[What triggers a Kafka consumer group rebalance]] and the broker-side role is in [[What is a Kafka consumer group coordinator for]].

```d2
direction: right
m1: "consumer A\nJoinGroup" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
m2: "consumer B\nJoinGroup" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
coord: "coordinator (broker)\nwaits, picks leader" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
lead: "leader consumer\nruns assignor on\nsubscriptions" {
  width: 260
  height: 100
  style.fill: "#ffe0b2"
}
sync: "SyncGroup:\neveryone collects\nits assignment" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
m1 -> coord
m2 -> coord
coord -> lead
lead -> sync
sync -> m1
sync -> m2
```

**Fig. 1.** The coordinator orchestrates but does not compute: in the classic protocol the chosen member plans the assignment and hands the plan back through SyncGroup.

## Why the assignment lives on a member

The design keeps the broker thin and makes the assignment logic pluggable: any client can embed its own metadata and strategy, which is how Kafka Streams ships its own assignor. The cost of that choice is protocol fragility — the broker stores opaque subscription bytes, compatibility of embedded metadata becomes a constraint, and debugging requires client logs. This is exactly what the next-generation rebalance protocol (KIP-848, GA since Kafka 4.0) removes: with `group.protocol=consumer` there is no client-side leader; the coordinator computes a target assignment with a server-side assignor (`uniform` by default, `range` available) and hands it out incrementally through heartbeat responses — the upgraded heartbeat is the subject of [[What is the Kafka consumer heartbeat thread for]]. The client configs `partition.assignment.strategy`, `session.timeout.ms` and `heartbeat.interval.ms` are not usable under the new protocol.

> [!warning] Leader is ephemeral — and often confused with the coordinator
> The leader is just an ordinary member: if it crashes or leaves, the next rebalance simply elects another member, and no offsets are lost because committed offsets live on the coordinator in `__consumer_offsets`, not on the leader. And the leader is **not** the coordinator — the coordinator is a broker that manages membership; the leader is a consumer that computes a plan. With the consumer protocol the leader role disappears entirely, so a correct answer should first ask which protocol the group runs.

> [!tip] Interview answer
> In the classic protocol the coordinator picks one of the group's consumers as leader; the leader receives all members' subscriptions in its JoinGroup response, computes the partition assignment with the client-side assignor, and everyone collects their share via SyncGroup. Since Kafka 4.0 you can set group.protocol=consumer and the leader disappears — the broker-side coordinator computes the assignment itself with a server-side assignor.

