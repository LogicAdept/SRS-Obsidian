<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What does the RabbitMQ mandatory flag do

> [!abstract] Short answer
> `mandatory` is a per-publish flag that turns silent drops into returns: if the exchange cannot route the message to any queue, the broker sends the message back to the publisher with `basic.return` instead of discarding it. Default is false — unroutable messages are dropped or sent to an alternate exchange.

## Return path mechanics

The flag rides on `basic.publish`. When no binding matches, the broker writes a `basic.return` carrying the full message plus a reply-code (312 NO_ROUTE) to the publishing channel; a return listener on that channel receives it. For a confirmed channel, the confirm for an unroutable mandatory publish arrives after the return — the broker confirms "I saw it, and it went nowhere". With `mandatory=false` the message is simply discarded or diverted by an [[What is a RabbitMQ alternate exchange|alternate exchange]], if configured. See [[What is a RabbitMQ exchange]] for why routing happens before storage.

```d2
direction: down
pub: "basic.publish\nmandatory=true" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
ex: "exchange\nno matching binding" {
  width: 250
  height: 80
  style.fill: "#fff3e0"
}
ret: "basic.return\n312 NO_ROUTE to publisher" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
ack: "confirm (after return)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
pub -> ex
ex -> ret
ex -> ack
```

**Fig. 1.** Unroutable mandatory publish: the return reaches the publisher first, then the channel confirm closes the episode.

## What mandatory does not cover

Mandatory speaks only about *routing*. A routed message that later sits in a queue can still expire, be overflowed out, or be dead-lettered — none of that returns anything to the publisher; those paths belong to [[What is message TTL and queue max-length in RabbitMQ]] and [[What is a RabbitMQ dead letter exchange]]. Nor does mandatory guarantee delivery to consumers: it guarantees the message reached at least one queue.

```java
ch.addReturnListener(r ->
        log.warn("unroutable: {}", r.getRoutingKey()));
ch.basicPublish("orders", "no.such.key",
        MessageProperties.PERSISTENT_TEXT_PLAIN, body,
        true,   // mandatory
        null);
```

**Listing 1.** The Java client's `basicPublish` overload with the mandatory flag plus a return listener to catch the bounce.

> [!warning] Without a return listener the flag does nothing
> Setting mandatory and ignoring returns reproduces the default behaviour with extra steps: the broker returns the message, nobody consumes the return, the message is gone anyway. Mandatory is only meaningful together with a return handler or an AMQP-library that surfaces returns as errors.

> [!tip] Interview answer
> Mandatory flips unroutable publishes from silent drop to basic.return back to the publisher, which needs a return listener; the confirm then follows. It covers routing only — queue-side expiry or dead-lettering never returns anything — and it pairs with alternate exchanges as the two unroutable-message strategies.
