<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messages #SRS

# What is the Message Expiration pattern?

> [!abstract] Short answer
> **Message Expiration** stamps a message with a **time limit for its usefulness**. Once it passes, consumers treat the message as if it had never been sent; most messaging systems reroute expired messages to a dead letter channel, others discard them — the choice is often configurable.

## Milk-carton semantics

Like an expiration date on milk: the grocer is supposed to pull expired cartons from the shelf, and if one still reaches your kitchen, you pour it out. In messaging terms: the broker should stop delivering expired messages, and a receiver that still gets one — already in flight — should discard it instead of processing. JMS exposes this as `JMSExpiration` (set via `TimeToLive` on the producer); AMQP 0-9-1 supports per-message `expiration` and per-queue `x-message-ttl`, with expired messages dead-lettered when a DLX is configured. Expiration is the standard companion of [[What is the Event Message pattern]] — stale events are worse than none — and it interacts with [[What is the Dead Letter Channel pattern]], because expiration is one of the canonical dead-letter triggers. Compare with [[What is the Guaranteed Delivery pattern]], which asks "will it survive", while expiration asks "is it still worth anything".

```d2
direction: right
pub: "Producer\nTTL = 30 s" {
  width: 170
  height: 60
  style.fill: "#e3f2fd"
}
q: "Queue\nmessage in flight" {
  width: 190
  height: 60
  style.fill: "#fff3e0"
}
fresh: "Consumer\nTTL ok -> process" {
  width: 210
  height: 65
  style.fill: "#e8f5e9"
}
exp: "TTL passed\n-> never process" {
  width: 210
  height: 65
  style.fill: "#ffebee"
}
pub -> q
q -> fresh: "delivered in time"
q -> exp: "expired: DLQ or discard"```

**Fig. 1.** The same queue delivers two very different fates depending on when the consumer finally gets the message.

## Setting and honoring TTL

```java
producer.setTimeToLive(30_000);          // header: JMSExpiration = now + 30s
producer.send(quotesTopic, event);
// Receiver side: in-flight messages can still be expired on arrival
if (message.getJMSExpiration() != 0 &&
        System.currentTimeMillis() > message.getJMSExpiration()) {
    return; // treat as never sent
}
```

**Listing 1.** The producer declares viability; the receiver double-checks because delivery races expiration at the queue boundary.

> [!warning] Expiration is computed against a clock, and clocks disagree
> `JMSExpiration` is producer-time plus TTL evaluated by the broker and by consumers on different machines; skew or a wrong timezone/NTP state silently shortens or extends message life. And beware RabbitMQ semantics details — per-message `expiration` only head-of-line expires lazily on delivery, so a stuck old message can block expiry of those behind it unless a per-queue TTL or lazy queue policy is used.

> [!tip] Interview answer
> Message Expiration is a header-declared lifespan: after it passes, the broker stops delivering the message — often dead-lettering it — and any consumer that already received it discards it. In JMS it is TimeToLive, in RabbitMQ per-message or per-queue TTL. Use it for time-sensitive data like quotes and events, and remember clocks skew, so receivers re-check expiry on arrival.
