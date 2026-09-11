<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is a RabbitMQ routing key

> [!abstract] Short answer
> The routing key is an address string the publisher attaches to each message. Direct exchanges compare it to binding keys for exact equality, topic exchanges match it word-by-word against wildcard patterns, and fanout and headers exchanges ignore it entirely.

## Interpretation per exchange type

The string itself has no global meaning — its semantics are entirely defined by the exchange type it meets. Topic exchanges split it on dots into segments and match against binding patterns where `*` binds exactly one segment and `#` binds zero or more; see [[How does a RabbitMQ topic exchange match routing keys]]. Direct exchanges need byte-equality. Headers exchanges look only at the header table. Convention, not protocol, makes keys look like `orders.created.eu`, and [[What is a RabbitMQ binding]] is the side that carries the key or pattern to match against.

```d2
direction: down
msg: "routing key\n'orders.eu.created'" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
direct: "direct exchange\nexact match only" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
topic: "topic exchange\n'orders.*.created'" {
  width: 250
  height: 80
  style.fill: "#fff3e0"
}
fanout: "fanout exchange\nkey ignored" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
msg -> direct
msg -> topic
msg -> fanout
```

**Fig. 1.** The same routing key is evaluated differently — exact, pattern, or ignored — depending on the exchange type.

## Beyond the plain key

Publishers can supply additional routing keys through the `CC` and `BCC` message headers (sender-selected distribution); the broker routes using the primary key plus those, and strips `BCC` before delivery. When a message is dead-lettered without an explicit `x-dead-letter-routing-key`, its original routing keys travel with it, which is how a DLQ consumer can still see where a failed message was headed.

```java
ch.basicPublish("orders",                 // exchange
                "orders.eu.created",      // routing key
                props, body);
```

**Listing 1.** The routing key travels as a `basic.publish` parameter, not as a message header.

> [!warning] The routing key is not a filter
> Treating the key like a regex or a permission scope breaks down: for direct exchanges it is byte equality, for topic exchanges `*` and `#` are segment wildcards, and no exchange type sees the key as anything else. If routing needs more than that, use a headers exchange instead of overloading the key.

> [!tip] Interview answer
> The routing key is publisher-supplied addressing metadata that each exchange type interprets its own way: exact match for direct, dot-segment wildcards for topic, ignored for fanout and headers. It is a publish parameter, plus optional CC/BCC extra keys, and it is reused when dead-lettering unless overridden.
