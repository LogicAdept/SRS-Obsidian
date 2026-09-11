<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What messaging patterns does RabbitMQ implement

> [!abstract] Short answer
> Out of the box RabbitMQ gives you point-to-point work queues with competing consumers, pub/sub via fanout or topic bindings, routing, request-reply with reply-to and correlation ids, dead-lettering, and delayed or retried delivery through TTL plus DLX. Streams add a replayable log for large fan-outs.

## Pattern to feature mapping

Point-to-point is the default: one queue, each message to one consumer; adding consumers turns it into competing consumers with round-robin dispatch. Pub/sub is exchange routing — fanout for broadcast, topic for patterned slices — with one queue per subscriber. Request-reply uses the `reply-to` and `correlation_id` properties, ideally with the direct reply-to pseudo-queue. Dead-lettering, TTL, and overflow implement poison handling and delayed retry. Streams replace destructive consume with offset reads when history and replay matter more than per-message acks.

```d2
direction: right
ev: "one event" {
  width: 140
  height: 60
  style.fill: "#e3f2fd"
}
fx: "fanout/topic" {
  width: 160
  height: 70
  style.fill: "#fff3e0"
}
w1: "work queue\ncompeting consumers" {
  width: 210
  height: 80
  style.fill: "#fff3e0"
}
w2: "audit queue\ncopy per subscriber" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
w3: "DLQ path\nreject/TTL/limit" {
  width: 170
  height: 80
  style.fill: "#ffebee"
}
ev -> fx
fx -> w1
fx -> w2
w1 -> w3
```

**Fig. 1.** The same routing layer serves work queues, pub/sub copies, and the failure path, depending on queue and binding design.

## Pattern boundaries

RabbitMQ does not implement a durable multi-subscriber log in queues — Kafka comparisons belong there, see [[What is the difference between Kafka and RabbitMQ]]. EIP names such as Dead Letter Channel or Competing Consumers map onto these features; the pattern-level views live in [[What is the Competing Consumers pattern]] and [[What is the Dead Letter Channel pattern]], while the broker mechanics are in [[How do competing consumers work in RabbitMQ]] and [[How does RPC work in RabbitMQ]].

```java
// request-reply core properties
props.replyTo = "rpc.replies";     // or amq.rabbitmq.reply-to
props.correlationId = reqId;
```

**Listing 1.** Two message properties turn a work queue into a request-reply conversation.

> [!warning] Feature presence is not pattern support
> Having exchanges does not mean "RabbitMQ does event sourcing" and having reply-to does not mean "it does RPC reliably at scale" — direct reply-to is at-most-once for replies, and queues delete on ack. Patterns are emergent from features plus topology discipline, not built-in guarantees.

> [!tip] Interview answer
> RabbitMQ covers the classic broker patterns: work queues with competing consumers, pub/sub and routing through exchange types, request-reply via reply-to plus correlation id, dead-lettering, TTL-driven delays and retries, and — through streams — replayable fan-out. It stays a queue broker, not a partitioned log.
