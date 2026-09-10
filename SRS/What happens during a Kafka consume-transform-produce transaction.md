<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What happens during a Kafka consume-transform-produce transaction?

> [!abstract] Short answer
> One producer wraps **both** the transformed output records and the **input offsets** of the consumed batch into a single transaction: begin, produce, `sendOffsetsToTransaction`, commit. The transaction coordinator stages the participant partitions, the offsets land in the group's internal topic marked as part of the transaction, and on commit, control records mark every involved partition — so `read_committed` consumers see all of it or none of it.

Kafka transactions differ from classic messaging transactions: the consumer and producer are separate objects, and only the producer is transactional. The trick is that the consumer's position is itself data in a Kafka topic, so the producer can write it atomically with the output. Under the hood the flow is two-phase: the transaction coordinator (a broker module whose state lives in an internal topic) first adds each target partition to the transaction, then on commit writes a `COMMIT` control record to every one of them; a later `read_committed` consumer uses those markers to filter.

## The copier pattern end to end

```java
import org.apache.kafka.clients.consumer.ConsumerGroupMetadata;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;

import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.Properties;

/** Transactional consume-transform-produce: copies sem-src into sem-dst atomically. */
public class TxnCopierDemo {
    public static void main(String[] args) {
        Properties c = new Properties();
        c.setProperty("bootstrap.servers", "localhost:9092");
        c.setProperty("group.id", "copy-g");
        c.setProperty("key.deserializer", StringDeserializer.class.getName());
        c.setProperty("value.deserializer", StringDeserializer.class.getName());
        c.setProperty("enable.auto.commit", "false");
        c.setProperty("isolation.level", "read_committed");
        c.setProperty("auto.offset.reset", "earliest");

        Properties p = new Properties();
        p.setProperty("bootstrap.servers", "localhost:9092");
        p.setProperty("key.serializer", StringSerializer.class.getName());
        p.setProperty("value.serializer", StringSerializer.class.getName());
        p.setProperty("transactional.id", "copy-txn");

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(c);
             KafkaProducer<String, String> producer = new KafkaProducer<>(p)) {
            consumer.subscribe(List.of("sem-src"));
            ConsumerRecords<String, String> batch = null;
            var deadline = System.currentTimeMillis() + 30000;
            while (batch == null || batch.isEmpty()) {
                if (System.currentTimeMillis() > deadline) throw new IllegalStateException("no input");
                batch = consumer.poll(Duration.ofMillis(500));
            }
            producer.initTransactions();
            producer.beginTransaction();
            for (ConsumerRecord<String, String> r : batch) {
                String out = r.key().toUpperCase() + ":" + r.value().toUpperCase();
                producer.send(new ProducerRecord<>("sem-dst", r.key(), out));
                System.out.println("copied: " + r.key() + " -> " + out);
            }
            Map<TopicPartition, org.apache.kafka.clients.consumer.OffsetAndMetadata> offsets =
                    new java.util.HashMap<>();
            for (ConsumerRecord<String, String> r : batch.records("sem-src")) {
                offsets.put(new TopicPartition(r.topic(), r.partition()),
                        new org.apache.kafka.clients.consumer.OffsetAndMetadata(r.offset() + 1));
            }
            ConsumerGroupMetadata gm = consumer.groupMetadata();
            producer.sendOffsetsToTransaction(offsets, gm);
            producer.commitTransaction();
            System.out.println("transaction committed, input offsets advanced to 3");
            System.out.println("group generation used: " + gm.generationId());
        }

        Properties v = new Properties();
        v.setProperty("bootstrap.servers", "localhost:9092");
        v.setProperty("group.id", "verify-g");
        v.setProperty("key.deserializer", StringDeserializer.class.getName());
        v.setProperty("value.deserializer", StringDeserializer.class.getName());
        v.setProperty("isolation.level", "read_committed");
        v.setProperty("auto.offset.reset", "earliest");
        try (KafkaConsumer<String, String> verifier = new KafkaConsumer<>(v)) {
            verifier.subscribe(List.of("sem-dst"));
            var deadline = System.currentTimeMillis() + 30000;
            int seen = 0;
            while (seen < 3 && System.currentTimeMillis() < deadline) {
                for (ConsumerRecord<String, String> r : verifier.poll(Duration.ofMillis(500))) {
                    System.out.println("read_committed verify: " + r.value());
                    seen++;
                }
            }
        }
    }
}
```

**Listing 1.** Consume-transform-produce, run against a local Kafka 4.3.1 broker with kafka-clients 4.3.1:

```console
copied: k1 -> K1:V1
copied: k2 -> K2:V2
copied: k3 -> K3:V3
transaction committed, input offsets advanced to 3
group generation used: 1
read_committed verify: K1:V1
read_committed verify: K2:V2
read_committed verify: K3:V3
```

**Listing 2.** Three records moved and their offsets committed in one transaction; a `read_committed` verifier sees exactly the committed output. Note the offsets are committed as `offset + 1` — the next record to process.

```d2
direction: right
src: "sem-src\ninput records" {
  width: 170
  height: 70
  style.fill: "#e3f2fd"
}
txn: "Transaction\ncopy-txn" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
dst: "sem-dst\noutput records" {
  width: 170
  height: 70
  style.fill: "#fff3e0"
}
offs: "committed offsets\noffset + 1" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
commit: "COMMIT markers\non both partitions" {
  width: 230
  height: 70
  style.fill: "#e8f5e9"
}
src -> txn: consume
txn -> dst
txn -> offs: sendOffsetsToTransaction
dst -> commit
offs -> commit
```

**Fig. 1.** Output records and the input position enter the same transaction; the commit writes control records to each participant partition, making the pair atomic for `read_committed` consumers.

The group metadata passed to `sendOffsetsToTransaction` ties the commit to the consumer's current generation, so a rebalance concurrent with the transaction fails the commit instead of double-processing. The offsets being committed are ordinary group offsets stored in the group's own topic — [[What is the consumer_offsets topic for]] — held by the [[What is a Kafka consumer group coordinator for]]. This is the mechanism [[How do you achieve exactly-once processing in Kafka]] assembles into a full recipe.

> [!warning] An abort does not rewind the consumer
> After `abortTransaction`, the aborted output is invisible, but the consumer's in-memory position stays where the failed batch ended — the application must seek back to the last committed offset itself, or the reprocessing loop silently skips the failed records. And a transaction left open stalls `read_committed` consumers at the last stable offset until it is committed, aborted, or expired via `transaction.timeout.ms`.

> [!tip] Interview answer
> In a consume-transform-produce transaction the producer is the only transactional actor, and it commits two things together: the output records and the consumer's input offsets, handed over with sendOffsetsToTransaction together with the group generation. The coordinator writes commit or abort markers to every partition involved, so read_committed consumers see all of it or none — and on abort the application must rewind the consumer position explicitly.

