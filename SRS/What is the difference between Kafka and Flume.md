<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Messaging/Tools/Flume #SRS

# What is the difference between Kafka and Flume?

> [!abstract] Short answer
> Flume is an ingestion pipeline, Kafka is a durable log. Flume agents move events from sources through channels to sinks — a hop-by-hop pipe tuned for collecting log data into stores like HDFS — while Kafka is the distributed, replicated, replayable broker that many independent readers consume from. They also integrate: Flume has Kafka sources, sinks, and channels ([[What are the main components of Apache Kafka]]).

## Pipeline versus platform

```d2
direction: right
src: "Web servers\nlog files" {
  width: 190
  height: 90
  style.fill: "#e3f2fd"
}
agent: "Flume agent\nsource -> channel -> sink" {
  width: 280
  height: 110
  style.fill: "#fff3e0"
}
hdfs: "HDFS / store sink" {
  width: 200
  height: 90
  style.fill: "#e8f5e9"
}
kafka: "Kafka\nreplicated partitioned log,\nmany consumer groups" {
  width: 300
  height: 110
  style.fill: "#e8f5e9"
}
apps: "Many independent\nconsumers" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
src -> agent -> hdfs
src -> kafka -> apps
```

**Fig. 1.** A Flume flow is a fixed pipeline between named endpoints; a Kafka topic is a shared buffer whose consumers come and go independently.

Flume's unit is the agent: a JVM process hosting a source (Avro, Thrift, exec, syslog, and more), a channel (a passive store — file-backed or memory), and a sink (HDFS, another agent, and so on). Events flow hop by hop, transactions guaranteeing delivery from source to channel to sink within each agent; the model is a directed delivery graph you wire per deployment. Kafka's unit is the topic: producers append to partitioned, replicated logs, and any number of consumer groups read at their own pace, replay, and keep offsets — the log outlives any single pipeline and decouples producers from every consumer's lifecycle ([[How does Kafka process messages]]). Flume channels buffer in flight; Kafka retains after delivery — that difference is the replay capability, and it is why Kafka anchors stream platforms while Flume anchors collection tiers ([[What is the difference between Kafka and RabbitMQ]]).

## Where each one earns its keep

Flume fits bulk log and event collection with simple fan-in: thousands of agents shipping to central stores, file channels absorbing bursts, sinks batching into HDFS-compatible stores — a warehouse feed, not a messaging substrate. Kafka fits anything with more than one consumer, ordering needs, or stream processing downstream: per-partition ordering by key, consumer groups for parallel reading, Connect and Streams ecosystems on top, and replication for durability across brokers ([[How does Kafka achieve horizontal scalability]], [[What is Kafka MirrorMaker for]]). The overlap is real but narrow: using Kafka as a Flume channel (the documented Kafka Channel) makes Flume agents restart-safe and decouples hops; the reverse — rebuilding Kafka's multi-subscriber replay out of Flume pipelines — is where teams stop and adopt a log.

> [!warning] Flume is not a multi-consumer broker
> An event delivered into a sink is delivered; the pipeline has no notion of a second independent reader starting from the beginning next week. Teams that wire Flume as their "message bus" discover that adding a consumer means adding a pipeline, not a group id — the bus-shaped requirement is the moment Kafka enters the picture.

> [!tip] Interview answer
> Flume is an ingestion pipeline: agents with source, channel, sink move log events hop by hop into stores like HDFS, with per-hop transactional delivery. Kafka is a replicated, partitioned log with independent consumer groups, offsets, replay, and per-partition ordering — a platform, not a pipe. They integrate through Flume's Kafka source/sink/channel; modern stacks keep Kafka as the buffer and use dedicated collectors for the edge.

