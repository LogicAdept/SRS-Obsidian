<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Databases/OLAP/ClickHouse #SRS

# How do you ingest Kafka into ClickHouse?

> [!abstract] Short answer
> ClickHouse ships its own Kafka integration: a table with `Engine = Kafka` subscribes as a consumer group to your topics, reads batches, and a trigger-based materialized view inserts them into a MergeTree table. Alternatives for other shapes: the ClickHouse Kafka Connect sink, or ClickPipes for managed ingestion — but the engine-plus-view path is the native, self-hosted default ([[What are the main components of Apache Kafka]]).

## The two-table shape

```d2
direction: right
kafka: "Kafka topic" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
engine: "Kafka engine table\nconsumer group, no storage" {
  width: 260
  height: 100
  style.fill: "#fff3e0"
}
mv: "Materialized view\nselect + transform" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
mt: "MergeTree target\ncolumnar storage" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
kafka -> engine -> mv -> mt
```

**Fig. 1.** The engine table stores nothing: it is a consumer handle. The materialized view is what copies each consumed block into the real table, applying casts and transformations on the way.

You create a stub table with `Engine = Kafka` and settings — `kafka_broker_list`, `kafka_topic_list` (several topics allowed on one engine), `kafka_group_name` for the consumer group, and `kafka_format` such as `JSONEachRow` or `Avro` — plus tuning like `kafka_num_consumers` and `kafka_thread_per_consumer` for parallel flushing. Then a materialized view over that table, with a `TO` clause naming the target MergeTree, starts consuming at creation and keeps running: each block the engine reads triggers the view's SELECT, which can cast and rename columns before the insert. Message metadata survives via virtual columns — `_topic`, `_partition`, and friends — which you can materialize into real columns for provenance and offset tracking ([[What is Kafka Consumer position for]]).

## What to watch in production

Delivery is at-least-once: if ClickHouse reads a block and the offset commit is lost — a connection drop, a restart — the block is re-read and re-inserted; deduplication with `ReplicatedMergeTree` reduces duplicates but relies on identical blocks, which a Kafka rebalance can invalidate. Consumption parallelism needs care: more consumers only pay off with `kafka_thread_per_consumer` enabled, and many engine tables each create librdkafka threads, so spreading load across the cluster or reading several topics from one engine beats spawning dozens of tiny consumers ([[How does Kafka achieve horizontal scalability]]). Schema evolution rides on the format layer: a new field in JSONEachRow is tolerated, a type change is not — clicks of breakage show up as consumption errors, and the recovery idiom is dropping and recreating the engine table so the view re-attaches ([[How does Kafka version messages]]).

> [!warning] The engine table is not a log you can query
> Selecting from a Kafka engine table directly is not the ingestion model — data flows through the materialized view, and the engine's contents are transient batches, not readable history. Debugging "missing rows" by querying the engine table misleads; the real checkpoints are the consumer group offsets and the target table's counts ([[What is Kafka consumer lag and how do you debug it]]).

> [!tip] Interview answer
> Natively, ClickHouse ingests Kafka with a two-table pattern: a Kafka engine table that acts as a consumer group — brokers, topics, group, format as settings — and a materialized view with a TO clause that transforms and inserts each consumed block into a MergeTree. Delivery is at-least-once, so dedupe with ReplicatedMergeTree, scale via kafka_num_consumers with per-consumer threads, and use virtual columns for topic and partition provenance.

