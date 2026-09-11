<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is the default exchange in RabbitMQ

> [!abstract] Short answer
> The default exchange is a pre-declared, nameless direct exchange that auto-binds every declared queue using the queue name as the binding key. Publishing with an empty exchange name and a routing key equal to a queue name therefore looks like publishing straight to the queue.

## Why it exists

AMQP 0-9-1 publishers always publish to exchanges. The default exchange exists as a convenience so simple applications can push to a named queue without building a topology: each `queue.declare` implicitly creates a binding with routing key equal to that queue name. It is still a routing hop — the message passes through a direct exchange — but applications cannot bind, unbind, or delete it themselves.

```d2
direction: right
pub: "basic.publish\nexchange: ''\nrouting key: 'orders'" {
  width: 260
  height: 110
  style.fill: "#e3f2fd"
}
def: "default exchange\namq.default, nameless" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
q: "queue 'orders'\nauto-bound by name" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
other: "queue 'audit'\nnot addressed" {
  width: 200
  height: 80
  style.fill: "#ffebee"
}
pub -> def
def -> q: "implicit binding"
def -> other: "no match"
```

**Fig. 1.** The nameless direct exchange resolves a queue-named publish to exactly that queue.

## Limitations and gotchas

Because it is a special-cased convention rather than a normal exchange, the default exchange does not support the alternate-exchange feature, and routing via it bypasses nothing else — `mandatory` semantics still apply: an unroutable publish (no such queue) is returned when `mandatory=true`, the behaviour behind [[What does the RabbitMQ mandatory flag do]]. Production systems usually graduate to named exchanges once several consumers need the same stream, since the default exchange cannot fan out — see [[What is a RabbitMQ exchange]] for the general model.

```java
ch.basicPublish("", "orders", props, body);      // via default exchange
ch.basicPublish("amq.topic", "orders", props, body); // named exchange instead
```

**Listing 1.** Publishing with an empty exchange name targets a queue by name; the same payload via `amq.topic` targets a topic topology.

> [!warning] It is not "no exchange"
> Describing a default-exchange publish as "direct to the queue, no routing involved" loses the interview: unroutable handling, `mandatory`, and returns all happen exactly as with a named direct exchange, and there is no way to add extra bindings to fan the message out.

> [!tip] Interview answer
> The default exchange is the nameless direct exchange every vhost pre-declares; each queue is auto-bound to it with its own name as the key, so publishing to it with a queue name delivers to that queue. You cannot bind it or attach an AE, and it is a convenience, not a special transport.
