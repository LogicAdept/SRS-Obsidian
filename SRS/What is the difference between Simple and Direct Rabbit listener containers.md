<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #Java/Spring/AMQP #SRS

# What is the difference between Simple and Direct Rabbit listener containers?

> [!abstract] Short answer
> **`SimpleMessageListenerContainer` (SMLC)** is the historic default: each consumer has a **dedicated thread**; the Rabbit **client thread hands off** deliveries through an **internal queue**. Concurrency is **`concurrentConsumers`** (plus auto-scale via `maxConcurrentConsumers`). **`DirectMessageListenerContainer` (DMLC)** (since AMQP 2.0) invokes the listener **on the RabbitMQ client thread** — fewer hops, shared client threads, concurrency via **`consumersPerQueue`**. Boot default is Simple; switch with **`spring.rabbitmq.listener.type=direct`**. Retry **advice must sit on the factory of the type you actually run**.

## Handoff vs in-place invoke

SMLC exists because old Rabbit clients could not deliver concurrently on client threads. Newer clients can, so DMLC is architecturally **simpler**. A container listening to **several queues**: SMLC uses **one consumer thread for all those queues**; DMLC runs **a consumer per queue** (times `consumersPerQueue`).

SMLC-only (not on DMLC): **`batchSize`** with **transactions** (ack/commit every N messages — more duplicates after a crash); **`consumerBatchEnabled`**; **`maxConcurrentConsumers`** auto-scaling. DMLC has **`messagesPerAck`** to batch acks, but **not with transactions** — each message is its own tx/ack. You can still **change `consumersPerQueue` at runtime**; there is **no** SMLC-style auto-scaler.

DMLC wins: **add/remove queues** without cancelling every consumer; **no client→worker context switch**; threads **shared** across consumers (configure the connection factory thread pool — see “Threading and Asynchronous Consumers” in the AMQP reference) ([[How do you consume RabbitMQ messages in Spring Boot]], [[How does Spring AMQP retry work]]).

```java
factory.setConcurrentConsumers(3);     // SMLC
dmlc.setConsumersPerQueue(3);          // DMLC — not concurrentConsumers
```

**Listing 1.** Conceptual. Different knobs; copying SMLC properties onto a Direct factory does nothing useful.

```d2
direction: down
broker: "RabbitMQ" {
  width: 140
  height: 40
  style.fill: "#e8f5e9"
}
client: "Client thread(s)" {
  width: 160
  height: 40
  style.fill: "#fff3e0"
}
q: "SMLC internal queue" {
  width: 180
  height: 40
  style.fill: "#fce4ec"
}
worker: "Dedicated consumer thread" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
direct: "DMLC: listener on client thread" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
broker -> client
client -> q: "SMLC handoff"
q -> worker
client -> direct: "DMLC invoke"
```

**Fig. 1.** Simple decouples client I/O from your listener; Direct does not.

> [!warning] A blocking DMLC listener stalls the client thread
> Your `@RabbitListener` **is** the Rabbit consumer thread. Slow I/O or a retry **sleep** on that thread delays **other** work sharing the client pool. SMLC isolates that onto the dedicated worker (the client thread only enqueues). Put retry interceptors on **whichever** `*RabbitListenerContainerFactory` Boot is using.

> [!warning] `concurrentConsumers` is not DMLC
> Interview mix-up: Direct uses **`consumersPerQueue`**. SMLC **restarts all consumers** when you add/remove a queue at runtime; Direct cancels only the affected queue.

> [!tip] Interview answer
> Simple: worker threads + handoff queue, `concurrentConsumers`, optional scaling and transactional `batchSize`. Direct: listener on the AMQP client thread, `consumersPerQueue`, cheaper queue changes, no SMLC auto-scale. Boot is Simple until you set `listener.type=direct`. Match retry advice to that container.
