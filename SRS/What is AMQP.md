<!--
reps: 0
priority: 0
-->
#Messaging/AMQP #Messaging/Tools/RabbitMQ #SRS

# What is AMQP

> [!abstract] Short answer
> AMQP is an open application-layer messaging protocol family. AMQP 0-9-1, RabbitMQ's native protocol, defines the broker model — exchanges, queues, bindings, channels. AMQP 1.0 is a different protocol sharing nothing at the wire level; RabbitMQ supports it natively since 4.0.

## AMQP 0-9-1: the broker-facing model

0-9-1 prescribes strong messaging semantics and a specific broker shape: publishers write to exchanges, exchanges route by bindings to queues, consumers acknowledge deliveries, and `basic.qos` limits unacked deliveries. The protocol is binary but simple enough to have many client libraries. RabbitMQ extends it with features such as `basic.nack`, publisher confirms, alternate exchanges, and exchange-to-exchange bindings.

```d2
direction: right
pub: "publisher" {
  width: 150
  height: 60
  style.fill: "#e3f2fd"
}
ex: "exchange" {
  width: 150
  height: 60
  style.fill: "#fff3e0"
}
q: "queue" {
  width: 150
  height: 60
  style.fill: "#fff3e0"
}
con: "consumer" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
pub -> ex: "basic.publish"
ex -> q: "bindings"
q -> con: "basic.deliver + ack"
```

**Fig. 1.** The 0-9-1 model: publish to exchange, route by binding, deliver and acknowledge.

## AMQP 1.0: transport-first redesign

1.0 dropped the broker model entirely and became a peer-to-peer transfer protocol: links, sessions, transfer frames, settlement outcomes (`accepted`, `released`, `rejected`, `modified`). It imposes far fewer semantic requirements, which is why many brokers support it, and it is an OASIS standard and ISO/IEC 19464. A card-by-card contrast of the two models is in [[What is a RabbitMQ exchange]], which shows the 0-9-1 routing vocabulary 1.0 deliberately lacks. RabbitMQ bridged 1.0 onto its internal model: in AMQP 1.0 terms a 0-9-1 queue is addressed by a target address, and settlement outcomes map to ack/requeue semantics. See [[What protocols does RabbitMQ support]] for where each protocol fits.

```java
// 0-9-1 publish: broker model, routing key matters
ch.basicPublish("orders", "orders.eu", props, body);
```

**Listing 1.** The same intent in 1.0 is a transfer over a link to a node address — no exchange or routing key vocabulary exists there.

For the menu of other protocols, see [[What protocols does RabbitMQ support]].

> [!warning] AMQP 1.0 is not "the next version of 0-9-1"
> Saying "AMQP 1.0 is a newer, better AMQP with exchanges" mixes up two protocols: 1.0 has no exchanges, no bindings, and no channels; conflating them leads to wrong architecture decisions, especially since port 5672 serves both on RabbitMQ via version negotiation.

> [!tip] Interview answer
> AMQP is the protocol family behind RabbitMQ. 0-9-1 is the native, semantics-rich broker model with exchanges, queues, and acks. AMQP 1.0 is a different OASIS transport protocol with links and settlement outcomes, supported natively by RabbitMQ 4.0+. The name is shared, the protocols are not.
