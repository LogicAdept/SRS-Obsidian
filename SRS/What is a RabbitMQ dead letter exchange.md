<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is a RabbitMQ dead letter exchange

> [!abstract] Short answer
> A DLX is an ordinary exchange that receives republished messages from a queue when four events occur: reject or nack with requeue=false, per-message TTL expiry, max-length overflow (drop-head or reject-publish-dlx), or a quorum queue's delivery-limit being exceeded. The DLX is configured per queue via policy or x-arguments.

## Trigger events and routing

Dead-lettering republishes the message: with `x-dead-letter-routing-key` set, the DLX route uses that key; without it, the message's original routing keys are reused — including CC/BCC keys. The DLX itself is any type, so a topic DLX can fan failures out into per-failure-class DLQs. An entire expired queue's messages are *not* dead-lettered — expiry of the queue is not a per-message event. Dead-lettering republishes internally *without* confirms by default, so DLX delivery is not guaranteed-safe in clusters; quorum queues add at-least-once dead-lettering with internal confirms.

```d2
direction: down
q: "work queue\nDLX configured" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
tr: "reject/requeue=false\nTTL expiry\noverflow\ndelivery-limit" {
  width: 240
  height: 110
  style.fill: "#ffebee"
}
dlx: "DLX (any type)" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
dlq: "DLQ → inspect, retry, park" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
q -> tr
tr -> dlx
dlx -> dlq
```

**Fig. 1.** Four failure classes converge on one exchange; the DLQ behind it is where humans and retry jobs live.

## Configuration and gotchas

Policy keys `dead-letter-exchange` and `dead-letter-routing-key` are preferred over hardcoded x-arguments because policies change without redeployment (arguments win when both exist). Declaring needs read on the queue and write on the DLX. Without a DLX configured, rejected/expired messages simply drop — the silent-loss trap. Uses: poison parking, retry loops, delayed processing — see [[How does RabbitMQ dead-letter-exchange get used as an Invalid Message Channel]] for the EIP angle, [[How do you implement retries in RabbitMQ]] for loops, and [[What is the difference between Invalid Message Channel and Dead Letter Channel]] for pattern-level boundaries.

```bash
rabbitmqctl set_policy DLX "^orders$"   '{"dead-letter-exchange":"orders.dlx"}' --apply-to queues
```

**Listing 1.** Minimal DLX policy; bind a DLQ to `orders.dlx` and rejected orders become visible.

> [!warning] DLX is not a queue
> Calling "the DLQ" and "the DLX" the same thing muddles topology: the exchange routes, queues store. You bind a queue to the DLX like any exchange, choose its type deliberately, and a routing key mismatch between dead-letter config and DLQ bindings is a classic silent-drop bug.

> [!tip] Interview answer
> A DLX is the queue's failure exit: reject/nack without requeue, TTL expiry, overflow, and quorum delivery limits republish there, reusing original routing keys unless overridden. It is a normal exchange — pick a type, bind DLQs, and remember that without it those messages are silently dropped, while quorum queues add confirmed at-least-once dead-lettering.
