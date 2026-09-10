<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What are Kafka commitSync and commitAsync for?

> [!abstract] Short answer
> They are the manual offset-commit APIs for consumers with `enable.auto.commit=false`, giving you control over when the group position advances. `commitSync` blocks and retries internally until the commit succeeds or fails irrecoverably; `commitAsync` returns immediately, does not retry, and reports the outcome in a callback. The usual shape: async commits inside the poll loop for latency, a final sync commit on close or rebalance.

Committing an offset means storing `offset + 1` — the offset of the **next record to process** — under the group id, for each partition. Whoever restarts later resumes from there, which is why the commit timing defines at-least-once versus at-most-once behavior — the failure modes of leaving it to the timer are in [[Why is Kafka enable.auto.commit dangerous]]. `commitSync` throws `CommitFailedException` when the member is no longer valid, typically because a rebalance moved the partitions elsewhere ([[What triggers a Kafka consumer group rebalance]]); `commitAsync` cannot retry safely — a slow retry could overwrite a newer commit from another member — so failures surface in the callback and the next commit supersedes them.

## Both APIs in one loop

```java
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.OffsetAndMetadata;
import org.apache.kafka.clients.consumer.OffsetCommitCallback;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.CountDownLatch;

/** Manual offset commit: commitAsync during processing, commitSync on shutdown. */
public class ManualCommitDemo {
    public static void main(String[] args) throws Exception {
        Properties c = new Properties();
        c.setProperty("bootstrap.servers", "localhost:9092");
        c.setProperty("group.id", "manual-g");
        c.setProperty("key.deserializer", StringDeserializer.class.getName());
        c.setProperty("value.deserializer", StringDeserializer.class.getName());
        c.setProperty("enable.auto.commit", "false");
        c.setProperty("auto.offset.reset", "earliest");
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(c)) {
            consumer.subscribe(List.of("commit-demo"));
            var deadline = System.currentTimeMillis() + 30000;
            int got = 0;
            while (got == 0 && System.currentTimeMillis() < deadline) {
                for (ConsumerRecord<String, String> r : consumer.poll(Duration.ofMillis(500))) {
                    got++;
                }
            }
            TopicPartition tp = new TopicPartition("commit-demo", 0);
            long next = consumer.position(tp, Duration.ofSeconds(5));
            System.out.println("poll returned " + got + " records, position=" + next);

            CountDownLatch done = new CountDownLatch(1);
            consumer.commitAsync(new OffsetCommitCallback() {
                public void onComplete(Map<TopicPartition, OffsetAndMetadata> offsets, Exception e) {
                    System.out.println("async commit callback: " + (e == null ? "ok at offset " + offsets.get(tp).offset() : e));
                    done.countDown();
                }
            });
            var cbDeadline = System.currentTimeMillis() + 15000;
            while (!done.await(100, java.util.concurrent.TimeUnit.MILLISECONDS)
                    && System.currentTimeMillis() < cbDeadline) {
                consumer.poll(Duration.ofMillis(100));
            }
            consumer.commitSync(Map.of(tp, new OffsetAndMetadata(next)));
            System.out.println("sync commit ok at offset " + next);
        }
    }
}
```

**Listing 1.** Run against kafka-clients 4.3.1 on a 6-record partition (callbacks are delivered during poll, so the loop keeps polling while the latch waits):

```console
poll returned 6 records, position=6
async commit callback: ok at offset 6
sync commit ok at offset 6
```

**Listing 2.** The async commit reported success through its callback, and the synchronous one confirmed the same position — the shutdown commit is the safety net that pins everything the loop already processed.

```d2
direction: right
loop: "poll loop\ncommitAsync (no retry)" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
cb: "callback reports result\nnext commit supersedes" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
stop: "close / rebalance\ncommitSync (retries)" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
fail: "partitions reassigned\nCommitFailedException" {
  width: 270
  height: 80
  style.fill: "#ffebee"
}
loop -> cb
stop -> fail: member lost partitions
```

**Fig. 1.** Async commits keep the loop fast and tolerate gaps; the sync commit at shutdown is the durable anchor, and it is the point where a lost assignment turns into a `CommitFailedException`.

Per-partition overloads let you commit only the partitions whose records are fully processed, and `consumer.committed(Set.of(tp))` reads back what the group actually has stored — the value [[What is Kafka Consumer position for]] contrasts with the in-memory position.

> [!warning] Async commit gaps are normal, sync commit failure is not
> A failed `commitAsync` is usually harmless — a later commit for newer offsets makes it irrelevant — but an application that treats the callback as confirmation for side effects has it backwards. And a `CommitFailedException` from `commitSync` means your generation ended: the partitions belong to another member, your in-flight results for them may race with its processing, and the only correct response is to finish locally, rejoin, and reprocess from the newly committed offsets.

> [!tip] Interview answer
> These two APIs exist because auto-commit has no idea when processing is done. commitSync blocks and retries — use it on close, on rebalance, anywhere correctness beats latency. commitAsync returns immediately and never retries so a late retry can't overwrite a newer offset — use it inside the loop, treat its callback as telemetry, and pin the final position with a sync commit. Committing means storing offset plus one, the next record to process.

