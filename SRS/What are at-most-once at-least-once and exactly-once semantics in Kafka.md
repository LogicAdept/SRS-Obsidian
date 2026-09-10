<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #API/Idempotency #SRS

# What are at-most-once at-least-once and exactly-once semantics in Kafka?

> [!abstract] Short answer
> They describe what happens to a record across producer and consumer failures. **At-most-once**: a record is processed zero or one times — loss is possible, duplicates are not. **At-least-once** (Kafka's default): zero loss, duplicates possible after retries or reprocessing. **Exactly-once**: no loss, no duplicates — in Kafka achieved with the idempotent producer, transactions, and `isolation.level=read_committed`, or by Kafka Streams with the same primitives.

Delivery semantics break into two independent halves: the durability of **publishing** a record, and what the consumer does between **processing** and **committing its position**. On the publish side, `acks=0` can silently drop records, `acks=1` can lose records acknowledged by a leader that then fails, and `acks=all` with the idempotent producer (default since 3.0) gives lossless, duplicate-free writes to the log. On the consume side, the consumer controls its position, and the ordering of "process the record" versus "commit the position" picks the semantics.

## The consume side decides the semantics

```java
// Conceptual: the two orderings behind at-least-once and at-most-once
// at-least-once: process first, then save the position
records.forEach(app::process);
consumer.commitSync(positionOf(records));      // crash before commit → records reprocessed

// at-most-once: save the position first, then process
consumer.commitSync(positionOf(records));      // crash before process → records lost
records.forEach(app::process);
```

**Listing 1.** Conceptual orderings. The consumer reads records, processes them, and stores its position — the crash window between those steps decides whether records repeat or vanish.

```d2
direction: right
atmost: "at-most-once\ncommit → process" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
atleast: "at-least-once\nprocess → commit" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
exactly: "exactly-once\nprocess + commit in one transaction" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
loss: "loss possible\nno duplicates" {
  width: 200
  height: 70
  style.fill: "#ffebee"
}
dup: "no loss\nduplicates possible" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
none: "no loss\nno duplicates" {
  width: 190
  height: 70
  style.fill: "#e8f5e9"
}
atmost -> loss
atleast -> dup
exactly -> none
```

**Fig. 1.** The three semantics as consequences of ordering processing against the position commit; exactly-once merges the output write and the position commit into one atomic step.

Exactly-once for read-process-write flows inside Kafka uses the transactional producer: the consumer's position is itself a record in an internal topic, so the producer can write output records and the position update in the same transaction. If it aborts, the position reverts and output records are hidden from `read_committed` consumers. This is covered step by step in [[What happens during a Kafka consume-transform-produce transaction]] and [[How do you achieve exactly-once processing in Kafka]].

> [!warning] Exactly-once is not a property of the log alone
> The claim covers read-process-write flows inside Kafka. A consumer writing to a database or an external API still owns its side effects: no broker setting stops your service from charging a card twice when it reprocesses a record. Sinks need idempotent writes, upserts by event id, or a two-phase-commit-style layout — see [[What is the difference between Kafka delivery guarantees and application exactly-once]].

> [!tip] Interview answer
> At-most-once means the consumer saves its position before processing — a crash can skip records but never repeats them. At-least-once, the default, processes first and commits after — a crash repeats records but never skips them. Exactly-once combines the idempotent producer, transactions, and read-committed consumers so that output records and the input offset land atomically; outside Kafka you still need an idempotent sink.

