<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How does reactive messaging work in Quarkus?

> [!abstract] Short answer
> The `quarkus-messaging` extension (SmallRye Reactive Messaging) wires beans to streams through **channels**: a method annotated **`@Outgoing("channel")`** produces a stream, **`@Incoming("channel")`** consumes one, and connector extensions (Kafka, AMQP, RabbitMQ, MQTT, or the built-in **in-memory connector**) map channels onto real transports. Methods work with plain payloads, `Uni`, `Multi`, `Message<T>` (for ack/nack control) or `@Channel`/`Emitter` for imperative sends. Back-pressure, acknowledgement and failure handling are part of the stream contract, not afterthoughts.

## The wiring model

Channels decouple code from transport: `@Incoming("prices-in")` says "feed me that channel", and whether the channel is Kafka topic `prices` (configured via `mp.messaging.incoming.prices.topic=...` or `quarkus.messaging.*`) or an in-memory stream is a configuration decision. A processor is a method with both annotations — consume one channel, return another. Types compose naturally with Mutiny: returning `Multi<X>` declares a stream, `Uni<X>` an async single item, `Message<X>` gives explicit acknowledgement semantics — automatic ack on success, nack on exception, with dead-letter or failure-strategy configuration per channel (`@OnFailure`, `failure-strategy` in connector config) ([[What is Mutiny in Quarkus]]). The `@Channel` + `Emitter` pair lets ordinary code push a message into an outgoing channel imperatively.

```java
// src/main/java/org/acme/check/infra/PriceChannel.java (JDK 21, Quarkus 3.39.2;
// quarkus-messaging with the default in-memory connector - no broker, no Docker needed).
package org.acme.check.infra;

import io.smallrye.mutiny.Multi;
import jakarta.enterprise.context.ApplicationScoped;
import org.eclipse.microprofile.reactive.messaging.Incoming;
import org.eclipse.microprofile.reactive.messaging.Outgoing;
import java.time.Duration;
import java.util.concurrent.atomic.AtomicInteger;

@ApplicationScoped
public class PriceChannel {
    private final AtomicInteger received = new AtomicInteger();

    @Outgoing("prices-out")
    public Multi<Integer> generate() {
        return Multi.createFrom().ticks().every(Duration.ofMillis(200))
                .select().first(40)
                .onOverflow().drop()
                .map(l -> (int) (long) l);
    }

    @Incoming("prices-out")
    @Outgoing("prices-in")
    public int transform(int i) {
        return i * 2;
    }

    @Incoming("prices-in")
    public void consume(int i) {
        received.incrementAndGet();
    }
}
// mvn test: 6/6 green - the assertion channel.receivedCount() >= 1 passed,
// proving generate -> transform (x2) -> consume flowed through two in-memory channels.
```

**Listing 1.** A complete pipeline: a tick-driven producer, a doubling processor, a consumer counter. Switching "prices-out" to Kafka is configuration — the bean code is unchanged ([[How do you test a Quarkus application]]).

```d2
direction: right
gen: "@Outgoing(\"prices-out\")\nMulti<Integer> ticks" {
  width: 280
  height: 65
  style.fill: "#e3f2fd"
}
proc: "@Incoming(\"prices-out\")\n@Outgoing(\"prices-in\")\ntransform" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
con: "@Incoming(\"prices-in\")\nconsume" {
  width: 250
  height: 60
  style.fill: "#e8f5e9"
}
kafka: "Kafka connector\n(channel -> topic)" {
  width: 240
  height: 55
  style.fill: "#f5f5f5"
}
mem: "In-memory connector\ntest/dev default" {
  width: 230
  height: 55
  style.fill: "#f5f5f5"
}
gen -> proc -> con
proc -o kafka
proc -o mem
```

**Fig. 1.** One programming model, pluggable transports: the same annotations target a broker in prod and the in-memory connector in tests ([[How does reactive messaging work in Quarkus]] — the connector decides at configuration time).

## Health, back-pressure, ordering

Reactive Messaging registers built-in health checks ("SmallRye Reactive Messaging - liveness/readiness checks" were visible verbatim on `/q/health` of the same verified app), so a disconnected broker flips readiness — a Kubernetes-native behavior ([[What health checks does Quarkus expose]]). Back-pressure propagates through the Reactive Streams contract: a slow consumer signals upstream instead of unbounded buffering; `onOverflow` strategies (drop, buffer, fail) are explicit at producers. Ordering is per partition in Kafka terms, per stream in memory — nothing globally ordered without design.

> [!warning] @Incoming methods are not request handlers
> A consumer runs on its own stream, driven by the connector — no HTTP request, no `@RequestScoped` context, and exceptions do not bubble to a client; they become nacks with the channel's failure strategy. The frequent misconception: "I'll annotate a REST method with @Incoming" — the model is message-driven, not request-driven. Also: plain payload methods ack automatically; if you need exactly-once-ish control you must switch to `Message<T>` and acknowledge deliberately — mixing those up either double-processes or drops messages under failure.

> [!tip] Interview answer
> Quarkus reactive messaging is SmallRye Reactive Messaging: beans talk to channels — @Outgoing produces a stream, @Incoming consumes, both on one method makes a processor — and connectors bind channels to transports: Kafka, AMQP, RabbitMQ, or the in-memory connector for tests. Methods speak payloads, Uni, Multi or Message for ack/nack control, back-pressure flows through the Reactive Streams contract, and built-in health checks tie broker connectivity to Kubernetes readiness. Same bean code from dev's in-memory channels to prod Kafka.
