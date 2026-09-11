<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka Producer API for?

> [!abstract] Short answer
> The `org.apache.kafka.clients.producer` package is the write side of Kafka's client surface: build a `ProducerRecord`, hand it to `KafkaProducer.send()` for asynchronous delivery, and get delivery control on the same object — checked futures for simple sends, idempotence by default, and transactions for atomic multi-partition writes.

## Core methods

`send(record)` adds the record to the internal buffer and returns immediately with a `Future<RecordMetadata>`; the future completes with topic, partition, and offset once the leader acknowledges per `acks`. An optional `Callback` runs when the request completes — it generally executes on the background I/O thread, so it should be fast, and on failure its `RecordMetadata` carries -1 in all fields. `flush()` blocks until every previously sent record has been acknowledged, which is how a synchronous send is built. `partitionsFor(topic)` exposes the current partition list from cached metadata. These calls are bounded by `max.block.ms` (60 s) when metadata is unavailable or the buffer is full.

```java
ProducerRecord<String, String> record =
        new ProducerRecord<>("payments", orderId, payload); // topic, key, value

producer.send(record, (meta, exception) -> {
    if (exception != null) {
        log.error("send failed for order {}", orderId, exception);
    } else {
        log.info("order {} -> partition={} offset={}", orderId, meta.partition(), meta.offset());
    }
});
```

**Listing 1.** The callback style is the normal production pattern: send stays asynchronous while failures surface in one place.

The transactional pattern brackets a batch of sends with the four lifecycle methods:

```java
producer.initTransactions(); // once, right after creating the producer

try {
    producer.beginTransaction();
    for (Event e : batch) {
        producer.send(new ProducerRecord<>("output-topic", e.key(), e.value()));
    }
    producer.commitTransaction();
} catch (ProducerFencedException | OutOfOrderSequenceException | AuthorizationException e) {
    producer.close(); // unrecoverable: fenced, sequence gap, or authorization revoked
} catch (KafkaException e) {
    producer.abortTransaction(); // nothing from this batch becomes visible
}
```

**Listing 2.** Conceptual transactional loop: recoverable errors abort the transaction, unrecoverable ones close the producer.

## Delivery control on the same API

Idempotence and transactions are configuration plus a few methods, not a separate client. Set `transactional.id` — idempotence and its dependent configs switch on automatically — then `initTransactions()`, `beginTransaction()`, `send(...)`, and `commitTransaction()` or `abortTransaction()`. These transactional methods are blocking and report failures by throwing; a producer keeps at most one open transaction, and `sendOffsetsToTransaction()` writes consumer offsets into the same transaction, which is exactly what consume-transform-produce loops need ([[What happens during a Kafka consume-transform-produce transaction]]). For transactional topics the documentation recommends `replication.factor` of at least 3 and `min.insync.replicas` of 2. The vocabulary of the resulting guarantees lives in [[What are at-most-once at-least-once and exactly-once semantics in Kafka]] and [[What is the Kafka Transactions API for]]; the internals of the pipeline are in [[How does a Kafka producer send a record internally]].

> [!warning] Ignoring the result loses records silently
> `send()` returning does not mean the record was written. If nobody checks the future or registers a callback, a failed send — buffer exhausted, record expired in the buffer, unrecoverable broker error — disappears without a trace. The transactional producer is the exception: inside a transaction, an irrecoverable send error surfaces as a `KafkaException` from the transactional calls, so abort vs commit is decided with full information.

> [!tip] Interview answer
> The Producer API publishes records asynchronously: `send()` returns a `Future<RecordMetadata>` with an optional fast-running callback, `flush()` converts a stream of sends into a synchronous block, and the transactional methods — init, begin, commit, abort, plus `sendOffsetsToTransaction` — turn the same producer into an all-or-nothing writer. Delivery strength is chosen by config, not by switching APIs.
