<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is a RabbitMQ fanout exchange

> [!abstract] Short answer
> A fanout exchange copies every publish to all of its bound queues, streams, or exchanges and completely ignores the routing key. It is the broker-side mechanism behind classic pub/sub: one event published, every subscriber's queue receives its own copy.

## Broadcast semantics

Because the key is ignored, topology alone decides delivery: bind a queue and it gets everything the fanout receives; unbind it and it stops. Each subscriber must own its queue — sharing one queue between two subscribers gives round-robin delivery of halves, not copies. This distinction is exactly the competing-consumers versus pub/sub split described in [[What is the Competing Consumers pattern]] and [[What messaging patterns does RabbitMQ implement]].

```d2
direction: right
pub: "publish\nkey ignored" {
  width: 190
  height: 90
  style.fill: "#e3f2fd"
}
fx: "fanout" {
  width: 130
  height: 60
  style.fill: "#fff3e0"
}
q1: "email queue" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
q2: "sms queue" {
  width: 150
  height: 60
  style.fill: "#e8f5e9"
}
q3: "audit queue" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
pub -> fx
fx -> q1
fx -> q2
fx -> q3
```

**Fig. 1.** One publish produces three independent queue copies; each consumer acks its own copy separately.

## Practical notes

Unroutable fanout publishes — a fanout with zero bindings — are simply dropped when not mandatory, since nothing can ever match. Fanout plus per-subscriber filtering is not a feature: if subscribers need subsets, use a topic exchange instead. A fanout can be bound to another fanout or to topic exchanges through exchange-to-exchange bindings to compose topologies, per [[What are exchange-to-exchange bindings in RabbitMQ]].

```java
ch.exchangeDeclare("user.events", "fanout", true);
ch.queueDeclare("sms-worker", true, false, false, null);
ch.queueBind("sms-worker", "user.events", ""); // key unused
```

**Listing 1.** The binding key is empty on a fanout — only the binding's existence matters.

> [!warning] Copies are independent messages
> If one subscriber's queue is full and overflows with drop-head, the other subscribers still receive their own copies — but that subscriber's copy is gone. "Fanout is reliable if one consumer works" is wrong: delivery to each bound queue follows that queue's own limits and dead-lettering.

> [!tip] Interview answer
> A fanout exchange is AMQP's broadcast: every bound destination gets its own copy, the routing key is ignored, and each copy lives independently in its queue. Subscribers need separate queues; zero bindings means a drop or a return, not buffering, and selective routing calls for topic or headers instead.
