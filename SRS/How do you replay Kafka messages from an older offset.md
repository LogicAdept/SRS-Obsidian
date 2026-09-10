<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How do you replay Kafka messages from an older offset?

> [!abstract] Short answer
> Move the read cursor back and poll again: `seek(partition, offset)` for a concrete offset, `offsetForTimes` to translate a timestamp into one, `beginningOffsets`/`endOffsets` for the bounds. To also change where a **restart** resumes from, reset the group's committed offsets — `commitSync` after seeking, or the `kafka-consumer-groups --reset-offsets` tool. `auto.offset.reset` alone does nothing here: it applies only when no valid committed offset exists.

Replay is possible because the log keeps records until retention removes them and offsets are stable addresses. The consumer API route: find the target offset (`beginningOffsets`, `endOffsets`, `offsetForTimes` for time-based rewinds), `seek` the position, and `poll` — the returned records are the old ones again. The group route: reset the **committed** offsets so every future member of the group starts there; the CLI tool does it offline for a stopped group with modes such as `--to-earliest`, `--to-datetime`, `--shift-by`, or `--to-offset`.

## Seek-based replay in code

```java
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.List;
import java.util.Properties;

/** Replay: re-consume the same records after seek back to the first offset. */
public class ReplayDemo {
    public static void main(String[] args) {
        Properties c = new Properties();
        c.setProperty("bootstrap.servers", "localhost:9092");
        c.setProperty("group.id", "replay-g");
        c.setProperty("key.deserializer", StringDeserializer.class.getName());
        c.setProperty("value.deserializer", StringDeserializer.class.getName());
        c.setProperty("enable.auto.commit", "false");
        c.setProperty("auto.offset.reset", "earliest");
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(c)) {
            consumer.subscribe(List.of("replay-topic"));
            TopicPartition tp = new TopicPartition("replay-topic", 0);
            var deadline = System.currentTimeMillis() + 30000;
            int got = 0;
            while (got < 3 && System.currentTimeMillis() < deadline) {
                for (ConsumerRecord<String, String> r : consumer.poll(Duration.ofMillis(500))) {
                    System.out.println("first pass: " + r.value());
                    got++;
                }
            }
            long begin = consumer.beginningOffsets(List.of(tp), Duration.ofSeconds(5)).get(tp);
            long end = consumer.endOffsets(List.of(tp), Duration.ofSeconds(5)).get(tp);
            System.out.println("beginningOffsets=" + begin + " endOffsets=" + end);
            consumer.seek(tp, begin);
            System.out.println("seek back to offset " + begin);
            var dl2 = System.currentTimeMillis() + 30000;
            int back = 0;
            while (back < 3 && System.currentTimeMillis() < dl2) {
                for (ConsumerRecord<String, String> r : consumer.poll(Duration.ofMillis(500))) {
                    System.out.println("replayed: " + r.value());
                    back++;
                }
            }
        }
    }
}
```

**Listing 1.** Run against kafka-clients 4.3.1 on a 3-record partition:

```console
first pass: r0
first pass: r1
first pass: r2
beginningOffsets=0 endOffsets=3
seek back to offset 0
replayed: r0
replayed: r1
replayed: r2
```

**Listing 2.** The same three records came back after `seek`; nothing was rewritten — replay is a cursor move over an unchanged log.

## Resetting the group's committed offsets

```console
kafka-consumer-groups --bootstrap-server localhost:9092 \
  --group replay-g --topic replay-topic --reset-offsets --to-earliest --execute

GROUP           TOPIC           PARTITION  NEW-OFFSET
replay-g        replay-topic    0          0
```

**Listing 3.** The administrative route, executed against the stopped group `replay-g`: the tool rewrites what the group has committed, so every future member resumes from offset 0.

```d2
direction: right
log: "partition log\n0 1 2 3 …" {
  width: 190
  height: 70
  style.fill: "#e3f2fd"
}
seekc: "seek / offsetForTimes\nposition only" {
  width: 250
  height: 70
  style.fill: "#fff3e0"
}
resetc: "reset-offsets / commitSync\ncommitted offsets" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
poll2: "poll returns old records\nagain" {
  width: 250
  height: 70
  style.fill: "#e8f5e9"
}
log -> seekc
log -> resetc
seekc -> poll2
resetc -> poll2: restart
```

**Fig. 1.** Two levers, one log: seek moves the live position of a running consumer; resetting committed offsets changes where any restart resumes.

`offsetForTimes(Map.of(tp, timestamp))` is the timestamp route — it returns the first offset at or after the given time, ideal for "reprocess everything since 14:00". How far back you can go is bounded by retention, not by the API. And because replay re-delivers records an application may have already applied, its safety depends on the sink: see [[What is the difference between Kafka delivery guarantees and application exactly-once]] for why the handler must be idempotent, and [[What is Kafka Consumer position for]] for the cursor this whole mechanism moves.

> [!warning] You cannot reset under an active group
> `--reset-offsets` refuses to run while the group has active members, and a `commitSync` after seek silently races a rebalance that takes the partition away. The other half of the trap is downstream: replay means the same business events arrive twice — counters, appends, and charges run twice unless the sink deduplicates by key or event id.

> [!tip] Interview answer
> Replay is just moving cursors over an immutable log: seek to a computed offset — directly, from beginningOffsets or endOffsets, or via offsetForTimes for a timestamp — and poll again. If the restart point must move too, reset the group's committed offsets with commitSync or the kafka-consumer-groups tool, which only works when the group has no active members. The sink has to tolerate the duplicates this produces.

