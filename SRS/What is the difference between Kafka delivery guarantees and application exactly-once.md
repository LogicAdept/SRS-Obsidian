<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #API/Idempotency #SRS

# What is the difference between Kafka delivery guarantees and application exactly-once?

> [!abstract] Short answer
> Kafka's guarantees are about the **log**: at-least-once by default, and exactly-once for read-process-write flows that stay inside Kafka (transactions plus `read_committed`). **Application exactly-once** is about the **side effects** of your handler — database rows, API calls, emails. A broker cannot see those, so duplicate record delivery can still duplicate application work unless the effect itself is idempotent.

The two notions fail in different places. Kafka's delivery layer fails on retries: a producer that retries after a timeout can duplicate records (fixed by idempotence), and a consumer group that reassigns partitions after a crash reprocesses from the last committed offset (fixed only by committing inside a transaction). Application exactly-once fails even when delivery is perfect: the record arrives once, but the handler crashes after writing to the database and before committing the offset — so the next consumer writes the same business effect again. Both halves trace back to the semantics defined in [[What are at-most-once at-least-once and exactly-once semantics in Kafka]], and duplicate suppression of any kind is the general problem behind [[How do you prevent duplicate message or packet delivery]].

## Same records delivered twice, same end state

```java
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

/** Application-level idempotency: replaying the same records leaves the sink state unchanged. */
public class AppEosDemo {
    public static void main(String[] args) {
        Properties c = new Properties();
        c.setProperty("bootstrap.servers", "localhost:9092");
        c.setProperty("group.id", "appeos-g");
        c.setProperty("key.deserializer", StringDeserializer.class.getName());
        c.setProperty("value.deserializer", StringDeserializer.class.getName());
        c.setProperty("enable.auto.commit", "false");
        c.setProperty("auto.offset.reset", "earliest");
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(c)) {
            consumer.subscribe(List.of("app-eos"));
            Map<String, Integer> state = new LinkedHashMap<>();
            var deadline = System.currentTimeMillis() + 30000;
            int got = 0;
            while (got < 3 && System.currentTimeMillis() < deadline) {
                for (ConsumerRecord<String, String> r : consumer.poll(Duration.ofMillis(500))) {
                    apply(state, r.value());
                    got++;
                }
            }
            System.out.println("after first pass: " + state);
            TopicPartition tp = new TopicPartition("app-eos", 0);
            consumer.seek(tp, 0);
            var dl2 = System.currentTimeMillis() + 30000;
            int back = 0;
            while (back < 3 && System.currentTimeMillis() < dl2) {
                for (ConsumerRecord<String, String> r : consumer.poll(Duration.ofMillis(500))) {
                    apply(state, r.value());
                    back++;
                }
            }
            System.out.println("after replay (3 records applied twice): " + state);
        }
    }

    static void apply(Map<String, Integer> state, String record) {
        String[] parts = record.split("=");
        state.put(parts[0], Integer.parseInt(parts[1]));
    }
}
```

**Listing 1.** A sink keyed by event id, run against kafka-clients 4.3.1 with every record deliberately applied twice:

```console
after first pass: {e1=100, e2=50}
after replay (3 records applied twice): {e1=100, e2=50}
```

**Listing 2.** Re-delivery changes nothing: the upsert by event id makes the effect idempotent, which is exactly the property a non-idempotent handler (a counter, an append, a charge) lacks.

```d2
direction: right
k: "Kafka delivery layer\nretries, dedup in log" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
app: "Application handler\ndatabase rows, API calls" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
inside: "exactly-once in Kafka\ncovers this arrow only" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
outside: "application idempotency\nmust cover this" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
k -> app: records
k -> inside
app -> outside
```

**Fig. 1.** Transactions and `read_committed` make the record flow inside Kafka exactly-once; the last hop into external state is the application's responsibility.

> [!warning] Auto-commit plus an external sink duplicates business effects
> With `enable.auto.commit=true` the position can be committed while processing is still in flight, and a crash then repeats the effect after restart; committing after processing has the same exposure on the failure side. The cure lives in the handler — upsert by a natural key, keep processed event ids, or write offsets with the output — not in a producer setting. See [[Why is Kafka enable.auto.commit dangerous]].

> [!tip] Interview answer
> Kafka's delivery guarantees describe the log: at-least-once by default, exactly-once for flows that read, process, and write inside Kafka using transactions and read-committed consumers. Application exactly-once is about side effects outside the log, and no client setting provides it — the handler must be idempotent, for example upserting by event id, so a re-delivered record lands as a no-op instead of a duplicate effect.

