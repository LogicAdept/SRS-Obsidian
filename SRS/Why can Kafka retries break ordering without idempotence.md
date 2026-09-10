<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# Why can Kafka retries break ordering without idempotence?

> [!abstract] Short answer
> With `enable.idempotence=false`, `retries > 0`, and `max.in.flight.requests.per.connection > 1`, the producer keeps sending while an earlier batch waits to retry: **batch 1 fails transiently, batch 2 succeeds, then batch 1's retry lands after it** — the partition log ends up with later records first. The idempotent producer prevents this by tagging batches with a producer id and per-partition sequence numbers, and the broker rejects anything out of sequence.

## The failure, step by step

The producer sends batches asynchronously; up to `max.in.flight.requests.per.connection` (default 5) can be unacknowledged on one connection. A transient error — leader switch, timeout — fails batch 1 only. While batch 1 waits to be retried, batches 2 and 3 succeed, so the retry of batch 1 appends *after* them even though its records were sent first. With `enable.idempotence=false` and `max.in.flight` greater than 1, records of a later batch can therefore appear in the partition before records of an earlier batch.

```java
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

public class OrderFragileProducer {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "false");
        props.put(ProducerConfig.RETRIES_CONFIG, 10);
        props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);
        try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
            producer.send(new ProducerRecord<>("orders", "step-1", "charge"));
            producer.send(new ProducerRecord<>("orders", "step-2", "ship"));
        }
    }
}
```

**Listing 1.** The risky combination, compile-checked against kafka-clients 4.3.1. The reordering itself only shows up when a broker hiccup coincides with in-flight batches, so the sequence below is conceptual, not output from this run.

```d2
direction: right
b1: "batch 1\nsent → fails" {
  width: 150
  height: 70
  style.fill: "#ffebee"
}
b2: "batch 2\nsent → ok" {
  width: 150
  height: 70
  style.fill: "#e8f5e9"
}
log2: "log: [batch 2]" {
  width: 170
  height: 50
  style.fill: "#fff3e0"
}
b1r: "batch 1 retried\nappends after b2" {
  width: 210
  height: 70
  style.fill: "#ffebee"
}
log1: "log: [batch 2, batch 1]" {
  width: 250
  height: 50
  style.fill: "#ffebee"
}
b1 -> b1r: transient error
b2 -> log2
b1r -> log1
```

**Fig. 1.** The retry mechanism reorders: batch 1 reaches the log after batch 2 despite being sent earlier.

## What idempotence changes

`enable.idempotence=true` (the **default since 3.0**) makes the producer register a producer id and attach sequence numbers per partition; the broker retains up to 5 batches per producer and accepts them strictly in sequence, so duplicates from retries are dropped and order survives. That is why the docs allow `max.in.flight` ≤ 5 with ordering preserved. Idempotence requires `acks=all` and `retries > 0` — and ties into delivery guarantees covered in [[What is the difference between Kafka acks 0 1 and all]] and [[What is an idempotent Kafka producer for]].

> [!warning] Modern Kafka reorders only if you opt out
> Since 3.0 idempotence is on by default, so "retries break order" describes a misconfiguration, not the norm. The real traps: explicitly setting `enable.idempotence=false` for order-sensitive topics, or combining explicit idempotence with `max.in.flight` above 5 — that throws `ConfigException` at startup rather than reordering.

> [!tip] Interview answer
> Retries resend a failed batch while newer batches keep flowing; with more than one unacknowledged request in flight, the retry can append after records that were sent later. The idempotent producer fixes it: producer id plus per-partition sequence numbers let the broker reject out-of-order or duplicate batches, with up to five in-flight requests. Since 3.0 this is the default, so reordering today means idempotence was disabled.

