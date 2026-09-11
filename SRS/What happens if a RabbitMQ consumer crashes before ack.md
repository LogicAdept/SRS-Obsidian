<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What happens if a RabbitMQ consumer crashes before ack

> [!abstract] Short answer
> With manual acks nothing is lost: the unacked deliveries are requeued to the queue's ready set (at, or as close as possible to, their original positions) and redelivered — possibly to other consumers, with the redelivered flag set. With auto-ack the message is gone the moment it was sent.

## The requeue path

Unacked deliveries belong to the channel; when the channel or its connection dies — process crash, network loss, channel exception — the broker requeues them automatically. Redelivered messages carry `redelivered=true` and may go to any of the queue's consumers, not necessarily the one that died. Requeue position is "original position if possible", otherwise closer to the head, which already hints that order across consumers can shuffle — see [[How does RabbitMQ preserve message order]]. The consumer-side duty is idempotency, per [[Why must RabbitMQ consumers be idempotent]].

```d2
direction: down
live: "consumer processes\nbut does not ack" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
dead: "channel/connection dies" {
  width: 210
  height: 70
  style.fill: "#ffebee"
}
ready: "requeued, redelivered=true" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
other: "other consumer receives it" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
live -> dead
dead -> ready
ready -> other
```

**Fig. 1.** The crash turns unacked deliveries back into ready messages for any consumer of the queue.

## Consequences teams forget

With manual acks the crash costs at-least-once duplicates, not data; with auto-ack it costs data. A quorum queue additionally counts the failure against `x-delivery-count`, so repeated crashes of a poisoned message eventually dead-letter it — the mechanism behind [[What is a poison message in RabbitMQ]]. Requeue also interacts with [[What is RabbitMQ prefetch]]: a dead channel drops its whole unacked window back at once, which is why huge prefetch turns one crash into a burst.

```java
boolean redelivered = delivery.getEnvelope().isRedeliver();
if (redelivered && !alreadyProcessed(eventId)) {
    process(delivery.getBody());      // idempotent path
}
ch.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
```

**Listing 1.** Treat redelivered as a hint, not an error: idempotent processing plus ack.

> [!warning] Requeue does not preserve strict order
> Requeued messages jump back toward the head while other consumers keep working, so even a single-queue setup shows reordering after crashes. Claims that "RabbitMQ redelivers in order" fail the follow-up: position is best-effort, order is a stream-or-SAC story.

> [!tip] Interview answer
> Manual-ack deliveries that never got acked are requeued when the channel dies and redelivered to any consumer with the redelivered flag — at-least-once with duplicates, nothing lost. Auto-ack loses them on send. Quorum queues count the failure toward the delivery limit so crash loops dead-letter.
