<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Messaging/Tools/RabbitMQ #SRS

# What is the difference between Kafka and RabbitMQ?

> [!abstract] Short answer
> Different storage models for different jobs. RabbitMQ is a message broker: exchanges route each message to queues, consumers acknowledge, and the message is gone. Kafka is a distributed log: records append to partitioned, retained topics, consumers move offsets, and nothing disappears on read — so RabbitMQ excels at per-message routing and delivery semantics, Kafka at replayable, ordered, high-throughput streams ([[What are at-most-once at-least-once and exactly-once semantics in Kafka]]).

## Routing versus placement

```d2
direction: right
p: "Publisher" {
  width: 160
  height: 70
  style.fill: "#e3f2fd"
}
ex: "Exchange\ndirect / fanout /\ntopic / headers" {
  width: 230
  height: 100
  style.fill: "#fff3e0"
}
q: "Queues\nmessages held,\nacked then removed" {
  width: 230
  height: 110
  style.fill: "#ffebee"
}
k: "Kafka alternative\npartitioned log,\noffset per consumer" {
  width: 290
  height: 110
  style.fill: "#e8f5e9"
}
p -> ex -> q
p -> k
```

**Fig. 1.** RabbitMQ's model is routing-centric: publishers hit exchanges, bindings fan messages into queues, and acks drain them. Kafka's is placement-centric: the record's partition is its whole address.

In RabbitMQ the publisher sends to an exchange, and bindings — direct, fanout, topic, or headers exchanges — decide which queues receive copies; consumers subscribe or pull, acknowledge explicitly or auto, and the broker then removes the message. Undeliverable or rejected messages dead-letter; unacked messages can return. This is a per-message, queue-centric world: flexible routing, per-message TTLs and priorities, and consumption that genuinely consumes. Kafka replaces routing with partition placement — a record lands in one partition by key or stickiness, every consumer group reads it independently, and "delivery" is a committed offset, not a removal. Retention is time/size/compaction based, independent of consumer progress, which is why replay and new-consumer bootstrapping are native in Kafka and foreign in RabbitMQ ([[What is Kafka log compaction]], [[What is Kafka Consumer position for]]).

## Matching the tool to the workload

Workloads that fit RabbitMQ: work distribution where each job goes to exactly one worker, complex routing topologies, per-message deadlines, and moderate throughput with rich delivery semantics — acks, rejections, dead-lettering as first-class operations. Workloads that fit Kafka: event streaming where many independent systems consume the same events, ordering per key matters, throughput is high, and consumers must be able to re-read history or rebuild state — which is also why stream processing ecosystems (Streams, CDC pipelines) build on Kafka's model rather than on queues ([[What is the difference between a Kafka Consumer and Kafka Streams]], [[What is change data capture with Kafka]]). Scale-out shapes differ too: RabbitMQ scales with clustered queues and federation; Kafka scales with partitions and brokers, making consumer-side parallelism a property of the topic layout ([[How does Kafka achieve horizontal scalability]]).

> [!warning] Neither subsumes the other, and "Kafka is just faster" is the lazy answer
> Kafka's ordering, retention, and offset model come at the cost of routing flexibility and per-message semantics; RabbitMQ's queues cannot give you history or cheap multi-subscriber replay. A team replacing one with the other usually discovers the lost half late — queue semantics that Kafka never had, or stream semantics RabbitMQ has to simulate.

> [!tip] Interview answer
> RabbitMQ is an AMQP message broker: exchanges route each message into queues, consumers acknowledge, the message is removed — per-message routing, TTLs, dead-lettering, work-queue distribution. Kafka is a replicated partitioned log: records stay for retention, consumers move offsets per group, ordering is per partition, replay is native. Choose RabbitMQ for routing-rich work distribution; Kafka for ordered, replayable, multi-consumer event streams at scale.

