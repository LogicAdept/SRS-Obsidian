<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What RabbitMQ queue types exist

> [!abstract] Short answer
> Three types: classic — the original non-replicated FIFO; quorum — Raft-replicated and the default recommendation for durable, highly available queues; and stream — an append-only replicated log with offset-based, non-destructive reads. The type is fixed at declaration via `x-queue-type`.

## Classic

Classic queues are versatile, non-replicated (replication was removed with classic queue mirroring in 4.0) FIFOs. They keep most messages on disk with a small in-memory working set, support priorities, per-consumer prefetch, and most TTL features, and they suit transient workloads, exclusive queues, and cases where data safety is not critical. They lack poison-message handling and at-least-once dead-lettering.

## Quorum and stream

Quorum queues replicate through a Raft group: a leader plus followers, a publish is confirmed once a majority has persisted it, and leadership survives node loss. Streams are append-only logs: consumers read independently with offsets, repeatedly, until expiry — closer to Kafka than to a work queue; see [[What are RabbitMQ streams]] for the mechanics.

```d2
direction: right
c: "classic\nno replication\nbest-effort" {
  width: 200
  height: 100
  style.fill: "#ffebee"
}
q: "quorum\nRaft majority ack" {
  width: 200
  height: 100
  style.fill: "#fff3e0"
}
s: "stream\nappend-only log\noffset reads" {
  width: 210
  height: 100
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** The three types by data-safety model: none, Raft replication, and log-with-offsets.

```java
Map<String, Object> qq = Map.of("x-queue-type", "quorum");
ch.queueDeclare("orders", true, false, false, qq);
Map<String, Object> sq = Map.of("x-queue-type", "stream");
ch.queueDeclare("orders.log", true, false, false, sq);
```

**Listing 1.** Both replicated types are one argument away from a classic declare; durable is implied for them.

## Choosing

Default to quorum for anything that must survive node loss with competing consumers, classic for transient, per-connection, or best-effort work, streams for fan-out history, replay, and big backlogs. The type cannot be changed after declaration — migration means a new queue plus a shovel or consumer switch. Individual mechanics: [[What is a RabbitMQ quorum queue]] and [[What is the difference between mirrored queues and quorum queues in RabbitMQ]] for the historical replication model.

> [!warning] The type is immutable
> Trying to redeclare an existing queue with a different `x-queue-type` raises PRECONDITION_FAILED, not a migration. Teams discover this mid-refactor: plan a new queue plus a drain strategy instead of expecting an in-place upgrade.

> [!tip] Interview answer
> Classic: non-replicated FIFO, fine for transient and exclusive work, no replication since 4.0. Quorum: Raft-replicated, data-safety default for durable queues, with delivery limits and at-least-once dead-lettering. Stream: replicated append-only log with offset-based non-destructive consumers for replay and large fan-outs.
