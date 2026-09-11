<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/CQRS #Methodologies/DDD #SystemDesign/Consistency #SRS

# How does an aggregate persist and publish events without a distributed transaction

> [!abstract] Short answer
> The standard answer is the transactional outbox: in the same local database transaction that persists the aggregate, insert the domain events into an outbox table; a separate relay (polling publisher or CDC log reader) reads the outbox afterwards and publishes the events to the message broker. Atomicity is preserved locally (state change + event are one commit), and publication is eventually consistent — no 2PC across database and broker.

## Why the naive approaches fail

Two obvious designs are both broken. Publish-then-commit: the service publishes the event to the broker, then commits the aggregate — if the commit fails afterwards, consumers already processed an event for a change that never happened (a phantom event). Commit-then-publish: commit first, then publish — if the process dies between the two, the event is lost forever, and consumers miss a change that happened. Both attempt to atomically update two systems (database, broker) — exactly what a distributed transaction (2PC) exists for, and exactly what Fowler's article argues to avoid in modern systems (2PC-level cost: coordination, blocking, brittleness across availability boundaries). The microservices.io transactional-outbox pattern names the goal precisely: atomically update the database AND send messages, using only the database's own transaction.

## The outbox mechanics

Write both in one transaction: `UPDATE aggregate ...; INSERT INTO outbox(event_type, payload, ...) COMMIT;` — atomic because both are rows in the same database. The relay then publishes asynchronously. Two relay styles: polling publisher — a scheduled job queries unpublished outbox rows, publishes each to the broker, marks them published (simple; adds polling latency; needs ordering care); log-based CDC — a tailer reads the database commit log (Debezium-style) and publishes each inserted outbox row as it appears (lower latency, exactly the commit order, no extra queries; more infrastructure). Guarantees and obligations: delivery to the broker is at-least-once (the relay may crash after publishing but before marking), so consumers must be idempotent or deduplicate ([[What is idempotency in HTTP and in messaging]] — usually by event id); the outbox table needs its own housekeeping (retention, cleanup) and index design; read-your-writes spans database and downstream consumers only after the relay's lag elapses ([[What is eventual consistency]]). The aggregate's own persistence stays a plain ACID transaction — [[What is the difference between atomicity and consistency]] names what the local transaction still guarantees.

```sql
BEGIN;
UPDATE orders   SET status = 'PAID'      WHERE id = 42;
INSERT INTO outbox (event_type, payload, published)
VALUES ('OrderPaid', '{"orderId":42}', false);
COMMIT;   -- state + event: one atomic local transaction

-- relay (poll): SELECT * FROM outbox WHERE published = false
--               -> publish to broker -> mark published = true
```

**Listing 1.** The outbox: aggregate update and event insert share one commit; the relay publishes afterwards.

> [!warning] The outbox moves the problem to the consumer's idempotency
> At-least-once publication means a consumer can receive an event twice (relay crash between publish and mark). Without deduplication by event id, the same order can be "paid" twice downstream — the outbox guarantees exactly-once effect only when consumers cooperate.

> [!tip] Interview answer
> I use the transactional outbox: persist the aggregate and insert its domain events in the same local transaction — atomic by the database, no 2PC. A relay (poller or CDC log reader) publishes rows to the broker afterwards, at-least-once, so consumers deduplicate by event id. It trades a small publication lag for removing distributed transactions entirely.
