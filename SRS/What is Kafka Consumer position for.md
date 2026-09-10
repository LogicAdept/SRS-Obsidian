<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is Kafka Consumer position for?

> [!abstract] Short answer
> `position` is the offset of the **next record that `poll` will return** for a partition — the consumer's live, in-memory read cursor. `committed` is the last offset **stored in Kafka** for the group. On restart, the consumer resumes from `committed`, so the distance between the two is exactly the at-least-once/at-most-once window, and `seek` moves the position by hand.

The consumer tracks a position per assigned partition. It advances as records are returned, and it is not guaranteed to be consecutive: on a compacted topic or a transactional topic, offsets can jump. The committed offset is a different animal — it lives in the group's internal topic, survives restarts, and only moves when someone commits (or an administrator resets it). Everything about delivery semantics is the ordering of writes to those two cursors, which is why [[What are Kafka commitSync and commitAsync for]] exists as its own topic.

## The two cursors in one run

```java
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.OffsetAndMetadata;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

/** position() vs committed(): next fetch offset vs last stored offset. */
public class PositionDemo {
    public static void main(String[] args) {
        Properties c = new Properties();
        c.setProperty("bootstrap.servers", "localhost:9092");
        c.setProperty("group.id", "pos-g");
        c.setProperty("key.deserializer", StringDeserializer.class.getName());
        c.setProperty("value.deserializer", StringDeserializer.class.getName());
        c.setProperty("enable.auto.commit", "false");
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
            long pos = consumer.position(tp, Duration.ofSeconds(5));
            var committed = consumer.committed(Set.of(tp), Duration.ofSeconds(5)).get(tp);
            System.out.println("after poll of " + got + " records: position=" + pos);
            System.out.println("committed before any commit: " + committed);
            consumer.commitSync(Map.of(tp, new OffsetAndMetadata(pos)));
            var committed2 = consumer.committed(Set.of(tp), Duration.ofSeconds(5)).get(tp);
            System.out.println("committed after commitSync: " + committed2.offset());
            consumer.seek(tp, 0);
            System.out.println("after seek(tp, 0): position=" + consumer.position(tp, Duration.ofSeconds(5)));
        }
    }
}
```

**Listing 1.** Run against kafka-clients 4.3.1 on a fresh group and a 3-record partition:

```console
after poll of 3 records: position=3
committed before any commit: null
committed after commitSync: 3
after seek(tp, 0): position=0
```

**Listing 2.** The poll moved the position to 3 while the group had nothing stored; one `commitSync` aligned them, and `seek` moved only the position — the next `poll` would replay from offset 0.

```d2
direction: right
pos: "position (in-memory)\nnext offset poll returns" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
com: "committed (in Kafka)\nresumes here after restart" {
  width: 290
  height: 80
  style.fill: "#fff3e0"
}
gap: "gap between them\n= loss or duplicate window" {
  width: 290
  height: 80
  style.fill: "#ffebee"
}
seek: "seek / seekToBeginning\nmoves position only" {
  width: 270
  height: 80
  style.fill: "#e8f5e9"
}
pos -> gap: uncommitted records
com -> gap
seek -> pos
```

**Fig. 1.** Position and committed answer different questions — "what will I read next" versus "what would I read after a crash" — and the gap between them is the delivery-semantics window.

Replaying deliberately means moving the position without waiting for a failure: [[How do you replay Kafka messages from an older offset]] covers seek, timestamp lookup, and resetting the committed offsets of a group. Reading back the stored value is `committed(...)`, and commits land as records in the group's internal topic — [[What is the consumer_offsets topic for]].

> [!warning] position() is not a local variable read
> Calling `position` may block on a coordinator or metadata round trip (hence the timeout overloads), and after a rebalance the position for a partition you no longer own throws. The common misreading is the opposite direction: treating `committed` as "where my loop is" — it only moves when someone commits, and with auto-commit it can be ahead of your handler, as [[Why is Kafka enable.auto.commit dangerous]] demonstrates.

> [!tip] Interview answer
> Position is the consumer's next read offset, kept in memory; committed is what the group has stored in Kafka and what a restart resumes from. They drift apart between commits, and that drift is the loss-or-duplicate window — closing it is what manual commits and transactions are for. seek moves only the position, so replay is just seeking back and polling again.

