<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS

# What is the Dead Letter Channel pattern?

> [!abstract] Short answer
> A **Dead Letter Channel** is where the **messaging system** puts a message it **cannot or should not deliver** — after retries failed, the queue no longer exists, TTL passed, or length limits reject it. The broker, not the application, performs the move; in most products the channel is a queue called a **DLQ**.

## When the messaging system gives up

The exact behavior is implementation-specific — some systems provide one, some do not. Usually each machine running the messaging system has a **local** dead letter channel, so a dying message hops between local queues without network uncertainty, and the move records where the message died plus the original destination channel. Concrete mechanics differ by product: JMS providers speak of a "dead message queue", MQSeries of a DLQ; RabbitMQ routes rejected, expired, or overflowed messages through the `x-dead-letter-exchange` argument of the queue; Amazon SQS ships a redrive policy that redirects a source queue to a DLQ after `maxReceiveCount`. This is delivery-side plumbing — the receiver-side counterpart for unprocessable content is [[What is the Invalid Message Channel pattern]], and the boundary between them is drawn in [[What is the difference between Invalid Message Channel and Dead Letter Channel]].

```d2
direction: down
pub: "Producer" {
  width: 160
  height: 55
  style.fill: "#e3f2fd"
}
q: "Work queue\nretry redeliveries" {
  width: 220
  height: 65
  style.fill: "#fff3e0"
}
dlc: "Dead Letter Channel\n(DLQ on the broker)" {
  width: 250
  height: 70
  style.fill: "#ffebee"
}
ops: "Operator / replayer" {
  width: 200
  height: 55
  style.fill: "#e8f5e9"
}
pub -> q
q -> q: "cannot deliver:\nretry N times"
q -> dlc: "move, record\noriginal channel"
dlc -> ops```

**Fig. 1.** The messaging system retries delivery first; only after it gives up does the message land on the dead letter channel.

## RabbitMQ wiring

```java
Map<String, Object> args = Map.of(
    "x-dead-letter-exchange", "orders.dlx",
    "x-dead-letter-routing-key", "orders.parking");
channel.queueDeclare("orders.work", true, false, false, args);
// reject/nack with requeue=false, TTL expiry, or overflow
// now dead-letter the message into orders.dlx -> parking queue
```

**Listing 1.** Declaring the work queue with a dead-letter exchange is enough: the broker reroutes rejected or expired messages; the application code only has to `nack(requeue=false)`.

> [!warning] DLQ is not a trash can and not a retry queue
> Messages in a DLQ still need an owner: an operator or replayer who inspects, fixes, and resubmits them — or an explicit TTL policy that drops them. A DLQ that grows silently is a delayed outage, and using it as a "retry later" mechanism without a replay path just parks failed business processes.

> [!tip] Interview answer
> A Dead Letter Channel is broker-side: when the messaging system exhausts delivery attempts or hits TTL and length rules, it moves the message to a dead letter queue, recording the original destination. RabbitMQ implements it via `x-dead-letter-exchange`, SQS via a redrive policy. The key contrast: dead-lettering handles undeliverable messages, while an Invalid Message Channel handles delivered-but-unprocessable ones.
