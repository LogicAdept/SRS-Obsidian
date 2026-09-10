<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is a Kafka consumer group coordinator for?

> [!abstract] Short answer
> The group coordinator is the broker-side manager of one consumer group: it tracks members and their sessions, runs the rebalance procedure, and persists committed offsets in the internal `__consumer_offsets` topic. Every group maps to exactly one coordinator, chosen deterministically from the group name, and consumers find it with a `FindCoordinator` request.

## How a consumer finds it

Consumer groups are assigned to coordinators based on their group names. A consumer that only knows `bootstrap.servers` sends a `FindCoordinator` request to any broker and reads the coordinator's host and port from the response; if the coordinator later moves (broker restart, leadership change of the offsets partition), the consumer rediscovers it the same way. This is why the group id, not the client, decides which broker owns your group — two groups with different ids usually land on different brokers, spreading coordination load across the cluster.

## The three jobs

**Membership and liveness.** The coordinator accepts `JoinGroup` requests, tracks each member's session, and monitors heartbeats. If no heartbeat arrives before `session.timeout.ms` expires, the coordinator removes the member and starts a rebalance. In the classic protocol it also picks the group leader that computes the assignment — the division of labor is explained in [[What is a Kafka consumer group leader]].

**Rebalance driving.** The coordinator collects subscriptions, distributes assignments (classic: `JoinGroup`/`SyncGroup`; KIP-848 consumer protocol since Kafka 4.0: incremental target assignment handed out through `ConsumerGroupHeartbeat` responses, computed by a server-side assignor). With `group.protocol=consumer`, session timeouts and heartbeat intervals are broker-side configs — `group.consumer.session.timeout.ms` (45 s default) and `group.consumer.heartbeat.interval.ms` (5 s default) — which is part of moving protocol complexity off the clients.

**Offset storage.** When the coordinator receives an offset commit, it appends the commit to the compacted internal topic `__consumer_offsets` and only then answers success; if replication of that append does not finish within the timeout, the commit fails and the consumer retries. Offset fetches are served from the coordinator's in-memory cache of the latest commits. The storage layout itself is the topic of [[What is the consumer_offsets topic for]].

```d2
direction: right
c1: "consumer A\npoll loop" {
  width: 200
  height: 90
  style.fill: "#e3f2fd"
}
c2: "consumer B\npoll loop" {
  width: 200
  height: 90
  style.fill: "#e3f2fd"
}
find: "FindCoordinator\nby group.id" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
coord: "group coordinator\n(broker)\nmembership · rebalance\nheartbeat watch" {
  width: 300
  height: 130
  style.fill: "#fff3e0"
}
offsets: "__consumer_offsets\ncompacted log\noffset commits" {
  width: 260
  height: 110
  style.fill: "#e8f5e9"
}
c1 -> find
c2 -> find
find -> coord
coord -> offsets: commit append
```

**Fig. 1.** Both members discover the same coordinator for their group; the coordinator keeps membership state and durably appends offset commits to the internal offsets topic.

## Seeing it in operations

The admin tooling exposes the coordinator per group: `kafka-consumer-groups --describe` prints a `COORDINATOR (ID)` column alongside the group state (`Stable`, `Rebalancing`, …) and the member count. You can also read the coordinator id straight from the describe output when you need to know which broker to inspect for a stuck group.

> [!warning] Coordinator is not the group leader
> A classic interview mix-up: the coordinator is a **broker** chosen from the cluster, while the group leader (classic protocol) is one of the **consumers** in the group that computes the partition assignment. Also, one broker coordinates many groups at once, and a group's coordinator has nothing to do with which broker is the leader of the topic partitions the group reads.

> [!tip] Interview answer
> The coordinator is the broker responsible for a consumer group: it tracks member sessions via heartbeats, triggers and drives rebalances, and durably stores committed offsets by appending them to the compacted __consumer_offsets topic before acknowledging the commit. Consumers locate it with a FindCoordinator request derived from the group id, and since Kafka 4.0 it can also compute the assignment itself with the new consumer protocol.

