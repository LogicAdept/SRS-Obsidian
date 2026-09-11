<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is a RabbitMQ quorum queue

> [!abstract] Short answer
> A quorum queue is a replicated queue type built on the Raft consensus algorithm: a leader plus follower replicas, a publish confirmed only after a majority persists it, and automatic leader elections. It has been the recommended choice for durable, highly available queues since its 3.8 introduction.

## Replication and confirms

Declare with `x-queue-type: quorum` (and odd member counts are encouraged). A publish is confirmed once a majority of members has accepted and confirmed it to the leader, so a confirmed publish survives single-node loss. The queue leader serves all operations; followers replay the log. If the leader dies, remaining members elect a new one provided a majority is online — a minority stops committing rather than accepting data loss. Members are per-queue, chosen from cluster nodes, and can be adjusted by policies.

```d2
direction: down
pub: "publish" {
  width: 150
  height: 60
  style.fill: "#e3f2fd"
}
leader: "leader replica" {
  width: 190
  height: 70
  style.fill: "#fff3e0"
}
f1: "follower 1" {
  width: 150
  height: 60
  style.fill: "#fff3e0"
}
f2: "follower 2" {
  width: 150
  height: 60
  style.fill: "#ffebee"
}
conf: "publisher confirm\nafter majority" {
  width: 230
  height: 70
  style.fill: "#e8f5e9"
}
pub -> leader
leader -> f1
leader -> f2
leader -> conf
```

**Fig. 1.** Confirmation waits for a Raft majority; the down follower does not block the ack but limits quorum health.

## Feature trade-offs

Quorum queues have their own feature set: poison-message handling with `x-delivery-limit` (default 20 since 4.0), at-least-once dead-lettering, consumer timeouts, delayed retry, and — since 4.3 — strict message priorities in the 0–31 range, always enabled. They require durable declarations, do not support exclusive access, and their memory and disk footprint is higher than classic. Poison handling and retries continue in [[What is a poison message in RabbitMQ]] and [[How do you implement retries in RabbitMQ]].

```java
Map<String, Object> args = Map.of(
        "x-queue-type", "quorum",
        "x-delivery-limit", 10);
ch.queueDeclare("payments", true, false, false, args);
```

**Listing 1.** A durable quorum queue with a delivery limit; rejected deliveries past the limit dead-letter or drop.

> [!warning] Quorum is not a backup system
> Replication protects against node loss, not against a bad publish: an incorrect message is replicated faithfully everywhere. Deleting data from a quorum queue means consuming or letting TTL/limits act — replication is not an undo log.

> [!tip] Interview answer
> A quorum queue is a Raft-replicated queue: majority-persisted publishes, automatic leader elections, and member sets you control. It defaults the delivery limit to 20, supports at-least-once dead-lettering and, in 4.3, strict priorities 0–31. Use it as the durable default and skip classic mirroring entirely.
