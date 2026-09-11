<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What are exchange-to-exchange bindings in RabbitMQ

> [!abstract] Short answer
> An exchange-to-exchange (E2E) binding is a RabbitMQ AMQP 0-9-1 extension that binds one exchange as a destination of another, using the `exchange.bind` method. Messages published to the source are then routed through the destination exchange's own type and bindings — a way to compose routing topologies without extra queues.

## How routing composes

E2E bindings are semantically identical to exchange-to-queue bindings — unidirectional, with a binding key interpreted by the source type — but both endpoints are exchanges. A publish to the source is routed once using the combined binding set of the source and all reachable destination exchanges: E2E is a routing extension, not a republish. Cycles are detected during delivery and each queue receives at most one copy per publish even if several paths lead to it.

```d2
direction: right
pub: "publish\nto source" {
  width: 170
  height: 70
  style.fill: "#e3f2fd"
}
src: "fanout source" {
  width: 170
  height: 70
  style.fill: "#fff3e0"
}
dst: "topic destination" {
  width: 190
  height: 70
  style.fill: "#fff3e0"
}
q1: "eu queue" {
  width: 140
  height: 60
  style.fill: "#e8f5e9"
}
q2: "audit queue" {
  width: 150
  height: 60
  style.fill: "#e8f5e9"
}
pub -> src
src -> dst: "E2E binding"
dst -> q1: "'orders.eu'"
dst -> q2: "'audit.#'"
```

**Fig. 1.** A fanout feeding a topic exchange lets new consumer sets subscribe to a shared stream without reworking the publisher.

## Why use it instead of a fanout to queues

E2E lets different subsystems attach their own routing layer to one shared stream: a core team publishes to one exchange, each consumer team binds their own exchange with their own keys, and later changes never touch the publisher. Because the message is routed once over the union of bindings, ingress metrics on the destination exchange do not tick — a known observability surprise. See [[What is a RabbitMQ binding]] for the base mechanics and [[What is a RabbitMQ fanout exchange]] for the broadcast case E2E most often extends.

```java
ch.exchangeDeclare("shared.stream", "fanout", true);
ch.exchangeDeclare("team.payments", "topic", true);
ch.exchangeBind("team.payments", "shared.stream", "");  // destination, source
ch.queueBind("payments.eu", "team.payments", "payments.eu.#");
```

**Listing 1.** The Java client's `exchangeBind` takes destination first, then source — a swap that bites everyone once.

> [!warning] Auto-delete interplay is one-directional
> An auto-delete exchange is deleted only when bindings *where it is the source* are removed; being a pure destination of E2E bindings does not keep it alive in that direction and does not trigger deletion on destination-binding removal. Teams relying on auto-delete across E2E topologies leak exchanges.

> [!tip] Interview answer
> E2E bindings bind exchanges to exchanges via exchange.bind, extending AMQP 0-9-1. Routing is one pass over the combined bindings, cycles are pruned, queues get one copy max. They let consumer teams evolve private routing layers against a shared stream without touching publishers.
