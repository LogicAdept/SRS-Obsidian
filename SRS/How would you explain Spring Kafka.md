<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Java/Spring/Kafka #SRS

# How would you explain Spring Kafka?

> [!abstract] Short answer
> **Spring for Apache Kafka** wraps the Kafka **Producer** and **Consumer** in Spring types: **`KafkaTemplate`** to **send**, **`@KafkaListener`** plus a **`ConcurrentKafkaListenerContainerFactory`** to **receive**. Boot (`spring-boot-starter-kafka`) auto-configures both from **`spring.kafka.*`** (`bootstrap-servers`, `consumer.group-id`, serializers). It is **not** Kafka itself, **not** Kafka Streams (that is an opt-in `@EnableKafkaStreams`), and **not** Spring Cloud Stream (a binder on top).

## Send and listen

`KafkaTemplate.send(topic, key, value)` (and overloads) returns a **`CompletableFuture<SendResult>`**. Listeners need `@EnableKafka` when you wire the factory yourself; Boot supplies a default factory named **`kafkaListenerContainerFactory`**. `@KafkaListener(topics = "…", groupId = "…", concurrency = n)` builds a **`ConcurrentMessageListenerContainer`**: `concurrency` is how many **`KafkaMessageListenerContainer`** children run. Each child is **one thread / one Kafka consumer**. Kafka **assigns partitions**; **one partition is processed sequentially** on its consumer ([[How do you configure a Spring Kafka producer and listener]], [[What is Apache Kafka]]).

If `concurrency` **exceeds** assigned partitions (static `TopicPartitionOffset`s), Spring **lowers** concurrency so each child gets a partition. With **group management** and the default **`RangeAssignor`**, extra consumers can sit **idle** (classic: many topics × `concurrency` larger than partitions-per-topic). Client `acks`, `enable.idempotence`, serializers live in **`ProducerConfig` / `ConsumerConfig`** (Boot: `spring.kafka.producer.*` / `consumer.*`).

```java
@Component
public class OrderKafka {

	private final KafkaTemplate<String, String> kafka;

	public void publish(String id, String json) {
		this.kafka.send("orders", id, json);
	}

	@KafkaListener(topics = "orders", groupId = "fulfillment", concurrency = "3")
	public void consume(String json) { /* ... */ }
}
```

**Listing 1.** Conceptual. Template send; listener concurrency is child containers, not threads per partition.

```d2
direction: down
tpl: "KafkaTemplate.send" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
topic: "topic partitions" {
  width: 180
  height: 40
  style.fill: "#fff3e0"
}
cmlc: "ConcurrentMessageListenerContainer\nconcurrency = 3" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
c1: "child consumer" {
  width: 140
  height: 40
  style.fill: "#fce4ec"
}
c2: "child consumer" {
  width: 140
  height: 40
  style.fill: "#fce4ec"
}
c3: "child consumer" {
  width: 140
  height: 40
  style.fill: "#fce4ec"
}
tpl -> topic
topic -> cmlc
cmlc -> c1
cmlc -> c2
cmlc -> c3
```

**Fig. 1.** Produce through the template; consume through N child containers that Kafka load-balances by partition.

Listener failures: container **`DefaultErrorHandler`** (retries + backoff). Default recoverer **logs** the record; **`DeadLetterPublishingRecoverer`** publishes to a DLT. Boot wires a **`CommonErrorHandler`** bean onto the default factory. Manual ack: `AckMode.MANUAL` / `MANUAL_IMMEDIATE` and an `Acknowledgment` argument. Tests: **`@EmbeddedKafka`** (`spring-kafka-test`); point Boot at it with `bootstrapServersProperty = "spring.kafka.bootstrap-servers"`.

> [!warning] Concurrency is not “threads per partition”
> Kafka still gives **at most one consumer in the group per partition**. Surplus `concurrency` is idle or scaled down. Same-partition order is kept **inside** a child; it is not a way to parallelize one partition.

> [!warning] `RangeAssignor` + many topics
> Three topics × five partitions and `concurrency=15` can leave **ten idle** consumers. Switch `partition.assignment.strategy` (for example RoundRobin) if you expected 15 busy children.

> [!tip] Interview answer
> Spring Kafka is `KafkaTemplate` plus `@KafkaListener` on the Kafka client. Concurrency is extra consumers in the group — cap it by partitions and the assignor. Failures go through `DefaultErrorHandler`; a DLT is `DeadLetterPublishingRecoverer`, not magic. Producer `acks`/`idempotence` are still Kafka producer configs.
