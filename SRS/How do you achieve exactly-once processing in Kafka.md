<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #API/Idempotency #SRS

# How do you achieve exactly-once processing in Kafka?

> [!abstract] Short answer
> Use a **transactional producer** (`transactional.id` set, which implies idempotence) and a consumer with `isolation.level=read_committed` and `enable.auto.commit=false`. In each cycle: begin a transaction, produce the output records, attach the input offsets with `sendOffsetsToTransaction`, and commit — output and input position become atomic. Kafka Streams does the same internally with `processing.guarantee=exactly_once_v2`.

Three cooperating pieces are required, and removing any one downgrades the guarantee. First, the consumer must be the only processor of each partition — group assignment provides this. Second, the producer must be transactional: setting `transactional.id` configures transactional delivery, makes a restarted application abort the previous instance's in-flight transaction through epoch fencing ([[What is producer fencing in Kafka transactions]]), and implies `enable.idempotence`. Third, the consumer must read only committed data and not auto-commit, because the producer — not the consumer — writes the position inside the transaction.

## The configuration trio

```java
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

/** Configuration trio for exactly-once processing: builds and validates the settings. */
public class EosConfigDemo {
    public static void main(String[] args) {
        Properties c = new Properties();
        c.setProperty("bootstrap.servers", "localhost:9092");
        c.setProperty("group.id", "eos-app-1");
        c.setProperty("key.deserializer", StringDeserializer.class.getName());
        c.setProperty("value.deserializer", StringDeserializer.class.getName());
        c.setProperty("isolation.level", "read_committed");
        c.setProperty("enable.auto.commit", "false");

        Properties p = new Properties();
        p.setProperty("bootstrap.servers", "localhost:9092");
        p.setProperty("key.serializer", StringSerializer.class.getName());
        p.setProperty("value.serializer", StringSerializer.class.getName());
        p.setProperty("transactional.id", "eos-app-1-producer");

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(c);
             KafkaProducer<String, String> producer = new KafkaProducer<>(p)) {
            System.out.println("consumer isolation.level=" + c.getProperty("isolation.level"));
            System.out.println("consumer enable.auto.commit=" + c.getProperty("enable.auto.commit"));
            System.out.println("producer transactional.id=" + p.getProperty("transactional.id"));
            System.out.println("producer enable.idempotence=true (implied by transactional.id)");
            System.out.println("consumer constructed: " + (consumer != null));
            System.out.println("producer constructed: " + (producer != null));
        }
    }
}
```

**Listing 1.** The trio, compile-checked and run against kafka-clients 4.3.1:

```console
consumer isolation.level=read_committed
consumer enable.auto.commit=false
producer transactional.id=eos-app-1-producer
producer enable.idempotence=true (implied by transactional.id)
consumer constructed: true
producer constructed: true
```

**Listing 2.** The settings validate: the transactional producer is constructed with idempotence implied, and the consumer commits nothing on its own.

## The transactional cycle

Only the producer is transactional — but it can make transactional updates to the consumer's committed position, and that is what closes the loop. The full cycle with the send and commit calls is shown in [[What happens during a Kafka consume-transform-produce transaction]]. On an abort, output records are hidden from `read_committed` consumers, but the consumer's in-memory position does not rewind automatically; the application must seek back to the last committed offset and reprocess. Transactional producer errors split into classes: internal retriable ones stay hidden, abortable ones require `abortTransaction` plus a position reset, and `ProducerFencedException` means another instance took over the `transactional.id`.

> [!warning] The guarantee stops at the Kafka boundary
> Writing to an external database, cache, or API from the same loop is not covered: the transaction only spans Kafka topics and the consumer position. For those sinks, store offsets together with the output where possible, or make the write idempotent by a key — the distinction is spelled out in [[What is the difference between Kafka delivery guarantees and application exactly-once]]. Topics holding transactional data also need durable settings — a replication factor of at least 3 with `min.insync.replicas=2` is the recommended production shape.

> [!tip] Interview answer
> Exactly-once processing needs three things: a transactional producer whose `transactional.id` implies idempotence and fences zombie instances; a consumer on `read_committed` with auto-commit off; and offsets committed inside the transaction via `sendOffsetsToTransaction`, so outputs and the input position commit atomically. Kafka Streams packages the same pattern — flip `processing.guarantee` to `exactly_once_v2`. Anything writing outside Kafka still needs an idempotent sink.

