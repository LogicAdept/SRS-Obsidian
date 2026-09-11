<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is a poison message in RabbitMQ

> [!abstract] Short answer
> A poison message is a delivery that always fails processing — malformed payload, missing dependency, a bug — so redelivery loops forever. RabbitMQ's fixes are quorum queues' `x-delivery-limit` (default 20) dead-lettering the message after too many failed deliveries, and manual retry topologies with caps plus DLQs.

## Why the loop happens

Redelivery sources are structural: a nack or reject with requeue=true, a channel closing with unacked deliveries, or a consumer crashing mid-handler. Each redelivery re-executes the same failing handler, pinning a consumer and generating log noise, and with prefetch above one the unacked window fills too. Quorum queues track failures in the `x-delivery-count` header — included with redelivered messages — and when the count exceeds `x-delivery-limit` the message is dead-lettered or dropped, which is the built-in poison break. Classic queues have no such mechanism, so caps must come from the retry topology or the handler itself; see [[How do you implement retries in RabbitMQ]] for the loop design.

```d2
direction: down
deliver: "basic.deliver" {
  width: 170
  height: 70
  style.fill: "#e3f2fd"
}
fail: "handler fails\nreject requeue=true" {
  width: 230
  height: 90
  style.fill: "#ffebee"
}
loop: "redelivery\nx-delivery-count + 1" {
  width: 230
  height: 90
  style.fill: "#ffebee"
}
limit: "x-delivery-limit exceeded\n→ DLX or drop" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
deliver -> fail
fail -> loop
loop -> fail
loop -> limit: "quorum queues"
```

**Fig. 1.** Without a limit the cycle never exits; the quorum delivery limit is the only broker-side break.

## Operational detection

Signs of poisoning: unacked counts pinned at prefetch, redelivery-heavy traffic, a queue whose ready count is small but whose ack rate is near zero, and DLQ growth once limits exist. Monitoring redeliveries and delivery-limit DLQ depth catches it before consumers starve; the metrics are in [[What RabbitMQ metrics do you monitor]], and the semantic difference between reject and nack counting is in [[What is the difference between ack nack and reject in RabbitMQ]].

> [!warning] Auto-ack "fixes" poisoning by losing data
> Switching to auto-ack makes the poison loop disappear because the broker forgets the message on delivery — along with every other message lost on crash. Poison handling must happen at the retry/limit/DLQ layer, not by disabling acknowledgement.

> [!tip] Interview answer
> A poison message is one that always fails and loops through requeue, blocking consumers. Quorum queues break the loop natively with x-delivery-count versus x-delivery-limit (default 20) then dead-letter; classic queues need a capped retry topology with a DLQ. Auto-ack hides the loop by silently dropping work.
