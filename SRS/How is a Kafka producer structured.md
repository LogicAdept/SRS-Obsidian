<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How is a Kafka producer structured?

> [!abstract] Short answer
> A `KafkaProducer` is a pool of buffer space holding records not yet transmitted, plus a background I/O thread that turns those records into requests. The calling threads run interceptors, serializers, and the partitioner, then append into per-partition batches; the Sender thread owns all networking. The object is thread-safe, so one shared instance is the intended usage.

## Components between send() and the socket

- **Serializers** — user-supplied `key.serializer` / `value.serializer`; they run on the caller's thread and must match the record's generic types.
- **Partitioner** — computes the target partition when the record does not name one; also on the caller's thread.
- **Record accumulator** — per-partition batches allocated from `buffer.memory` (32 MiB default) in `batch.size` chunks (16 KiB default); `linger.ms` (5 ms default in Kafka 4.0) bounds how long a partial batch waits for company.
- **Sender thread** — a single background runnable that drains ready batches into produce requests; the accumulator is the meeting point between many producing threads and this one I/O thread.
- **Network client** — owns connections and metadata; at most `max.in.flight.requests.per.connection` (5 default) unacknowledged requests per broker connection, and `acks` decides when a request counts as complete ([[What is the difference between Kafka acks 0 1 and all]]); metadata refreshes on demand and at least every `metadata.max.age.ms` (5 minutes default).

```java
Properties props = new Properties();
props.put("bootstrap.servers", "broker1:9092,broker2:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("linger.ms", "20");            // trade up to 20 ms of latency for bigger batches
props.put("batch.size", "65536");        // per-partition batch target: 64 KiB
props.put("buffer.memory", "67108864");  // total buffering: 64 MiB
props.put("compression.type", "lz4");    // compression applies to whole batches
props.put("enable.idempotence", "true"); // default true since Kafka 3.0 (acks=all, retries=MAX)

Producer<String, String> producer = new KafkaProducer<>(props);
```

**Listing 1.** The structure is visible in the config: serializer and partitioning settings affect the inline path, while `linger.ms`, `batch.size`, and `buffer.memory` tune the accumulator the Sender drains.

## Threading model

`KafkaProducer` is documented thread-safe, and sharing one instance across threads is faster than using several, because all of them feed the same accumulator and the same connection pool. Several producer instances in one process fragment batching and connections instead of adding throughput. From the application's point of view the split is invisible: `send()` and `flush()` are the only entry points an app touches, while serialization, batching, and I/O happen where the structure puts them — the caller's thread and the Sender thread respectively ([[How does a Kafka producer send a record internally]] walks one send through the pipeline). `close()` makes pending buffered records available for sending, waits for them, and releases the buffer pool and the I/O thread — the documentation explicitly warns that failing to close leaks these resources.

The two halves are deliberately asymmetric: serialization and partitioning are cheap CPU work that scales with producing threads, while connections, request scheduling, and retry bookkeeping benefit from being centralized. That asymmetry is why one producer with one I/O thread outperforms several producers each with their own.

> [!warning] A producer per request defeats the whole design
> Creating a `KafkaProducer` per request or per message pays metadata discovery, connection setup, and buffer allocation every time, and the accumulator never fills — so no batching materializes. The structure only pays off behind one long-lived shared producer; keeping producers around and closing them once is part of the contract, not a detail.

> [!tip] Interview answer
> Producer = caller-side pipeline (interceptors, serializers, partitioner) writing into a shared per-partition record accumulator, plus a single background Sender thread whose network client drains batches straight to partition leaders. It is thread-safe by design — share one instance, size `buffer.memory` and `batch.size` for the batch efficiency you want, and always close it.
