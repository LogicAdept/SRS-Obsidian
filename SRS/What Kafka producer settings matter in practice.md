<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What Kafka producer settings matter in practice?

> [!abstract] Short answer
> Reliability comes from one group — `enable.idempotence` with its `acks=all`, `retries`, and in-flight constraints, plus `delivery.timeout.ms` as the real budget. Throughput comes from another — `linger.ms`, `batch.size`, `compression.type`. The rest are boundaries: `buffer.memory`, `max.request.size`, `max.block.ms`.

## The two groups and the boundaries

```properties
enable.idempotence=true                # default true since Kafka 3.0; forces acks=all,
                                       # retries=MAX_VALUE, max.in.flight<=5
delivery.timeout.ms=120000             # total send budget, >= request.timeout.ms + linger.ms
request.timeout.ms=30000               # per-request await window
linger.ms=5                            # default 5 since Kafka 4.0 (was 0)
batch.size=16384                       # per-partition batch target, 16 KiB
max.in.flight.requests.per.connection=5   # idempotence ceiling: 5
compression.type=lz4                   # default none; compresses whole batches
buffer.memory=33554432                 # 32 MiB of buffering before send() blocks
max.block.ms=60000                     # send() blocks at most this long, then fails
max.request.size=1048576               # vs broker message.max.bytes=1048588
```

**Listing 1.** Producer settings that decide behavior; comments carry the shipped defaults.

```properties
bootstrap.servers=broker1:9092,broker2:9092  # seeds metadata discovery, not the full cluster list
key.serializer=org.apache.kafka.common.serialization.StringSerializer
value.serializer=org.apache.kafka.common.serialization.StringSerializer
```

**Listing 2.** The mandatory minimum: bootstrap servers only seed metadata discovery, and the serializers must match the `ProducerRecord` generic types.

The idempotence default quietly defines the reliability baseline: since Kafka 3.0 a producer without explicit config already runs `acks=all`, unbounded retries, and broker-side deduplication, so the interview-era advice "set acks and retries by hand" is a leftover — [[What is an idempotent Kafka producer for]]. `delivery.timeout.ms` (2 minutes) caps the whole life of a record: time in the accumulator, await of the ack, and all retry attempts; it must be at least `request.timeout.ms` plus `linger.ms`. The throughput group works as a unit — compression applies to whole batches, so bigger batches via `linger.ms`/`batch.size` compress better too ([[How does a Kafka producer send a record internally]] walks the pipeline). The boundary group prevents surprises under pressure: `buffer.memory` exhaustion blocks `send()` up to `max.block.ms` and then fails the record, and `max.request.size` must agree with the broker's `message.max.bytes` or the topic's `max.message.bytes`.

Sizing the throughput group is a latency budget, not a truth: `linger.ms` is the worst-case extra wait you accept on a quiet partition, `batch.size` is the payload that wait can fill, and both only matter up to the point where the record actually fits — an oversized record skips batching entirely and still must fit under `max.request.size`. Watch the producer's own metrics (`request-latency-avg`, `buffer-available-bytes`) instead of guessing: rising latency with an emptying buffer means batching got better; a draining buffer with rising retry rates means the cluster, not the config, is the bottleneck.

> [!warning] Conflicting configs silently downgrade idempotence
> Setting `acks=1` (or `retries=0`, or in-flight above 5) alongside the defaults does not throw — the producer just disables idempotence and continues with weaker guarantees. Only if you explicitly set `enable.idempotence=true` against a conflicting config does it fail fast with a `ConfigException`. Check what actually survived the config merge before trusting deduplication — [[What is the difference between Kafka acks 0 1 and all]].

> [!tip] Interview answer
> I read producer config as three layers: idempotence and its acks/retries/in-flight constraints for correctness, linger/batch/compression for throughput, and buffer plus size caps as backpressure boundaries. The default profile since Kafka 3.0 is already the strong one — acks all, infinite retries, dedup — so tuning is mostly about latency, throughput, and making sure no conflicting setting silently turned idempotence off.
