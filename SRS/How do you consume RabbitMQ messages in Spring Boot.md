<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #Java/Spring/AMQP #SRS

# How do you consume RabbitMQ messages in Spring Boot?

> [!abstract] Short answer
> Boot’s **`spring-boot-starter-amqp`** auto-configures a **`CachingConnectionFactory`**, **`RabbitAdmin`**, **`AmqpTemplate` / `RabbitTemplate`**, and a **`SimpleRabbitListenerContainerFactory`**. Consume with **`@RabbitListener`** on a Spring bean method. The **container** (Simple by default; Direct via `spring.rabbitmq.listener.type=direct`) pulls deliveries and invokes the method. Publish with `convertAndSend`. Topology is **`Queue` / `Exchange` / `Binding` beans** or `@RabbitListener(bindings = @QueueBinding(…))`. It is **not** Spring Cloud Stream.

## Listener endpoint

`@RabbitListener(queues = "someQueue")` needs the queue to **exist** (or a `RabbitAdmin` plus a `Queue` bean / `queuesToDeclare` / `bindings`). `bindings = @QueueBinding` declares queue, exchange, and routing key. Empty `@Queue` is an **anonymous** exclusive auto-delete queue. `queues`, `bindings`, and `queuesToDeclare` are **mutually exclusive**. Boot wires a **`MessageConverter`** bean onto the default factory if you define one (JSON is a `Jackson2JsonMessageConverter` you add — not the default `SimpleMessageConverter` of the adapter) ([[What is the difference between Simple and Direct Rabbit listener containers]], [[How does Spring AMQP retry work]]).

The container is the **active** part: `ConnectionFactory` + queue names + listener callback (`MessageListener`, `ChannelAwareMessageListener` for the AMQP `Channel`, or the annotation adapter). Prefetch default since 2.0 is **250** (was 1).

```java
@Component
public class OrderListener {

	@RabbitListener(queues = "orders")
	public void process(String body) {
		// payload after MessageConverter
	}
}
```

**Listing 1.** Conceptual. Boot creates a Simple container unless you set `listener.type=direct` or `containerFactory`.

```java
@RabbitListener(bindings = @QueueBinding(
		value = @Queue(value = "orders", durable = "true"),
		exchange = @Exchange(value = "orders.exchange"),
		key = "order.created"))
public void processOrder(Order order) { /* ... */ }
```

**Listing 2.** Conceptual. `RabbitAdmin` declares queue, exchange, and binding on connect.

```d2
direction: down
broker: "RabbitMQ queue" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
c: "Listener container\nSimple or Direct" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
m: "@RabbitListener method" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
broker -> c: "deliver"
c -> m: "converter + invoke"
```

**Fig. 1.** Container owns consume/ack; your method stays a POJO ([[How does a message flow through RabbitMQ]]).

Manual ack: `AcknowledgeMode.MANUAL` and a `Channel` argument (`ChannelAwareMessageListener` / adapter that passes channel). AUTO (typical) acks after a successful listener return; a thrown exception is handled by the container (requeue unless you reject).

> [!warning] Listener exception without retry requeues forever
> If Boot **listener retry is off** (the default) and the method throws, the broker **redelivers** (`defaultRequeueRejected` true). Poison messages loop. Enable listener retry, set `defaultRequeueRejected=false`, or throw `AmqpRejectAndDontRequeueException` (and configure a DLX).

> [!warning] Prefetch 250 vs ordering
> High prefetch improves throughput; for **strict order** or **large/slow** messages, drop prefetch (often to **1**) or you buffer many unacked bodies in the client.

> [!tip] Interview answer
> Boot AMQP: `@RabbitListener` plus a listener container on `spring-boot-starter-amqp`. Declare topology as beans or `@QueueBinding`. `RabbitTemplate` sends. Simple vs Direct is the container type; retry and ack mode live on that container, not on the annotation alone.
