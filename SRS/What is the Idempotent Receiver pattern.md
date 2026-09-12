<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #API/Idempotency #Patterns/Architecture/Microservices/CommunicationStyles #SRS

# What is the Idempotent Receiver pattern?

> [!abstract] Short answer
> An **Idempotent Receiver** can **safely receive the same message more than once**: either duplicates are explicitly de-duped on arrival (a processed-ids store), or the message's semantics are designed so that applying it twice has the same effect as once.

## Two routes to idempotency

Redelivery is the norm, not an anomaly: retries after timeouts, reconnections, failovers, and at-least-once delivery all re-present messages that may have been processed. The receiver has exactly two defenses. **Explicit de-duping**: record each handled message's unique id before or with the business work; a repeated id is skipped — the standard implementation is a dedup table written inside the same transaction as the business change, so "seen it" and "did it" commit or roll back together. **Idempotent semantics by design**: make the operation naturally repeatable — an absolute `setStatus(shipped)` instead of an incremental `incrementShipmentCount()`, or an upsert keyed by a business key. The mathematical sense is f(x) = f(f(x)): applying the message again does not change the outcome. This pairs with [[What is the Transactional Client pattern]] (redelivery is what makes it necessary) and with [[What is the Competing Consumers pattern]] (parallel duplicates). Do not confuse it with the producer-side mechanism in Kafka — [[What is an idempotent Kafka producer for]] — which dedups retries within the broker, not application processing.

```d2
direction: down
m: "Message id=42\n(delivered twice)" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
chk: "Seen before?\nprocessed_ids lookup" {
  width: 230
  height: 65
  style.fill: "#fff3e0"
}
biz: "Process business work\n+ insert id (same tx)" {
  width: 250
  height: 70
  style.fill: "#e8f5e9"
}
skip: "Skip duplicate\nack only" {
  width: 180
  height: 55
  style.fill: "#ffebee"
}
m -> chk
chk -> biz: "no"
chk -> skip: "yes"```

**Fig. 1.** The dedup check and the business work share one transaction; the second copy of the message acks without effects.

## Dedup as a transaction, not a flag

```sql
BEGIN;
INSERT INTO processed_messages (message_id) VALUES ('42'); -- unique key
UPDATE accounts SET balance = balance - 100 WHERE id = 'A-1';
COMMIT;  -- duplicate delivery: INSERT conflicts, nothing else happens
```

**Listing 1.** The unique key on `message_id` turns the second delivery into a no-op atomically — the insert conflict is the dedup decision. The same receiver-side discipline reappears in the microservices vocabulary as the idempotent consumer of [[What is the messaging communication style between microservices]].

> [!tip] Interview answer
> An Idempotent Receiver survives duplicate deliveries either by explicit dedup — a processed-id table written in the same transaction as the business work — or by designing the effect so repeats are harmless, like absolute status updates or upserts. At-least-once delivery makes this mandatory, not optional; and Kafka's idempotent producer is a different mechanism that only dedups producer retries inside the broker.
