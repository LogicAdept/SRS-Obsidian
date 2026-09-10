<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# Why is Kafka enable.auto.commit dangerous?

> [!abstract] Short answer
> Because auto-commit commits the offsets **of the last poll** on a timer (`auto.commit.interval.ms`, default 5 s) — not the offsets of records your handler actually finished processing. The gap between that commit and the completion of processing is a correctness window: a crash there either loses records (commit ahead of work) or repeats them (work ahead of commit), and you do not control which.

The mechanism matters: with `enable.auto.commit=true` the consumer commits in the background during `poll()` calls and on close, and what it commits is the position returned by the most recent poll. Whether that is "safe" depends entirely on where your processing is at the moment the timer fires — something the consumer does not know. A batch that takes longer than the interval to process gets its offsets committed while it is still running.

## The window, made visible

```java
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.List;
import java.util.Properties;
import java.util.Set;

/** Auto-commit window: committed offset advances while "processing" is still pending. */
public class AutoCommitWindowDemo {
    public static void main(String[] args) throws Exception {
        Properties c = new Properties();
        c.setProperty("bootstrap.servers", "localhost:9092");
        c.setProperty("group.id", "autocommit-g");
        c.setProperty("key.deserializer", StringDeserializer.class.getName());
        c.setProperty("value.deserializer", StringDeserializer.class.getName());
        c.setProperty("enable.auto.commit", "true");
        c.setProperty("auto.commit.interval.ms", "1000");
        c.setProperty("auto.offset.reset", "earliest");
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(c)) {
            consumer.subscribe(List.of("pos-topic"));
            TopicPartition tp = new TopicPartition("pos-topic", 0);

            var deadline = System.currentTimeMillis() + 30000;
            int got = 0;
            while (got == 0 && System.currentTimeMillis() < deadline) {
                for (ConsumerRecord<String, String> r : consumer.poll(Duration.ofMillis(500))) {
                    got++;
                }
            }
            System.out.println("poll 1 returned " + got + " records, processing not started");
            var committed = consumer.committed(Set.of(tp), Duration.ofSeconds(5)).get(tp);
            System.out.println("committed while processing pending: " + committed);
            Thread.sleep(1200);
            consumer.poll(Duration.ofMillis(300));
            System.out.println("poll 2 fired, auto-commit interval elapsed");
            var committed2 = consumer.committed(Set.of(tp), Duration.ofSeconds(5)).get(tp);
            System.out.println("committed while processing still pending: " + (committed2 == null ? "null" : committed2.offset()));
        }
    }
}
```

**Listing 1.** Run against kafka-clients 4.3.1 on a fresh group with a 3-record partition (interval shortened to 1 s to make the window observable; the default is 5 s):

```console
poll 1 returned 3 records, processing not started
committed while processing pending: null
poll 2 fired, auto-commit interval elapsed
committed while processing still pending: 3
```

**Listing 2.** No record was processed, yet the committed offset reached 3 — if the process died here, those three records would never be processed, because the replacement consumer resumes from the committed position.

```d2
direction: right
poll1: "poll returns 3 records\nprocessing pending" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
timer: "interval elapses\nauto-commit fires" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
c3: "committed = 3\nwork done = 0" {
  width: 200
  height: 80
  style.fill: "#ffebee"
}
crash: "crash here →\n3 records lost" {
  width: 210
  height: 80
  style.fill: "#ffebee"
}
poll1 -> timer
timer -> c3
c3 -> crash
```

**Fig. 1.** Auto-commit advanced the group position past unprocessed records; the loss window is the span between the timer firing and the handler finishing.

Auto-commit is not broken — it is a deliberate trade for fire-and-forget consumption where an occasional loss or duplicate is acceptable. The moment processing has side effects, you need explicit commits: [[What are Kafka commitSync and commitAsync for]] shows the manual APIs, and transactional processing removes the window entirely by committing the position with the output, as in [[What are at-most-once at-least-once and exactly-once semantics in Kafka]].

> [!warning] The interval is not a safety margin
> Shortening `auto.commit.interval.ms` narrows the window but never closes it, and lengthening it trades duplicates for a bigger loss window. The subtler trap is `max.poll.interval.ms`: slow processing that outlives it gets the consumer kicked from the group, and the subsequent commit fails — the failure surfaces as a `CommitFailedException`, not as a delivery warning.

> [!tip] Interview answer
> Auto-commit fires on the poll loop every auto.commit.interval.ms and commits whatever the last poll returned, regardless of how far processing has gotten. A demo against a real broker shows committed reaching 3 with zero records processed — crash there and those records are lost; process-then-crash gives duplicates instead. It is fine for lossy log tailing; anything with side effects needs manual commits or transactions.

