<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What core Kafka APIs exist?

> [!abstract] Short answer
> Kafka 4.x ships **six core APIs**: **Producer**, **Consumer**, **Share Consumer** (cooperative consumption in share groups), **Streams**, **Connect**, and **Admin**. All of them speak the same language-independent wire protocol; only the Java clients are maintained inside the Apache Kafka project itself.

## The six, in one line each

- **Producer** — sends records to topics; handles partitioning, batching, retries, idempotence.
- **Consumer** — subscribes to topics and polls records, coordinating with a group.
- **Share Consumer** — records are delivered to consumers in a share group individually, acknowledging each one, instead of partition-locked assignment (introduced for queue-like workloads).
- **Streams** — a Java library that turns input topics into output topics with stateful operators: aggregations, joins, windowing, event-time processing.
- **Connect** — runs reusable **connectors** that continuously pull from source systems into Kafka or push from Kafka into sinks, so integration rarely needs hand-written producers.
- **Admin** — creates and inspects topics, configs, ACLs, consumer group offsets; what CLI tools are built on.

## How they fit together

The Producer and Consumer APIs are the substrate: Streams applications are consumers plus producers with a state layer, Connect workers run connector tasks that use both, and tooling uses Admin. In practice you write a custom consumer or producer only when an existing connector or framework does not fit — [[How would you explain Spring Kafka]] wraps the two raw clients for application code, and [[What is the Kafka Streams API for]] and [[What is the Kafka Connector API for]] cover the higher-level layers.

Where each one runs matters too. Producer and Consumer live inside your application's process and talk straight to the brokers. Streams also runs in your process, but adds state directories and internal changelog topics, so an instance is both a consumer group member and a stateful processor. Connect is a separate distributed service: connectors run on Connect workers, so an integration outage lands on the worker cluster, not on your app. Admin is usually embedded in operational tooling rather than in request paths.

All of this rides on one wire protocol whose version is negotiated per connection, which is why the Java client from the matching release line (kafka-clients 4.3.1 for a 4.3 broker) is the safe pairing, and why mixing very old clients with a modern cluster needs a compatibility check.

```java
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
    producer.send(new ProducerRecord<>("orders", "u1", "order-created"));
}
```

**Listing 1.** The raw Producer API from kafka-clients 4.3.1: a config object, serializers, and a send that returns a future.

> [!warning] Streams is not “a better consumer”
> The Streams API is a full stream-processing library with state stores and exactly-once plumbing, not a shortcut API on the Consumer. Reaching for Streams adds state directories, changelog topics, and rebalance semantics — for a plain consume-transform-produce loop the Consumer API is the right size.

> [!tip] Interview answer
> Six core APIs: Producer to write, Consumer to read, Share Consumer for queue-style group consumption, Streams for stateful processing between topics, Connect for source and sink integration, and Admin for management. They all use Kafka's client protocol, with Java clients first-class and everything else community-maintained. Most integration needs are met by Connect connectors rather than hand-rolled clients.

