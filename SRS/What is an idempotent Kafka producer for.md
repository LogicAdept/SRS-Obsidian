<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #API/Idempotency #SRS

# What is an idempotent Kafka producer for?

> [!abstract] Short answer
> It makes producer retries produce no duplicates: the broker assigns the producer a **producer id (PID)**, every batch carries a **per-partition sequence number**, and the broker silently drops a batch it has already stored. Retries stay safe, ordering per partition is preserved with up to 5 in-flight requests, and idempotence is the foundation transactions build on. Enabled by default since Kafka 3.0.

Without idempotence, a producer that times out waiting for an ack cannot tell whether the write landed, so it retries — and a retry after a successful original write appends the same record twice. With `enable.idempotence=true` the broker hands the producer a PID on session start, and the first batch to each partition establishes a sequence; the broker tracks the last 5 sequence numbers per producer id and partition and rejects duplicates and gaps. The requirements follow from that: `acks=all` (otherwise there is nothing to retry against), `retries > 0`, and `max.in.flight.requests.per.connection <= 5` — ordering holds for any value in that range because the broker reorders by sequence, not the client.

## A producer run with idempotence on

```java
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

/** Idempotent producer: sends 5 records, prints partition/offset of each accepted write. */
public class IdempotentProducerDemo {
    public static void main(String[] args) throws Exception {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "true");
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
            for (int i = 0; i < 5; i++) {
                RecordMetadata md = producer.send(
                        new ProducerRecord<>("idem-topic", "key-" + i, "value-" + i)).get();
                System.out.println("accepted: offset=" + md.offset() + " partition=" + md.partition());
            }
        }
    }
}
```

**Listing 1.** Idempotent producer against kafka-clients 4.3.1 on a fresh single-partition topic:

```console
accepted: offset=0 partition=0
accepted: offset=1 partition=0
accepted: offset=2 partition=0
accepted: offset=3 partition=0
accepted: offset=4 partition=0
```

**Listing 2.** The happy path looks ordinary — sequence numbers are contiguous and every write is accepted exactly once. The guarantee shows up on the failure path: when a retried batch was already stored, the broker drops it and the log never sees the copy.

Idempotence operates per partition. It makes no promise across partitions or across topics, so it cannot make "write to two topics atomically" true — that requires transactions. How retries without idempotence reorder a partition log is the failure mode shown in [[Why can Kafka retries break ordering without idempotence]].

> [!warning] The PID dies with the session
> Idempotence deduplicates **within one producer instance**: a restart creates a new producer with a new PID, and the broker happily stores the replayed records of the new writer. If duplicates must be suppressed across restarts or crashes — a "zombie" writing concurrently — use `transactional.id`, whose epoch fencing covers sessions; see [[What is producer fencing in Kafka transactions]]. Explicitly enabling idempotence while setting conflicting values (`acks` not `all`, `max.in.flight` above 5, `retries=0`) throws `ConfigException` at startup.

> [!tip] Interview answer
> The idempotent producer exists so that retries cannot duplicate records: the broker assigns a producer id, batches carry per-partition sequence numbers, and duplicates are dropped at append time. It requires acks=all, retries above zero, and at most five in-flight batches, with ordering intact — and it has been the default since 3.0. Its limits: one session, one partition — cross-restart dedup needs transactional.id, cross-partition atomicity needs transactions.

