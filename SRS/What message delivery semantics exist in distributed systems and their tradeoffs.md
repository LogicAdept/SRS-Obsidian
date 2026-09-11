<!--
reps: 0
priority: 0
-->
#DistributedSystems/Communication #Messaging #SystemDesign/Tradeoffs #SRS

# What message delivery semantics exist in distributed systems and their tradeoffs

> [!abstract] Short answer
> Three delivery guarantees span the spectrum: at-most-once (send once, never retry — may lose messages, never duplicates; cheapest), at-least-once (retry until acknowledged — no losses, but duplicates are possible, so consumers must be idempotent or deduplicate), and exactly-once (each message affects the consumer exactly once — the strongest and most expensive, achieved by transactional/deduplicated pipelines, not by the network being nice). The tradeoff is the cost of guarantee versus the cost your consumers pay to compensate.

## The three guarantees, mechanically

At-most-once: the producer sends (fire-and-forget or with abort-on-first-error) and never resends — a lost message is lost. It suits metrics, telemetry and other drop-tolerant flows where latency and cost dominate. At-least-once: the producer (or broker-redelivery) retries until the consumer acknowledges — RabbitMQ's manual acknowledgements and Kafka's producer retries with acks give this class; the price is duplicates: a consumer that processed a message but died before acknowledging will receive it again ([[How do you implement retries in RabbitMQ]] for the mechanics, [[How do you handle a poison pill message in Kafka]] for the failure sibling). Consumers therefore need idempotent effects or deduplication — consumer-side tracking of processed message ids (Kafka's idempotent producer and transactions raise part of this into the protocol; [[What is an idempotent Kafka producer for]] covers the producer side). Exactly-once: each message's effect appears exactly once despite retries, failures and replays. Achieved by pairing the message pipeline with transactional state: Kafka's transactional producer + read-committed consumers + offsets committed in the same transaction; or application-level — an outbox ([[How does an aggregate persist and publish events without a distributed transaction]]) plus idempotent consumers keyed by event id. The JMS specification's classic vocabulary names the same trio (at-most-once, at-least-once, once-and-only-once), which shows how old and universal the tradeoff is.

```text
at-most-once : send, no retry       -> loss possible, no dupes  (cheap)
at-least-once: send until acked     -> no loss, dupes possible
               consumer: idempotent / dedup by message id
exactly-once : transactional pipeline (Kafka txn) or outbox + dedup
               -> no loss, no dupe effects  (most infra + latency)
```

**Listing 1.** The spectrum with its price and compensation.

## Choosing per flow, not per company

The guarantee is chosen per message flow against the cost of each failure mode: losing a payment event is unacceptable (at-least-once with idempotent consumers, or exactly-once); losing a metrics datapoint is fine (at-most-once); double-charging a card is worse than losing a notification, but exactly-once infrastructure for the notification would be waste. The subtle interview point: "exactly-once delivery" is only meaningful as exactly-once processing — the effect on state is what matters; networking cannot promise it, only the pairing of redelivery with transactional/deduplicated consumer state can ([[What is eventual consistency]] explains the lag that transactional pipelines still accept). Brokers expose the knobs: producer acknowledgements and retries (dupe window), consumer acknowledgement modes (auto vs manual — [[How do competing consumers work in RabbitMQ]]'s ack semantics), and dead-lettering for messages that exhaust redelivery. The full resilience stack ([[When is a retry policy suitable for a command or API call]], [[How do you protect a slower downstream service from overload]]) assumes one of these semantics — the delivery guarantee is the contract the retry policy is built on.

> [!warning] Exactly-once is a property of the whole pipeline, not a checkbox
> A transactional producer with a non-idempotent consumer still double-processes; an idempotent consumer behind an at-most-once producer still loses messages. The guarantee holds only across producer, broker and consumer configured together — every link chooses the weakest one.

> [!tip] Interview answer
> The three semantics: at-most-once (cheap, may lose), at-least-once (no loss, needs idempotent consumers), exactly-once (transactional pipeline or outbox-plus-dedup — no loss, no dupe effects, most infrastructure). I pick per flow: telemetry at-most-once, business events at-least-once with idempotency, payment paths exactly-once — and I always say "exactly-once processing", because that is what can actually be built.
