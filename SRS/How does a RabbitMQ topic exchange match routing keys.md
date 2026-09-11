<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# How does a RabbitMQ topic exchange match routing keys

> [!abstract] Short answer
> Topic exchanges split both the message routing key and the binding key into dot-separated words. A binding pattern matches when every segment matches: `*` consumes exactly one word, `#` consumes zero or more words, and literal words must be equal.

## Matching algorithm

`log.*` binds log.info but not log.info.db, because `*` is exactly one word; `log.#` binds log, log.info, and log.info.db; `#` alone matches any key and turns the exchange into a fanout for that binding; `*.error` binds app.error but not app.error.disk. Matching is per-binding: one topic exchange can host exact-ish bindings, one-word wildcards, and catch-all hashes simultaneously, each producing its own queue copy.

```d2
direction: down
key: "routing key\n'orders.eu.created'" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
b1: "'orders.#'\nmatch (2 extra words)" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
b2: "'orders.*.created'\nmatch (* = eu)" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
b3: "'orders.eu'\nno match (shorter)" {
  width: 220
  height: 80
  style.fill: "#ffebee"
}
key -> b1
key -> b2
key -> b3
```

**Fig. 1.** One key against three bindings: a hash swallows the tail, a star matches one middle word, a shorter literal fails.

## Usage patterns and limits

Words carry no built-in meaning — `orders.eu.created` is a convention the team chooses. Topic bindings propagate well for multi-tenant routing (`region.*.payments`) and audit trails (`audit.#`). The wildcard symbols live only in binding keys; a routing key containing a literal `*` is just a word. See [[What is the difference between a direct and a topic exchange in RabbitMQ]] for when the extra flexibility pays off, and [[What RabbitMQ exchange types exist]] for the alternatives.

```java
ch.exchangeDeclare("events", "topic", true);
ch.queueBind("eu-orders", "events", "orders.eu.#");
ch.queueBind("all-created", "events", "*.#");
```

**Listing 1.** Two bindings on one topic exchange: a region catch-all and a suffix catch-all with different fans.

> [!warning] Topic is not regex
> Interviewees often treat `*` as "any characters" and `#` as "more of the same". In reality both operate on whole dot-delimited words only, and there is no partial-word matching — `orders.*` never matches a key whose segment is `orders.eu.part1` unless the segment count fits exactly.

> [!tip] Interview answer
> Topic matching compares dot-words: literal segments must be equal, star binds exactly one segment, hash binds zero or more. Matching runs per binding and each hit queues a copy. It gives hierarchical routing like orders.eu.created without regex power, and hash alone degrades to fanout.
