<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What does isolation.level read_committed do in Kafka?

> [!abstract] Short answer
> It makes `poll()` return only transactional records whose transaction **committed**, plus all non-transactional records — aborted or still-open transactions are filtered out. The consumer reads up to the **last stable offset (LSO)**: the offset just before the first open transaction, so records behind an in-flight transaction are withheld even if their own transactions committed.

The default, `read_uncommitted`, returns everything in offset order — including records from aborted transactions. `read_committed` instead consumes control records: every transaction ends with a `COMMIT` or `ABORT` marker written to each participant partition, and the consumer uses them to hide aborted data. The LSO is the second half of the contract — a transaction with no marker yet has no verdict, so nothing after its first record is returned until it resolves. That is why `seekToEnd` in `read_committed` returns the LSO, not the high watermark.

## Aborted records: visible to one consumer, hidden from the other

```java
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;

import java.time.Duration;
import java.util.List;
import java.util.Properties;

/** Aborted transaction + plain record; compares read_uncommitted vs read_committed views. */
public class IsolationDemo {
    public static void main(String[] args) throws Exception {
        Properties p = new Properties();
        p.setProperty("bootstrap.servers", "localhost:9092");
        p.setProperty("key.serializer", StringSerializer.class.getName());
        p.setProperty("value.serializer", StringSerializer.class.getName());
        p.setProperty("transactional.id", "iso-demo");

        KafkaProducer<String, String> tx = new KafkaProducer<>(p);
        tx.initTransactions();
        tx.beginTransaction();
        java.util.List<java.util.concurrent.Future<org.apache.kafka.clients.producer.RecordMetadata>> fs = new java.util.ArrayList<>();
        fs.add(tx.send(new ProducerRecord<>("iso-topic", "t", "tx-a1")));
        fs.add(tx.send(new ProducerRecord<>("iso-topic", "t", "tx-a2")));
        fs.add(tx.send(new ProducerRecord<>("iso-topic", "t", "tx-a3")));
        for (java.util.concurrent.Future<org.apache.kafka.clients.producer.RecordMetadata> f : fs) f.get();
        tx.abortTransaction();
        tx.close();
        System.out.println("transaction aborted (3 records invisible to read_committed)");

        Properties plainProps = new Properties();
        plainProps.setProperty("bootstrap.servers", "localhost:9092");
        plainProps.setProperty("key.serializer", StringSerializer.class.getName());
        plainProps.setProperty("value.serializer", StringSerializer.class.getName());
        try (KafkaProducer<String, String> plain = new KafkaProducer<>(plainProps)) {
            plain.send(new ProducerRecord<>("iso-topic", "p", "plain-1")).get();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        System.out.println("non-transactional record plain-1 written");

        view("uncommitted", "iso-u", "read_uncommitted", 4);
        view("committed", "iso-c", "read_committed", 1);
    }

    static void view(String label, String group, String isolation, int expected) {
        Properties c = new Properties();
        c.setProperty("bootstrap.servers", "localhost:9092");
        c.setProperty("group.id", group);
        c.setProperty("key.deserializer", StringDeserializer.class.getName());
        c.setProperty("value.deserializer", StringDeserializer.class.getName());
        c.setProperty("isolation.level", isolation);
        c.setProperty("enable.auto.commit", "false");
        c.setProperty("auto.offset.reset", "earliest");
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(c)) {
            consumer.subscribe(List.of("iso-topic"));
            var deadline = System.currentTimeMillis() + 30000;
            int seen = 0;
            while (seen < expected && System.currentTimeMillis() < deadline) {
                for (ConsumerRecord<String, String> r : consumer.poll(Duration.ofMillis(500))) {
                    System.out.println(label + " consumer sees: " + r.value());
                    seen++;
                }
            }
        }
    }
}
```

**Listing 1.** One aborted transaction, one plain record, two consumers — kafka-clients 4.3.1 against a local 4.3.1 broker:

```console
transaction aborted (3 records invisible to read_committed)
non-transactional record plain-1 written
uncommitted consumer sees: tx-a1
uncommitted consumer sees: tx-a2
uncommitted consumer sees: tx-a3
uncommitted consumer sees: plain-1
committed consumer sees: plain-1
```

**Listing 2.** The log physically contains all four records — `read_committed` filters at read time; nothing is deleted on abort.

```d2
direction: right
a1: "0\ntx-a1\naborted" {
  width: 130
  height: 90
  style.fill: "#ffebee"
}
a2: "1\ntx-a2\naborted" {
  width: 130
  height: 90
  style.fill: "#ffebee"
}
a3: "2\ntx-a3\naborted" {
  width: 130
  height: 90
  style.fill: "#ffebee"
}
mark: "3\nABORT marker" {
  width: 150
  height: 90
  style.fill: "#e3f2fd"
}
p1: "4\nplain-1\nnon-transactional" {
  width: 190
  height: 90
  style.fill: "#e8f5e9"
}
a1 -> a2 -> a3 -> mark -> p1
```

**Fig. 1.** The partition log after the demo: aborted data, the abort control record, then an ordinary record. `read_uncommitted` returns offsets 0–4; `read_committed` skips the aborted range and returns only `plain-1`.

Exactly-once processing depends on this mode: without it, a consumer would re-read output from transactions that were later aborted. The pairing with transactional producers is described in [[What happens during a Kafka consume-transform-produce transaction]], and the LSO sits below the [[What is the Kafka high watermark]], which only tracks replicated — not committed-transaction — progress.

> [!warning] An open transaction freezes read_committed consumers
> The LSO cannot advance past the first open transaction, so one long-running transaction blocks the readable frontier for every `read_committed` consumer of that partition — lag grows even though records keep arriving. The coordinator aborts a transaction once `transaction.timeout.ms` (default 1 minute, capped broker-side by `transaction.max.timeout.ms`) expires, which unsticks the LSO.

> [!tip] Interview answer
> read_committed filters the log view by transaction outcome: only committed transactional records plus non-transactional ones are returned, and polls stop at the last stable offset — the offset before the first still-open transaction. Aborted records stay in the log with an abort marker; they are hidden at read time. The cost is that one open transaction can hold back the readable frontier until it commits, aborts, or times out.

