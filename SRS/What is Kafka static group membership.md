<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is Kafka static group membership?

> [!abstract] Short answer
> Setting a non-empty `group.instance.id` makes the consumer a static member: the coordinator keys its seat by that stable id instead of an ephemeral member id, so a restarted process reclaims the same partitions without triggering a rebalance — as long as it returns before `session.timeout.ms` expires. Introduced by KIP-345, available on brokers and clients from 2.3.

## Dynamic vs static seats

Under ordinary dynamic membership the coordinator hands out ephemeral ids that change whenever members restart and rejoin, so routine administrative operations — code deploys, config updates, periodic restarts — churn the assignment and shuffle partitions between instances; the full trigger list is in [[What triggers a Kafka consumer group rebalance]]. For large stateful applications the shuffle is expensive: tasks that move must recover their local state before processing, and the application runs partially or entirely unavailable during that recovery. Static membership removes the churn: group membership stays unchanged based on the persistent ids, thus no rebalance is triggered when a member with the same id rejoins.

```d2
direction: right
restart: "pod restarts\nsame group.instance.id" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
quick: "returns within\nsession.timeout.ms" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
back: "reclaims the same partitions\nno rebalance" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
late: "still down after\nsession.timeout.ms" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
reb: "coordinator rebalances\npartitions move" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
restart -> quick
quick -> back
restart -> late
late -> reb
```

**Fig. 1.** The stable id turns a restart into a re-seat when the member is back inside the session window, and into an ordinary crash otherwise.

The documented usage recipe: upgrade brokers and clients to 2.3 or later, then set a unique `group.instance.id` per consumer instance in the group. Kafka Streams applications set one instance id per `KafkaStreams` instance, regardless of how many threads it uses. The feature also pairs naturally with a larger session timeout — the intended combination for riding out transient unavailability such as process restarts, and the timeout trade-offs are the same ones discussed in [[What is the difference between session.timeout.ms and max.poll.interval.ms]].

## The enforcement side

Because an instance id claims a single seat, the coordinator fences duplicates: if two processes present the same `group.instance.id` in one group, the broker shuts the intruder down with `FencedInstanceIdException`. The poll-gap timeout behaves differently too — for a static member that exceeds `max.poll.interval.ms`, partitions are not immediately reassigned; the consumer stops sending heartbeats and the partitions are reassigned after the session timeout expires, mirroring a static member that shut down. Only a genuinely dead member — silent past `session.timeout.ms` — hands its partitions over through the failover flow in [[How are Kafka partitions assigned when a consumer dies]].

```properties
# static member: stable seat across restarts
group.instance.id=orders-worker-1
session.timeout.ms=60000
heartbeat.interval.ms=3000
enable.auto.commit=false
```

**Listing 1.** Conceptual properties snippet: a unique instance id plus a session window long enough to cover a rolling restart; heartbeats stay at a third of the session.

> [!warning] Static membership is not crash immunity
> If the process is genuinely gone — hardware failure, deleted pod, crash that outlasts the session — the session timeout still fires and the group rebalances exactly as with a dynamic member; the stable id only removes rebalances for restarts that fit inside the window. And the same id must never run twice: duplicate ids are fenced with `FencedInstanceIdException`, so two replicas accidentally configured with the same `group.instance.id` will kill one of themselves.

> [!tip] Interview answer
> Static membership gives each consumer a persistent group.instance.id, so a restarted member within session.timeout.ms reclaims its old partitions and the group skips the rebalance that dynamic membership would have triggered — that is the point of KIP-345 for rolling deploys and stateful apps. If the member stays down past the session timeout the group rebalances anyway, and duplicate ids are fenced with FencedInstanceIdException.

