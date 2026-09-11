<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is a RabbitMQ binding

> [!abstract] Short answer
> A binding is the routing rule that links a source exchange to a destination — a queue, a stream, or another exchange. It optionally carries a binding key (for direct and topic types) or an arguments table (for headers). Without bindings, an exchange is an empty routing table that drops everything.

## Anatomy and behaviour

A binding is identified by source, destination, destination type (`queue` or `exchange`), and an optional key/arguments map. When a publish matches several bindings of one exchange, each match yields a separate copy into its destination. Binding key semantics come from the exchange type: exact string equality for direct, wildcard patterns for topic, ignored for fanout — see [[What is the difference between a direct and a topic exchange in RabbitMQ]] for the contrast.

```d2
direction: right
ex: "topic exchange 'events'" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
b1: "binding\nkey 'orders.#'" {
  width: 170
  height: 80
  style.fill: "#e3f2fd"
}
b2: "binding\nkey 'payments.*'" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
q1: "orders queue" {
  width: 170
  height: 60
  style.fill: "#e8f5e9"
}
q2: "payments queue" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
ex -> b1: "bind"
ex -> b2: "bind"
b1 -> q1
b2 -> q2
```

**Fig. 1.** Bindings are the rows of the exchange's routing table; the publish key is matched against each key.

## Durability and E2E bindings

A binding inherits durability from both endpoints: durable exchange plus durable queue gives a fully durable binding; a transient destination yields a semi-durable binding, which is removed when the node hosting the transient queue stops. Bindings between exchanges — the E2E extension — let you compose routing topologies, per [[What are exchange-to-exchange bindings in RabbitMQ]].

```java
ch.queueBind("eu-orders", "orders", "orders.eu.#");
ch.queueUnbind("eu-orders", "orders", "orders.eu.#");
```

**Listing 1.** `queueBind` adds the routing row and `queueUnbind` removes it; both take source, destination, and key.

> [!warning] Same key on same pair is one binding
> Re-declaring an identical binding is idempotent, but two bindings with different keys are separate rows. A common mistake is rebinding with the wrong key and then wondering why the old routing still fires: the old row was never removed, only a second row added.

> [!tip] Interview answer
> A binding is the link from an exchange to a queue, stream, or another exchange, with a key or argument map interpreted by the exchange type. Routing produces one copy per matching binding, bindings inherit durability from both endpoints, and an exchange without bindings routes nowhere.
