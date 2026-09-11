<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka Consumer API for?

> [!abstract] Short answer
> Reading records from topics from your own process: one class, `KafkaConsumer` from kafka-clients, covers group membership, fetching, position control, offset commits, and rebalance callbacks. It is the tool when the logic is yours — branching, business rules, custom sinks — and neither Kafka Connect nor a framework fits ([[What core Kafka APIs exist]]).

## Four clusters of methods

```d2
direction: down
membership: "Membership\nsubscribe / assign\npoll / wakeup / close" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
position: "Position\nposition / committed\nseek / seekToBeginning / seekToEnd" {
  width: 320
  height: 100
  style.fill: "#fff3e0"
}
commits: "Commits\ncommitSync / commitAsync\nor the auto-commit timer" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
metadata: "Metadata\npartitionsFor / beginningOffsets\nendOffsets / offsetsForTimes" {
  width: 320
  height: 100
  style.fill: "#f3e5f5"
}
membership -> position: poll advances
position -> commits: you commit
```

**Fig. 1.** The method families: membership decides which partitions you get, poll advances the in-memory fetch position, commits persist it, and metadata methods enable time-based replay.

`subscribe(topics)` enrolls the consumer in a group with dynamic assignment; `assign(partitions)` fixes partitions manually — the two cannot be mixed, and calling one after the other throws `IllegalStateException`. `poll(Duration)` is the engine: it joins the group on first call, fetches batches, and returns `ConsumerRecords` ([[What are Kafka subscribe and poll for]]) — liveness is governed by how often you call it, while heartbeats flow from a background thread ([[What is the Kafka consumer heartbeat thread for]]). The consumer tracks two positions: the *fetch position* — the offset of the next record `poll` returns — and the *committed position* — the last offset stored safely in the group so a restart resumes from there ([[What is Kafka Consumer position for]]). Commits are manual via `commitSync`/`commitAsync` or the auto-commit timer ([[What are Kafka commitSync and commitAsync for]]). Seek methods reposition within a partition — replaying, skipping, or jumping by time with `offsetsForTimes` — which is the API behind [[How do you replay Kafka messages from an older offset]]. `ConsumerRebalanceListener` hooks run when partitions are revoked and assigned, typically to commit or flush before handover ([[What triggers a Kafka consumer group rebalance]]).

## Manual assignment and a seek, not just a loop

```java
var tp = new TopicPartition("orders", 3);
consumer.assign(List.of(tp));          // fixed partition, no group placement
consumer.seek(tp, 42_000);             // start from an explicit offset
while (running) {
    ConsumerRecords<String, String> batch = consumer.poll(Duration.ofMillis(200));
    batch.forEach(this::handle);
    consumer.commitSync();             // commits the position of every assigned partition
}
```

**Listing 1.** With `assign` there is no rebalancing, but `group.id` still names where committed offsets live; the loop shape is unchanged.

The client handles broker failures and partition migration between fetches transparently, and communicates with brokers as far back as 0.10.0 — newer operations fail with `UnsupportedVersionException` rather than corrupting anything. Kafka 4.x additionally ships a separate `KafkaShareConsumer` for queue-style share groups where records are acknowledged individually instead of being partition-locked; the classic consumer remains the partition-based default.

> [!warning] Not thread-safe — except wakeup()
> A `KafkaConsumer` is owned by one thread; calling most methods from outside is a race, not a style issue. The single exception is `wakeup()`, which is safe from any thread and interrupts a blocked `poll` for shutdown. For parallelism, keep one consumer thread and hand records to a worker pool — do not share the consumer itself.

> [!tip] Interview answer
> The Consumer API is the read side of kafka-clients: subscribe or assign to get partitions, poll in a loop to fetch and to stay alive, seek to reposition, and commitSync or commitAsync to persist progress. It tracks a fetch position and a committed position separately, it is not thread-safe apart from wakeup, and it is what you use when a connector or a processing library would be too much — the plain consume-transform-produce substrate.

