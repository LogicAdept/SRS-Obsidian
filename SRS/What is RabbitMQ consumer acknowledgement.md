<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is RabbitMQ consumer acknowledgement

> [!abstract] Short answer
> Consumer acknowledgement is the consumer's confirmation that a delivery was received and processed: `basic.ack` removes the message, `basic.reject`/`basic.nack` requeue or dead-letter it. Manual ack mode is the safe default; auto-ack forgets the message the moment it is written to the socket.

## Manual versus automatic

In manual mode the delivery stays unacked until the handler finishes and the consumer returns `basic.ack`; a crash of the channel or connection requeues everything still unacked, flagged redelivered. In auto-ack mode the broker considers the delivery done as soon as it is written to the TCP socket — higher throughput, zero crash protection, and no prefetch-based in-flight bound, since the broker does not track completions. Docs describe auto-ack as fire-and-forget and recommend manual mode first. Acks are channel-scoped: acknowledging on a different channel raises an "unknown delivery tag" channel exception, and double-acking does the same.

```d2
direction: down
deliver: "basic.deliver\nredelivered flag possible" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
ack: "basic.ack\nmessage deleted" {
  width: 190
  height: 70
  style.fill: "#e8f5e9"
}
nack: "basic.reject/nack\nrequeue or DLX" {
  width: 230
  height: 80
  style.fill: "#ffebee"
}
auto: "auto-ack\ndeleted on send" {
  width: 190
  height: 70
  style.fill: "#ffebee"
}
deliver -> ack
deliver -> nack
deliver -> auto
```

**Fig. 1.** Manual mode keeps a decision point after delivery; auto-ack removes it entirely.

## The mechanics around acks

Delivery tags — monotonic per channel — identify each delivery; `multiple=true` acks or nacks everything up to the tag in one frame. Acks must arrive within the consumer acknowledgement timeout (30 minutes by default; since 4.3 enforced by quorum queues), otherwise the channel is closed with PRECONDITION_FAILED and the deliveries requeue. Ack after side effects, not before — the reasoning continues in [[What happens if a RabbitMQ consumer crashes before ack]] and [[Why must RabbitMQ consumers be idempotent]].

```java
DeliverCallback cb = (tag, delivery) -> {
    process(delivery.getBody());
    ch.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
};
ch.basicConsume("orders", false, cb, tag -> {}); // autoAck=false
```

**Listing 1.** Manual-ack consumption: ack strictly after processing completes.

> [!warning] Ack-before-processing is a silent-loss bug
> A handler that acks first and works after is auto-ack with extra steps: a crash between them loses the message with no requeue. Interviews treat this as a correctness red flag; ack last, and make the work idempotent instead of racing it.

> [!tip] Interview answer
> Consumer acks tell the broker a delivery was processed: manual basic.ack after side effects, reject/nack to requeue or dead-letter, multiple flag for batches, all channel-scoped by delivery tags. Auto-ack deletes on send — fast but unsafe — and the ack timeout closes stuck channels at 30 minutes by default.
