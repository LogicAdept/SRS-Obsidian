<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud/Stream #Messaging/Tools/RabbitMQ #SRS

# What is Spring Cloud Stream used for with RabbitMQ?

> [!abstract] Short answer
> **Spring Cloud Stream** is a Boot framework for **message-driven** services: you write `Supplier` / `Function` / `Consumer` beans; a **binder** maps them to a broker. With **`spring-cloud-starter-stream-rabbit`**, that binder is RabbitMQ: a logical **destination** becomes a **topic exchange**; a **consumer group** becomes a **queue** bound to it (`destination.group`). Same function code can target Kafka or Rabbit by swapping the starter. Use **Spring AMQP** when you need first-class AMQP topology (arbitrary DLX args, confirms, channels) instead of the binder’s opinionated map.

## Binder vs AMQP types

Stream’s binder SPI binds producers and consumers to **named destinations**. Groups give **competing consumers** (one message per group member) while **different groups** each get a copy. No `group` → an **anonymous** auto-delete queue with a random name ([[How do you consume RabbitMQ messages in Spring Boot]], [[What is RabbitMQ]]).

Rabbit binder defaults:

- Destination → `TopicExchange`
- Grouped consumer → durable-style queue `destination.group`
- Partitioned bindings suffix the queue and use the partition index as routing key

You still configure the broker with `spring.rabbitmq.*`. Rabbit-only knobs sit under `spring.cloud.stream.rabbit.bindings.<name>.consumer.` (and producer): `autoBindDlq`, `republishToDlq`, `requeueRejected`, `maxAttempts`. Failed messages can go to `destination.dlq` after binder retries (`maxAttempts > 1`) or a reject when retry is off. You can run **two binders** (Kafka in, Rabbit out) in one app.

```java
@SpringBootApplication
public class OrdersApp {

	@Bean
	public Function<String, String> uppercase() {
		return value -> value.toUpperCase();
	}
}
```

**Listing 1.** Conceptual. Bindings default to `uppercase-in-0` / `uppercase-out-0`; set `spring.cloud.function.definition` when more than one function bean exists.

```
spring.cloud.function.definition=uppercase
spring.cloud.stream.bindings.uppercase-in-0.destination=orders
spring.cloud.stream.bindings.uppercase-in-0.group=fulfillment
```

**Listing 2.** Conceptual. Exchange `orders`, queue `orders.fulfillment`.

```d2
direction: down
fn: "Function / Consumer bean" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
binder: "Rabbit binder" {
  width: 180
  height: 40
  style.fill: "#fff3e0"
}
ex: "TopicExchange\norders" {
  width: 180
  height: 45
  style.fill: "#e8f5e9"
}
q: "Queue\norders.fulfillment" {
  width: 200
  height: 45
  style.fill: "#fce4ec"
}
fn -> binder
binder -> ex
ex -> q
```

**Fig. 1.** Stream hides AMQP types; the Rabbit binder still creates exchange + group queue ([[How does a message flow through RabbitMQ]]).

> [!warning] `requeueRejected=true` without a DLQ loops
> With `republishToDlq=false`, requeue-on-failure **redelivers forever**. Enable binder retry (`maxAttempts > 1`) or `republishToDlq`, or reject to a DLX. `ImmediateAcknowledgeAmqpException` **skips** the DLQ and discards.

> [!warning] Anonymous consumers are not a shared work queue
> Omit `group` and each instance gets its **own** auto-delete queue — pub/sub, not competing consumers. That is easy to miss when you expected Kafka-style group load balancing.

> [!tip] Interview answer
> Stream + Rabbit is the binder: functions in, topic exchange and group queues out, so the same app can switch Kafka vs Rabbit. AMQP details leak through Rabbit binding properties and DLQ flags. Reach for Spring AMQP when the binder’s topology is the constraint, not the programming model.
