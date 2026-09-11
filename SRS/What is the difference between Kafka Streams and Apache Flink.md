<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Messaging/Tools/Flink #SRS

# What is the difference between Kafka Streams and Apache Flink?

> [!abstract] Short answer
> Scope and shape. Kafka Streams is an embedded Java library: your process, Kafka-only sources and sinks, state in local stores backed by changelog topics, scaling tied to input partitions. Flink is a standalone distributed engine: its own cluster runtime, any-to-any connectors, event-time processing with watermarks, and checkpointed state across a managed cluster — plus batch, Table API/SQL, and CEP on top ([[What is the Kafka Streams API for]]).

## Where the code runs and who owns the cluster

```d2
direction: right
ks: "Kafka Streams\nlibrary inside your app\nKafka in, Kafka out" {
  width: 290
  height: 110
  style.fill: "#e8f5e9"
}
fl: "Apache Flink\nown cluster runtime\njob manager + task managers" {
  width: 290
  height: 110
  style.fill: "#e3f2fd"
}
sources: "Sources/sinks\nKafka only (Streams)\nany system (Flink)" {
  width: 250
  height: 110
  style.fill: "#fff3e0"
}
ks -> sources
fl -> sources
```

**Fig. 1.** Deployment is the first fork: Streams ships as a dependency and borrows Kafka's scaling model; Flink is infrastructure you run, with its own resource management and a source/sink ecosystem.

Kafka Streams deliberately reuses Kafka: input and output are topics, parallelism is the input partition count, fault tolerance rides on changelog topics and consumer groups, and exactly-once processing commits through Kafka transactions (`exactly_once_v2`). You deploy it as part of your application — no separate cluster to run, which is its core selling point and its boundary: connecting to non-Kafka systems means writing that integration yourself. Flink runs jobs on its own distributed runtime: a job manager orchestrates task managers, operators run in parallel instances connected by network shuffles, and state is checkpointed to distributed storage on a timer, enabling exactly-once against arbitrary sources and sinks via two-phase commit. Flink's event-time machinery is deeper by design — watermarks push time forward and drive event-time windows and timers across partitions — and its surface is wider: Table API/SQL, CEP pattern matching, and batch execution of the same program shape ([[What is Kafka Streams DSL for]]).

## Choosing between them

Streams fits teams already standardized on Kafka who want stateful processing close to their services: no new infrastructure, operational model equal to "one more consumer group," DSL over KStream/KTable. Flink fits pipelines that outgrow that frame: many sources and sinks beyond Kafka, large state managed by the engine, complex event-time orchestration, SQL on streams, or a dedicated streaming platform team owning a cluster. Both deliver exactly-once semantics — the difference is what the guarantee is anchored to: Kafka transactions versus Flink checkpoints plus transactional sinks ([[How do you achieve exactly-once processing in Kafka]], [[What are at-most-once at-least-once and exactly-once semantics in Kafka]]).

> [!warning] "Streams is Flink for Kafka" undersells Flink and oversells Streams
> Streams has no engine to size, no watermarks-as-first-class, no SQL layer, and no network shuffles beyond Kafka's repartition topics — which is exactly why it is simple to run and why complex topologies hit its walls. Migrating a nontrivial Streams job to Flink later is a rewrite of the timing model, not a port.

> [!tip] Interview answer
> Kafka Streams is a library inside your JVM app: Kafka topics in and out, state in local stores restored from changelogs, scaling by input partitions, exactly-once via Kafka transactions. Flink is a standalone cluster engine: parallel operators with network shuffles, checkpointed state to storage, watermarks for event time, SQL and CEP, connectors to anything. Streams when Kafka is your platform; Flink when processing is its own platform.

