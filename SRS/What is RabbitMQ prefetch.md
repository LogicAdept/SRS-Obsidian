<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is RabbitMQ prefetch

> [!abstract] Short answer
> Prefetch (basic.qos) caps the number of unacknowledged deliveries a consumer may hold. It is RabbitMQ's flow-control lever between broker and consumer: 0 means unlimited, sane values are tens for slow handlers and higher for tiny jobs, and RabbitMQ applies the count per consumer even though AMQP 0-9-1 words it per channel.

## How the cap works

With manual acks, every delivery in flight occupies one prefetch slot until acked or nacked; when slots run out, the broker stops pushing — the consumer gets work back only as it acks. The AMQP spec scopes prefetch to the channel; RabbitMQ deviates deliberately and applies it per new consumer, because channel-level counting needs slow coordination with every queue the channel consumes from. Both can be set: per-consumer and global limits coexist and must both be under the cap before new deliveries flow.

```d2
direction: down
q: "queue" {
  width: 130
  height: 60
  style.fill: "#fff3e0"
}
c1: "consumer A\nprefetch 10" {
  width: 170
  height: 80
  style.fill: "#e3f2fd"
}
c2: "consumer B\nprefetch 10" {
  width: 170
  height: 80
  style.fill: "#e3f2fd"
}
slot: "10 unacked max each\nacks release slots" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
q -> c1
q -> c2
c1 -> slot
c2 -> slot
```

**Fig. 1.** Each consumer drains its own slot budget; acks are what refill it.

## Sizing and failure modes

Prefetch 0 (unset) lets the broker dump the queue into the client — memory pressure, unfair distribution versus other consumers, and no protection against a slow handler. Too low starves throughput on round-trip-latency-bound acks. The classic sizing guidance: unacked-seconds equals target throughput times processing time; auto-ack consumers have no cap by definition, which is one more reason the docs call manual mode the default. Prefetch also shapes crash blast radius, per [[What happens if a RabbitMQ consumer crashes before ack]] — a dead channel requeues its whole window.

```java
ch.basicQos(10);                       // per-consumer limit
ch.basicQos(30, true);                 // plus channel-global cap
ch.basicConsume("orders", false, cb, tag -> {});
```

**Listing 1.** Per-consumer 10 with a shared 30 ceiling; both limits must have room before new deliveries flow.

> [!warning] Prefetch does not police auto-ack consumers
> The cap counts unacknowledged deliveries; an auto-ack consumer never has any by definition. Teams that "set prefetch 1" but run auto-ack still flood the client — the pair must be manual acks plus prefetch, as in [[What is RabbitMQ consumer acknowledgement]].

> [!tip] Interview answer
> Prefetch is basic.qos's unacked-delivery cap — RabbitMQ's per-consumer deviation from the spec's channel scope, with optional global limit on top. Zero is unlimited, tens fit slow handlers, hundreds fit tiny jobs; it exists only with manual acks and is the main lever for throughput, fairness, and crash blast radius.
