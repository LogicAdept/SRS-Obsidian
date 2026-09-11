<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is a RabbitMQ exchange

> [!abstract] Short answer
> An exchange is the routing entity publishers publish to in AMQP 0-9-1. It holds no messages: it consults its bindings table and forwards each message to zero or more queues, streams, or other exchanges. Its type — direct, fanout, topic, headers — decides how bindings are matched.

## Routing table semantics

A freshly declared exchange is an empty routing table. A binding fills one row of it: source exchange, destination, and an optional binding key or arguments. When a publish arrives, the exchange evaluates the message's routing key (and headers) against every binding and delivers a copy to each match. Because matches produce copies, one publish to a fanout or broad topic binding fans out to many queues at once — the mechanism behind [[What is a RabbitMQ fanout exchange]].

```d2
direction: right
msg: "message\nrouting key 'orders.eu'" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
ex: "direct exchange" {
  width: 190
  height: 70
  style.fill: "#fff3e0"
}
q1: "queue 'eu'" {
  width: 150
  height: 60
  style.fill: "#e8f5e9"
}
q2: "queue 'audit'" {
  width: 150
  height: 60
  style.fill: "#ffebee"
}
msg -> ex
ex -> q1: "binding key 'orders.eu'"
ex -> q2: "no match"
```

**Fig. 1.** A direct exchange routes a copy to every binding whose key equals the message routing key; non-matching queues receive nothing.

## Properties and lifecycle

Exchanges are declared with a name, type, `durable` flag, `auto-delete` flag, and x-arguments (used by headers matching or an [[What is a RabbitMQ alternate exchange|alternate exchange]]). Durability preserves the definition across restarts, not the messages. Every vhost pre-declares the nameless [[What is the default exchange in RabbitMQ|default exchange]] plus `amq.*` exchanges like `amq.topic`. Names starting with `amq.` are reserved for broker-internal exchanges and cannot be declared by applications.

```java
channel.exchangeDeclare("orders", "topic", true, false, null);
channel.queueDeclare("eu-orders", true, false, false, null);
channel.queueBind("eu-orders", "orders", "orders.eu.#");
```

**Listing 1.** Declare a durable topic exchange and bind a queue; publishing then happens against `orders`, never against the queue directly.

> [!warning] Producers never publish to queues in AMQP 0-9-1
> Saying "the producer sends the message to the order queue" is a red flag. Even when using the default exchange to make queue-named publishing convenient, a direct exchange hop still happens under the hood, and that hop is where routing, alternate exchanges, and `mandatory` semantics live.

> [!tip] Interview answer
> An exchange is a stateless routing table: type plus bindings decide which queues get copies of each publish. It never buffers, and durability applies to its definition only. Routing failures are handled by the mandatory flag or an alternate exchange, not by queueing.
