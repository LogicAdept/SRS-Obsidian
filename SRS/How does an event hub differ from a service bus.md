<!--
reps: 0
priority: 0
-->
#Messaging #DevOps/Cloud #SRS

# How does an event hub differ from a service bus

> [!abstract] Short answer
> **Azure Event Hubs** is an event *streaming* platform: an append-only, partitioned log built to ingest millions of events per second for telemetry and analytics, where consumers read by offset in a time-ordered stream. **Azure Service Bus** is an enterprise *message broker**: queues and pub/sub topics that deliver individual messages — commands — with transactions, sessions, dead-lettering, and pull delivery. One stores a sequence to be replayed; the other routes discrete work items until each is settled.

The distinction mirrors the general split between events and commands. An **event** announces that something happened (a sensor reading, a click, a log line); an **event stream** is a long series of such facts evaluated as they arrive or over windows. A **command** requests a specific action from a specific consumer and usually must be delivered exactly once and settled. Event Hubs is built for the first shape: an event hub is an append-only distributed log with **partitions** — ordered sequences that scale throughput like lanes on a freeway — and **consumer groups**, where each group independently tracks its offset and checkpoint position, so multiple applications can replay the same stream without competing. Retention is time-based (days, by tier), the Kafka protocol endpoint lets existing Kafka clients run unmodified, and nothing is "consumed away" — the log remains until retention expires.

```d2
direction: right
p1: "Producers\n(Kafka, AMQP, HTTPS)" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
eh: "Event Hubs\npartitions: append-only log" {
  width: 340
  height: 100
  style.fill: "#fff3e0"
}
cg1: "Consumer group A\nown offsets" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
cg2: "Consumer group B\nown offsets" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
p1 -> eh
eh -> cg1
eh -> cg2
```

**Fig. 1.** Event Hubs: one durable, partitioned stream, read independently by each consumer group via offsets.

## Service Bus solves the other problem

Service Bus starts where the stream ends: discrete messages that must each be processed once. **Queues** give point-to-point delivery with competing consumers — each message goes to exactly one worker, protected by a **peek-lock** so no two consumers process the same message. **Topics and subscriptions** give pub/sub, with per-subscription filters and actions; subscriptions behave like queues on the receiving side. The enterprise features are the point: atomic **transactions** across receive and send operations (process, post results, settle the input — all or nothing), **sessions** for FIFO ordering and request-reply correlation, a **dead-letter queue** holding messages that cannot be delivered or processed (the mechanism behind [[How would you explain ACK NACK DLQ]]), plus scheduled delivery and deferral. Delivery is pull — long-lived receive requests — so consumers decide when work happens.

> [!warning] The classic architecture mistake
> Treating them as interchangeable queues inverts the design: distributing *commands* through Event Hubs loses per-message settlement — no peek-lock, no dead-letter, no transaction — because a log is not a work queue; and pushing *high-throughput telemetry* through Service Bus burns money on broker features the telemetry never uses and hits throughput walls. The Azure guidance is blunt: Event Hubs for "many producers, multiple consumers, time-ordered events"; Service Bus for "point-to-point or pub/sub with delivery guarantees". The third sibling, Event Grid, is push-based routing for discrete resource events — not either of the two. The partitioning model itself is [[What is the partitioned consumer pattern]] generalized, and the streaming side is the same concept behind [[How do you design a Kafka order event pipeline]].

> [!tip] Interview answer
> **Event Hubs is Azure's streaming ingestion: a partitioned, append-only log with time-based retention, consumer groups reading by offset, and a Kafka-compatible endpoint — built for telemetry and event pipelines at millions of events per second. Service Bus is a broker for commands: queues with competing consumers and peek-locks, topics with filtered subscriptions, transactions, FIFO sessions, and dead-lettering, delivered pull-style until each message is settled. Streams are replayed; queue messages are consumed away — picking the wrong one is the classic architecture error.**
