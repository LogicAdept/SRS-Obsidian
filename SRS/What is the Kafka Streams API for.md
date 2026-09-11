<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka Streams API for?

> [!abstract] Short answer
> Stateful stream processing between topics, as a Java library: it builds a topology of processors that reads input topics, transforms records — aggregations, joins, windowing on event time — and writes output topics, keeping intermediate state in fault-tolerant local stores backed by changelog topics. It is a separate artifact (`kafka-streams`), not a nicer consumer ([[What core Kafka APIs exist]]).

## The vocabulary: streams, tables, topology

A `KafkaStreams` instance runs a *processor topology*: source processors consume from topics, intermediate processors transform one record at a time, sink processors write results back. The high-level DSL expresses this with `KStream` and `KTable`: a `KStream` is an unbounded sequence of records where each one is an event; a `KTable` is the changelog view of a table, where each record with a key is an upsert. The two are dual — a stream is a table's changelog, and replaying it rebuilds the table — which is the same mechanism log compaction and change-data-capture use ([[What is Kafka log compaction]]). That duality has a concrete API consequence: an aggregation over a `KStream` returns a `KTable`, so later records for the same key update the running value instead of appending new events.

```java
Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "orders-analytics");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

StreamsBuilder builder = new StreamsBuilder();
builder.stream("orders")
    .groupBy((k, order) -> order.city())
    .count(Materialized.as("orders-by-city"))   // stateful: local store + changelog
    .toStream()
    .to("orders-by-city-counts");
new KafkaStreams(builder.build(), props).start();
```

**Listing 1.** A DSL topology: read a topic, group and count into a named state store, republish the table as a stream. `application.id` names the consumer group and the internal topics.

## State, time, and scaling

Stateful operators — `count`, `aggregate`, joins — run against *state stores* embedded in each task: persistent RocksDB stores or in-memory maps, restored after a rebalance by replaying their changelog topics, which is what makes the state fault-tolerant. Named stores are queryable read-only from outside the application through Interactive Queries. Time is event-driven: every record gets a timestamp from a `TimestampExtractor`, and window operators (`TimeWindows`, `SlidingWindows`, `SessionWindows`) group records per key into windows whose clock is *stream time* — it advances when records arrive, not by wall clock. A record whose timestamp lands in a window after that window's end plus its *grace period* is discarded rather than applied, which is the out-of-order-data control ([[What ordering guarantees does Kafka provide for messages]]). Scaling follows Kafka's own model: partitions of the input topics become tasks, so the parallelism ceiling is the partition count ([[What happens if you have more Kafka consumers than partitions]]).

```d2
direction: right
orders: "orders topic" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
task: "Stream task\ngroupBy + count" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
store: "Local state store\norders-by-city" {
  width: 230
  height: 90
  style.fill: "#fff3e0"
}
changelog: "changelog topic\n(compacted, restores state)" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
out: "orders-by-city-counts" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
orders -> task
task -> store
store -> changelog: backup
task -> out: results
```

**Fig. 1.** A stateful aggregation: the task keeps the running count in a local store, the store's changelog topic restores it after failure or rebalance, and results flow to the output topic.

Exactly-once processing is a config flag, not extra code: `processing.guarantee=exactly_once_v2` commits input offsets, state updates, and output writes atomically using producer transactions under the hood ([[How do you achieve exactly-once processing in Kafka]]); it requires brokers 2.5 or newer, and the older v1 implementation is deprecated since Kafka 3.0. Lifecycle is explicit: `start()` launches the streams threads and `close()` shuts them down — the contract notes you must `close()` an instance even if you never started it, or it leaks resources.

> [!warning] An aggregation gives you a table, not a log
> Downstream of `count` or `aggregate` you are looking at upserts per key — a `KTable` — even if the upstream looked like a firehose. Code that assumes every record is a new appended event (per-key counters, audit trails) silently misbehaves; call `toStream()` deliberately to turn the table back into a change stream.

> [!tip] Interview answer
> Streams is a library for turning input topics into output topics with state: KStream for events, KTable for upserts, windowing on event time with a grace period for late data, local state stores restored from changelog topics, and exactly-once via processing.guarantee=exactly_once_v2. It scales by input partitions and lives inside your process — choose it when the logic is stateful transformations, and a plain consumer when it is just forwarding.

