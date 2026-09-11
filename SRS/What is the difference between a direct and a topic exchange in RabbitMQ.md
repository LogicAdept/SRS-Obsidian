<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is the difference between a direct and a topic exchange in RabbitMQ

> [!abstract] Short answer
> A direct exchange matches the routing key to binding keys by exact string equality; a topic exchange matches the key word-by-word against binding patterns using `*` (one word) and `#` (zero or more words). Direct is cheaper and address-like; topic trades a little CPU for hierarchical, pattern-based subscriptions.

## The mechanical difference

With direct, binding key `orders.eu` and message key `orders.eu` match byte-for-byte and nothing else — the same key bound to several queues still delivers copies to all of them. With topic, binding `orders.*` also matches `orders.eu` and `orders.asia`, and `orders.#` additionally matches `orders.eu.created`. Both types can fan out via multiple equal bindings, so the real difference is what a single binding can express.

```d2
direction: down
key: "routing key\n'orders.eu.created'" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
d: "direct\nbinding 'orders.eu.created'\nmatch; 'orders.eu' no" {
  width: 290
  height: 100
  style.fill: "#fff3e0"
}
t: "topic\nbinding 'orders.#' matches\nbinding 'orders.*.created' matches" {
  width: 320
  height: 100
  style.fill: "#e8f5e9"
}
key -> d
key -> t
```

**Fig. 1.** The same key hits one direct binding but can satisfy several topic patterns at once.

## When to pick which

Use direct when the key is an address or ID — routing by tenant ID, task type, or queue-like semantics — and you want predictable, cheap exact routing. Use topic when producers emit hierarchical events and subscribers pick slices: `orders.eu.#`, `payments.*.declined`. Wildcards make access control and subscription growth easier but add matching work per publish and can surprise you with unintended broad bindings like `#`. Individual mechanics are in [[How does a RabbitMQ topic exchange match routing keys]], and the type inventory in [[What RabbitMQ exchange types exist]].

```java
ch.queueBind("eu-handler", "orders.direct", "orders.eu");
ch.queueBind("all-eu",     "orders.topic",  "orders.eu.#");
```

**Listing 1.** Same intent, two types: the direct binding matches one key, the topic binding covers the whole subtree.

> [!warning] Direct does not mean one-to-one
> A direct exchange with a key bound to three queues delivers three copies, so "direct is point-to-point" is a half-truth. One-to-one needs a single bound queue or competing consumers on one queue, which is a queue design question, not an exchange type property.

> [!tip] Interview answer
> Direct is exact-match routing between routing key and binding key — fast, address-like, but every distinct key needs its own binding. Topic matches dot-words with one-word stars and multi-word hashes, so one binding can cover a subtree. Both fan out over multiple bindings; the difference is pattern expressiveness versus matching cost.
