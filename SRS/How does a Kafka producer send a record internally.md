<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How does a Kafka producer send a record internally?

> [!abstract] Short answer
> A send is an asynchronous handoff, not a network call: the calling thread serializes the record, picks a partition, and appends the bytes into an in-memory per-partition batch. A single background Sender thread later drains full or expired batches into produce requests sent straight to the partition leader; the `Future` and callback complete once the leader answers per the `acks` contract.

## Serialization and buffering on the calling thread

`send(ProducerRecord)` does its data-plane work before it returns. An optional interceptor chain sees the record first, then the configured `key.serializer` / `value.serializer` turn the objects into bytes, then a partition is chosen — an explicitly set partition wins, otherwise the partitioner computes one ([[What is the Kafka Partitioner interface for]]). The serialized record is appended to the batch kept for that partition. Time spent inside user-supplied serializers or a partitioner is not counted against `max.block.ms`; waiting for metadata or for a free buffer is. When `buffer.memory` (32 MiB by default) is exhausted, `send()` blocks up to `max.block.ms` (60 s) and then completes exceptionally with `BufferExhaustedException`.

```d2
direction: right
send: "send(record)\nuser thread" {
  width: 190
  height: 70
  style.fill: "#e3f2fd"
}
ser: "interceptors,\nserialize key/value" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
part: "pick partition\n(explicit or partitioner)" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
acc: "append to per-partition batch\n(batch.size, linger.ms)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
sender: "Sender thread drains\nready batches" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
leader: "produce request to\npartition leader" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
ack: "acks satisfied ->\nFuture + Callback" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
send -> ser -> part -> acc
acc -> sender -> leader -> ack
```

**Fig. 1.** The user thread runs only the first three stages; everything after the accumulator belongs to the background Sender thread.

## The Sender thread and completion

One background I/O thread turns buffered records into requests. A batch leaves when it reaches `batch.size` (16 KiB by default) or when `linger.ms` expires — 5 ms by default since Kafka 4.0, previously 0. Under heavy load batching happens regardless of linger, because records arrive faster than they drain. One produce request can carry batches for several partitions, and it goes directly to the broker leading the target partition — there is no routing tier. Whole batches can be compressed (`compression.type`, `none` by default; larger batches compress better). The leader appends, replication proceeds per [[What is the difference between Kafka acks 0 1 and all]], and the future resolves with `RecordMetadata` — topic, partition, offset ([[How is a Kafka producer structured]] names the components; [[What is the Kafka Producer API for]] shows the surface).

Failures are retried automatically — `retries` defaults to `Integer.MAX_VALUE`, so `delivery.timeout.ms` (2 minutes by default) is the real budget; it must be at least `request.timeout.ms` plus `linger.ms`. With idempotence enabled, broker-side deduplication makes those retries invisible in the log. Without it, retries combined with more than one in-flight request can reorder batches — [[Why can Kafka retries break ordering without idempotence]].

> [!warning] Buffer pressure shows up as producer-thread latency, not broker errors
> Once `buffer.memory` is full, `send()` stops being cheap: the calling thread blocks up to `max.block.ms` and then gets a failed future. Applications treating send as fire-and-forget see this as latency spikes and `BufferExhaustedException` in the producing threads — the signal that the producer or the cluster cannot keep up.

> [!tip] Interview answer
> The work is split by thread: the caller serializes, partitions, and appends the record into a per-partition accumulator; one background Sender thread batches and ships requests directly to partition leaders. A batch leaves on `batch.size` or `linger.ms`, completion is a Future plus callback once the `acks` contract is met, `buffer.memory` bounds the memory, and `delivery.timeout.ms` bounds retries.
