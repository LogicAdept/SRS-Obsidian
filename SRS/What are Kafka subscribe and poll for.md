<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Messaging/PollingConsumer #SRS

# What are Kafka subscribe and poll for?

> [!abstract] Short answer
> `subscribe(topics)` enrolls the consumer in a **group** with dynamic partition assignment; `poll()` is the single entry point that drives everything — joining, heartbeats, rebalance participation, fetching — and returns a **batch** of records from the assigned partitions. You never call "receive": you loop on poll, and the group protocol moves partitions between members around you.

`subscribe` is the group-based alternative to `assign`: it hands partition placement to the group coordinator so consumers can join and leave freely. `poll` then does far more than fetch — the consumer joins the group when `poll` is invoked, stays in it as long as polling continues, and rejoins on topic metadata changes. The liveness contract is explicit: keep calling `poll`, keep your partitions. Records come back batched per partition in offset order, which is why a single poll typically returns many records at once.

## The loop, measured

```java
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.List;
import java.util.Properties;

/** subscribe + poll: dynamic group join, assignment, batched fetch. */
public class SubscribePollDemo {
    public static void main(String[] args) {
        Properties c = new Properties();
        c.setProperty("bootstrap.servers", "localhost:9092");
        c.setProperty("group.id", "poll-g");
        c.setProperty("key.deserializer", StringDeserializer.class.getName());
        c.setProperty("value.deserializer", StringDeserializer.class.getName());
        c.setProperty("enable.auto.commit", "false");
        c.setProperty("auto.offset.reset", "earliest");
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(c)) {
            consumer.subscribe(List.of("poll-topic"));
            var deadline = System.currentTimeMillis() + 30000;
            int total = 0;
            int pollN = 0;
            boolean printedAssignment = false;
            while (total < 6 && System.currentTimeMillis() < deadline) {
                pollN++;
                var batch = consumer.poll(Duration.ofMillis(500));
                if (!printedAssignment && !consumer.assignment().isEmpty()) {
                    System.out.println("assignment after join: " + consumer.assignment());
                    printedAssignment = true;
                }
                total += batch.count();
                System.out.println("poll " + pollN + ": " + batch.count() + " records");
                if (pollN >= 12) break;
            }
            System.out.println("total records delivered in batched polls: " + total);
        }
    }
}
```

**Listing 1.** Run against kafka-clients 4.3.1 on a 6-record partition:

```console
poll 1: 0 records
poll 2: 0 records
poll 3: 0 records
poll 4: 0 records
poll 5: 0 records
poll 6: 0 records
assignment after join: [poll-topic-0]
poll 7: 6 records
total records delivered in batched polls: 6
```

**Listing 2.** The early polls are the group protocol at work — join, sync, fetch warm-up — before the first batch arrives, all six records in one poll.

```d2
direction: right
sub: "subscribe(topics)\njoin intent" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
group: "group coordinator\nassigns partitions" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
pl: "poll()\njoin · heartbeat · fetch" {
  width: 250
  height: 80
  style.fill: "#fff3e0"
}
rec: "ConsumerRecords\nbatched, offset order" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
sub -> group: first poll
group -> pl
pl -> rec
```

**Fig. 1.** Subscription states the intent, the coordinator places partitions, and poll performs membership and fetching in one loop that ends with a batch.

Group coordination itself — who assigns, what the coordinator stores — is the subject of [[What is a Kafka consumer group coordinator for]], and the behavior when a second consumer joins the same group (partitions split) versus a different group (full copy) is [[What happens when a second Kafka consumer reads the same topic]].

> [!warning] Everything group-related happens inside poll — including losing the group
> If processing stalls longer than `max.poll.interval.ms`, the client proactively leaves the group; the next commit fails with `CommitFailedException` and the partitions are reassigned. Heartbeats alone do not save you — they prove the process is alive, while the poll interval proves it is making progress; the two timeouts are compared in [[What is the difference between session.timeout.ms and max.poll.interval.ms]].

> [!tip] Interview answer
> subscribe puts the consumer into a group where the coordinator decides which partitions it owns; assign is the manual alternative. poll is the heartbeat of the whole model — it joins, keeps membership alive, participates in rebalances, fetches, and returns records batched in offset order. Stop polling past max.poll.interval.ms and you are out of the group; the first polls often return nothing while join completes.

