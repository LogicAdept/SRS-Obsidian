<!--
reps: 0
priority: 0
-->
#Java/Spring/Kafka #Messaging/Tools/Kafka #SRS

# How do you configure a Spring Kafka producer and listener?

> [!abstract] Short answer
> Add **`spring-boot-starter-kafka`**. Boot auto-configures **`KafkaTemplate`** and a **`kafkaListenerContainerFactory`** from **`spring.kafka.*`**. Produce with **`kafkaTemplate.send(topic, key, payload)`**. Consume with **`@KafkaListener(topics = …, groupId = …)`**. Tune producer **`acks`**, serializers, and extra client keys via **`spring.kafka.producer.properties`**. Tune the listener with **`spring.kafka.listener.concurrency`** (or `concurrency` on the annotation). A **`CommonErrorHandler`** bean (typically **`DefaultErrorHandler` + `DeadLetterPublishingRecoverer`**) is wired onto the default factory. Boot tests: **`@EmbeddedKafka(bootstrapServersProperty = "spring.kafka.bootstrap-servers")`**.

## Auto-config, then send and listen

`spring.kafka.*` maps onto Apache Kafka client properties (hyphenated or camelCase → dotted Kafka names). Common keys apply to every client; `producer` / `consumer` / `admin` override. A **`NewTopic`** bean creates the topic on startup if it is missing.

```properties
spring.kafka.bootstrap-servers=${KAFKA_BOOTSTRAP_SERVERS}
spring.kafka.consumer.group-id=myGroup
spring.kafka.producer.acks=all
spring.kafka.producer.properties[enable.idempotence]=true
spring.kafka.producer.value-serializer=org.springframework.kafka.support.serializer.JacksonJsonSerializer
spring.kafka.listener.concurrency=3
```

**Listing 1.** Boot producer/listener knobs. `acks` is a first-class property; **`enable.idempotence`** goes through **`properties[]`**. Current Boot JSON type is **`JacksonJsonSerializer`** (dumps still say `JsonSerializer`). Trusted packages / default type belong on the **consumer** Jackson deserializer. Quote YAML `"*"`-style keys as in the Boot Kafka appendix ([[Which common Spring Boot starters do you know]]).

```java
this.kafkaTemplate.send("someTopic", "Hello");
this.kafkaTemplate.send("someTopic", key, payload);
```

**Listing 2.** Auto-wired **`KafkaTemplate`**. Overloads include key, partition, timestamp, `ProducerRecord`, and `Message`. `send` returns **`CompletableFuture<SendResult<K,V>>`**. Keys matter for partitioning ([[Why do Kafka producer keys matter]]). `spring.kafka.producer.transaction-id-prefix` auto-configures **`KafkaTransactionManager`**.

```java
@Component
public class MyBean {

	@KafkaListener(topics = "someTopic", groupId = "myGroup", concurrency = "3")
	public void processMessage(String content) {
		// ...
	}
}
```

**Listing 3.** Boot: **no** `@EnableKafka` required (plain `spring-kafka` does). `id` becomes **`group.id`** unless you set **`groupId`**. `concurrency` on the annotation overrides the factory / `spring.kafka.listener.concurrency`. That value is how many **`KafkaMessageListenerContainer`** children **`ConcurrentMessageListenerContainer`** starts. Kafka then assigns **partitions in the consumer group**. Extra members sit **idle** (especially with default **`RangeAssignor`** across several topics). Manual assignment: if concurrency **exceeds** the `TopicPartition` count, Spring **lowers** concurrency. Manual ack: `ackMode = "MANUAL"` (Spring Kafka **4.1+**) and `Acknowledgment.acknowledge()` — default **`AckMode` is `BATCH`**; the container sets **`enable.auto.commit=false`** unless you set it ([[Why is Kafka enable.auto.commit dangerous]]).

Register a **`CommonErrorHandler`** (Boot attaches it to the default factory):

```java
@Bean
CommonErrorHandler kafkaErrorHandler(KafkaTemplate<Object, Object> template) {
	return new DefaultErrorHandler(
			new DeadLetterPublishingRecoverer(template),
			new FixedBackOff(1000L, 2L));
}
```

**Listing 4.** After retries, **`DeadLetterPublishingRecoverer`** publishes to a DLT (default destination resolver: same partition, topic + **`-dlt`**). Default recoverer only **logs** after **`FixedBackOff(0L, 9)`** (ten attempts). Throw **`RuntimeException`**, not **`Error`**, or the handler is skipped.

```java
@SpringBootTest
@EmbeddedKafka(topics = "someTopic", bootstrapServersProperty = "spring.kafka.bootstrap-servers")
class MyTest {
}
```

**Listing 5.** Official Boot wiring of **`spring-kafka-test`**. Alternatives: map `EmbeddedKafkaBroker.BROKER_LIST_PROPERTY`, or `spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}`.

```d2
direction: down
props: "spring.kafka.*\nKafkaProperties" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
prod: "KafkaTemplate.send" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
lis: "@KafkaListener\nConcurrentMessageListenerContainer" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

props -> prod
props -> lis
```

**Fig. 1.** One property namespace; two auto-configured clients. A custom factory bean **replaces** the default — you then own error handler, concurrency, and converters yourself.

> [!warning] Concurrency is not “threads per partition”
> `concurrency=N` is **N consumers in the group**. More consumers than partitions wastes members. On **several topics**, default **RangeAssignor** can leave most of those N **idle**. Override `partition.assignment.strategy` if that is not what you want.

> [!warning] `@EnableKafka` vs the Boot starter
> Standalone Spring Kafka needs **`@EnableKafka`** plus a **`kafkaListenerContainerFactory`**. The Boot starter already provides both. Adding a **custom** factory bean means Boot **does not** create the default — your `CommonErrorHandler` bean will not attach unless you set it on **that** factory.

> [!tip] Interview answer
> In Spring Boot I add spring-boot-starter-kafka, set spring.kafka.bootstrap-servers and group-id, inject KafkaTemplate to send, and put @KafkaListener on a method to consume. Concurrency is the number of child containers in the consumer group, so I keep it at or below partition count. I register DefaultErrorHandler with DeadLetterPublishingRecoverer for retries and a DLT, and I test with @EmbeddedKafka remapped onto spring.kafka.bootstrap-servers.
