<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What RabbitMQ exchange types exist

> [!abstract] Short answer
> Four core types ship in the broker: direct (exact key match), fanout (broadcast to all bindings), topic (dot-segment wildcards), and headers (attribute matching with x-match). The nameless default exchange is a special-cased direct type, and plugins add more, such as consistent-hash and delayed-message.

## The four core types

Direct routes on byte-equality between routing key and binding key — one publish can still reach several queues bound with the same key. Fanout ignores the key and copies to every bound destination. Topic matches the key against patterns where `*` is one word and `#` is zero or more. Headers matches a message's header table against binding arguments using `x-match: all` (AND) or `any` (OR) and ignores the routing key completely. Plugin types include consistent-hash for load spreading, modulus-hash for partitioning, local-random, and the now-unmaintained delayed-message exchange.

```d2
direction: right
pub: "publish" {
  width: 130
  height: 60
  style.fill: "#e3f2fd"
}
d: "direct\nexact key" {
  width: 150
  height: 80
  style.fill: "#fff3e0"
}
t: "topic\n* and #" {
  width: 130
  height: 80
  style.fill: "#fff3e0"
}
f: "fanout\nbroadcast" {
  width: 140
  height: 80
  style.fill: "#ffebee"
}
h: "headers\nx-match" {
  width: 140
  height: 80
  style.fill: "#ffebee"
}
pub -> d
pub -> t
pub -> f
pub -> h
```

**Fig. 1.** The four core types side by side: what each of them actually looks at during routing.

## Choosing between them

Choose direct for point-to-point addressing with exact keys, topic for hierarchical events such as `orders.eu.created`, fanout for pure pub/sub copies, headers when routing criteria are several independent attributes rather than one string. The types are covered individually in [[What is a RabbitMQ fanout exchange]], [[How does a RabbitMQ topic exchange match routing keys]], and [[What is a RabbitMQ headers exchange]], with a direct-vs-topic contrast in [[What is the difference between a direct and a topic exchange in RabbitMQ]].

```java
ch.exchangeDeclare("orders.direct",  "direct",  true);
ch.exchangeDeclare("orders.events",  "topic",   true);
ch.exchangeDeclare("orders.alerts",  "fanout",  true);
```

**Listing 1.** The same declare call, different type argument; durability and x-arguments are orthogonal to the type.

> [!warning] Direct exchanges are not point-to-point
> A direct exchange routes to *every* queue bound with the matching key, so several queues can each get a copy. "Direct means one message, one queue" confuses direct routing with work queues — one-destination delivery needs either a dedicated binding or a competing-consumer queue.

> [!tip] Interview answer
> Core types: direct matches binding key to routing key exactly, fanout broadcasts ignoring the key, topic matches dot-segmented wildcards with one-word star and multi-word hash, headers matches header tables with x-match all/any. Default exchange is a nameless direct; plugins add consistent-hash and others.
