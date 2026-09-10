<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# Why do Kafka producer keys matter?

> [!abstract] Short answer
> The key decides the **partition**: by default the producer hashes it (murmur2) onto the partition count, so every record about one entity — user, order, device — lands on the same partition. That is what buys per-key ordering, per-entity locality for consumers, and a single latest value per key for log compaction ([[What is Kafka log compaction]]). A null key means no such guarantee: records go to a sticky partition chosen for batching.

## How the default partitioner uses the key

Kafka 4.x default logic, in order: if the record names a partition, use it; if a key is present, `murmur2(key) % numPartitions`; if neither, pick a sticky partition until at least `batch.size` bytes have been produced to it, then switch — good throughput for keyless streams, but no per-entity grouping. Override the behavior by implementing the partitioner interface, as [[What is the Kafka Partitioner interface for]] describes.

Verified against a local Kafka 4.3.1 broker with the default configuration — the full program that ran:

```java
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;
import java.util.concurrent.TimeUnit;

public class KeyPartitionDemo {
    public static void main(String[] args) throws Exception {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
            String[] keys = {"alice", "bob", "alice", "carol", "alice"};
            for (String key : keys) {
                ProducerRecord<String, String> rec =
                        new ProducerRecord<>("keys-demo", key, "event-by-" + key);
                RecordMetadata meta = producer.send(rec).get(10, TimeUnit.SECONDS);
                System.out.printf("key=%-6s -> partition=%d offset=%d%n",
                        key, meta.partition(), meta.offset());
            }
        }
    }
}
```

**Listing 1.** Three sends keyed alice, plus bob and carol; `RecordMetadata` reports where each landed.

```console
key=alice  -> partition=4 offset=0
key=bob    -> partition=3 offset=0
key=alice  -> partition=4 offset=1
key=carol  -> partition=2 offset=0
key=alice  -> partition=4 offset=2
```

**Listing 2.** Alice always maps to partition 4 with sequential offsets — the same key hashes to the same partition regardless of when it is sent.

## Keys shape storage and joins

Compaction needs keys to keep one latest value per entity, and keyed state processing needs related records colocated: two topics joined by the same key must be partitioned identically (co-partitioning), or the join cannot happen locally. Choosing the key is therefore a data-modeling decision, not a detail — it fixes which parallelism slice each entity belongs to.

> [!warning] A bad key is a hot partition generator
> Monotonic ids, timestamps, or a handful of tenants as keys skew the hash distribution: one partition takes most traffic while others idle — the classic [[What is a hot partition in Kafka]]. Keys should have high, even cardinality; if the natural key is skewed, pad or bucket it (accepting that per-entity order then needs a different mechanism).

> [!tip] Interview answer
> The key selects the partition through murmur2 hash mod partition count, so one entity's records always share a partition: that gives per-key ordering, per-key compaction state, and locality for consumers and joins. Null keys use sticky partitioning for batch efficiency and have no per-key guarantees. Key cardinality and skew decide whether partitions load-balance or go hot.

