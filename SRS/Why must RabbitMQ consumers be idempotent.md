<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #API/Idempotency

# Why must RabbitMQ consumers be idempotent

> [!abstract] Short answer
> Because at-least-once delivery is the safe operating mode, and it means redeliveries are normal: crashes before ack, nack-requeue, connection losses, and publisher republishes of unconfirmed messages all can deliver the same logical message twice. A non-idempotent handler turns that safety into duplicates.

## Where duplicates come from

The requeue machinery — [[What happens if a RabbitMQ consumer crashes before ack]] — redelivers unacked deliveries after any channel loss. Consumers also requeue deliberately for retries. And publishers without confirms must republish when a publish's fate is unknown, potentially duplicating an in-flight message. None of these paths can distinguish "message processed" from "message delivered" after the fact, so the handler must make repetition harmless — the [[What is the Idempotent Receiver pattern|Idempotent Receiver]] contract.

```d2
direction: down
crash: "crash before ack" {
  width: 190
  height: 70
  style.fill: "#ffebee"
}
nack: "nack requeue (retry)" {
  width: 210
  height: 70
  style.fill: "#ffebee"
}
rep: "republish unconfirmed" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}
redel: "redelivery" {
  width: 160
  height: 60
  style.fill: "#fff3e0"
}
dup: "handler must survive it" {
  width: 230
  height: 70
  style.fill: "#e8f5e9"
}
crash -> redel
nack -> redel
rep -> redel
redel -> dup
```

**Fig. 1.** Three structural redelivery sources converge on one requirement: repetition-safe processing.

## Idempotency techniques

Dedup keys are the standard: store a unique event/message id with the state change in one transaction, or use an upsert, so the second delivery is a no-op. Conditional updates (`update ... where status='new'`) achieve the same via database semantics. Retries after *unknown* outcomes (timeout on the side effect) need the same treatment — a response lost does not mean the effect was lost. This pairs with [[What delivery guarantees does RabbitMQ provide]] for the mode that makes it necessary.

```java
// insert-if-absent in one tx; second delivery is a no-op
insert into processed_events(event_id) values (?); // unique key
update account set balance = balance + ? where id = ?;
```

**Listing 1.** Conceptual dedup: the unique event id plus the state change committed together.

> [!warning] The redelivered flag is not a dedup key
> redelivered=true tells you the delivery is not the first attempt — but the first attempt may have half-executed, and the flag is false for a message that was redelivered to a different consumer chain. Dedup must key on message/event identity, not on delivery metadata.

> [!tip] Interview answer
> RabbitMQ's at-least-once path — crash requeues, retry topologies, republished unconfirmed sends — makes duplicate deliveries normal. Consumers must therefore be idempotent: unique event ids in a dedup table, upserts, or conditional updates so processing twice equals processing once. Otherwise reliability settings create double-charges.
