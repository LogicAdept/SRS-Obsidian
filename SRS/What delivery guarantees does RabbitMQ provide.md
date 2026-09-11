<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #API/Idempotency

# What delivery guarantees does RabbitMQ provide

> [!abstract] Short answer
> RabbitMQ gives you at-most-once (auto-ack or unconfirmed publishes) and at-least-once (manual acks plus publisher confirms) as practical modes; exactly-once is not a broker primitive — it is at-least-once plus idempotent processing, optionally with dedup at the consumer.

## The three levels

At-most-once: the broker forgets deliveries on send (auto-ack) or publishes without confirms, so crashes lose messages but nothing is processed twice from redelivery. At-least-once: the confirmed-publish/manual-ack pair guarantees no silent loss; duplicates appear after crashes or redeliveries — that is structural, not a bug. Exactly-once end-to-end is impossible at the broker level alone: the broker can dedup neither a client's business side effects nor a consumer's database write; the standard design is idempotent handlers keyed by message id or event id, in line with [[What is the Idempotent Receiver pattern]].

```d2
direction: down
most: "at-most-once\nauto-ack, no confirms" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
least: "at-least-once\nconfirms + manual acks" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
ex: "exactly-once\nat-least-once + idempotent handler" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
most <- -> least: "tradeoff: loss vs duplicates"
least -> ex: "app-level dedup"
```

**Fig. 1.** The trade-off axis: fewer guarantees lose data, stronger ones need consumer-side dedup.

## What the broker contributes

Publisher confirms tell you the broker accepted responsibility (persisted for quorum); manual acks tell the broker processing completed; redelivery closes crash gaps; delivery limits stop poison loops. Everything else — dedup, transactional side effects, idempotency — lives in the application, and [[Why must RabbitMQ consumers be idempotent]] explains why that is non-negotiable under at-least-once.

> [!warning] "RabbitMQ supports exactly-once" is the legendary lie
> The broker has no exactly-once delivery mode; quorum queues' "effectively once" dedup concerns AMQP 1.0 stream-style duplicates, not consumer side effects. Anyone claiming broker exactly-once for business processing has conflated transport with application semantics.

> [!tip] Interview answer
> You get at-most-once with auto-ack or missing confirms, at-least-once with confirms plus manual acks and redelivery, and exactly-once processing only by adding idempotent handlers or dedup keys on top. The broker guarantees acceptance and requeue semantics; side effects are your problem.
