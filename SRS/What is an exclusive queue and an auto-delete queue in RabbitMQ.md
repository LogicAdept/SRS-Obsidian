<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is an exclusive queue and an auto-delete queue in RabbitMQ

> [!abstract] Short answer
> An exclusive queue is usable only by its declaring connection and is deleted when that connection closes; an auto-delete queue is deleted when its last consumer unsubscribes or disconnects, after having had at least one. Both model transient, client-scoped state.

## Exclusive: connection-bound

Exclusive queues are declared per connection and reject any other connection's operations with a channel exception (RESOURCE_LOCKED). They always become classic queues — exclusive quorum queues or streams make no sense — and the broker ignores a durable flag on them: durability is meaningless for something that dies with its connection. Typical use is RPC reply queues, especially server-named ones, per [[How does RPC work in RabbitMQ]].

## Auto-delete: consumer-bound

Auto-delete queues linger until one consumer has registered and then all consumers are gone — cancellation or connection loss — at which point the broker deletes the queue. If a queue never had a consumer (pure `basic.get` polling), it is never auto-deleted; queue TTL covers that case. Use auto-delete for temporary fan-out subscriptions where the last departing subscriber should clean up, and remember [[What is a RabbitMQ queue]]'s shared-state advice: temporary queues with well-known names invite reconnect races.

```d2
direction: right
exc: "exclusive\ndies with declaring connection" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
auto: "auto-delete\ndies with last consumer" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
ttl: "queue TTL\ndies after idle time" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Three cleanup mechanisms keyed to different lifetimes: connection, consumer set, idle time.

```java
// exclusive, server-named RPC reply queue
ch.queueDeclare("", false, true, true, null);
// auto-delete, durable, shared pub/sub cleanup
ch.queueDeclare("live.updates", true, false, true, null);
```

**Listing 1.** The exclusive and auto-delete flags are independent declare arguments; combinations still need to make sense.

> [!warning] Auto-delete plus reconnect is a race
> A client that owns the only consumer of a well-known auto-delete queue and reconnects can lose the queue between deletion and re-declare — the broker deletes it as the old connection dies while the client re-declares it. Server-named queues or recovery delays are the documented workarounds.

> [!tip] Interview answer
> Exclusive means connection-private: other connections get RESOURCE_LOCKED, and the queue is deleted when the declaring connection closes — hence classic-only and effectively transient. Auto-delete drops the queue once the last consumer leaves after at least one subscribed. Both are for client-local state, not shared backlogs — the durable counterpart is [[What RabbitMQ queue types exist]].
