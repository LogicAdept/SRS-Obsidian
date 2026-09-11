<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What are RabbitMQ streams

> [!abstract] Short answer
> Streams are a persistent, replicated data structure modelled as an append-only log with non-destructive consumer semantics: messages are not deleted on ack, consumers read independently with offsets, and they can re-read from any point until retention expires them.

## How streams differ from queues

A queue deletes each message once acked and keeps a pointer; a stream keeps the log and gives every consumer its own offset. Consumers subscribe at an offset or timestamp, read as fast as they can, and can detach and replay later. Streams are always persistent and replicated; they can be consumed through a plain AMQP 0-9-1 queue-like interface, but the dedicated Stream protocol (plugin, port 5552) unlocks the full feature set and highest throughput. Super streams partition a logical stream across multiple streams, mimicking a partitioned log.

```d2
direction: down
pub: "append\noffset assigned" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
log: "replicated log\nretention by size/time" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
c1: "consumer A\noffset 10k" {
  width: 170
  height: 70
  style.fill: "#e8f5e9"
}
c2: "consumer B\noffset 0 (replay)" {
  width: 190
  height: 70
  style.fill: "#e8f5e9"
}
pub -> log
log -> c1
log -> c2
```

**Fig. 1.** Independent offsets over one shared log — the essence of non-destructive consumption.

## Use cases and boundaries

Streams were built for large fan-outs, replay, high throughput, and large backlogs — the four places queues converge poorly. They are the RabbitMQ answer closest to Kafka's model; the honest contrast with queues is destructive-versus-non-destructive consume, not speed alone. For job-once semantics with acks and delivery limits, quorum queues remain the tool, per [[What RabbitMQ queue types exist]]; the log-architectural comparison is in [[What is the difference between Kafka and RabbitMQ]].

```java
// Stream protocol client (Java)
stream.attach("orders.log");
stream.subscribe("orders.log", OffsetSpecification.first(), (offset, msg) -> {
    process(msg);   // no ack deletes anything; move your own offset
});
```

**Listing 1.** Conceptual stream subscription from the first offset; replay is just re-subscribing with an earlier offset.

> [!warning] Streams are not better queues
> A stream has no competing-consumer ack semantics, no per-message TTL, and no delivery-limit poisoning: "we replaced our work queue with a stream and got at-least-once job processing" breaks because the stream never removes work — dedup and offset tracking belong to your consumers.

> [!tip] Interview answer
> Streams are RabbitMQ's replicated append-only log: non-destructive offset-based consumers, replay, big fan-outs, and high throughput through the Stream protocol. Queues for delete-on-ack work, streams for shared history. Super streams add partitioning, and retention rules replace ack-based deletion.
