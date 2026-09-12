<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #Databases/Transactions #SRS

# How would you explain the transactional outbox pattern?

> [!abstract] Short answer
> The **Transactional Outbox** solves the dual-write problem: instead of writing to the database **and** sending to the broker (two systems, no shared transaction), the service writes the event into an **outbox table in the same local ACID transaction** as the business data, and a separate publisher ships outbox rows to the broker afterwards.

## One transaction, one database, no 2PC

A service command typically must update business entities **and** publish an event atomically; a traditional distributed transaction spanning database and broker is usually unavailable or undesirable. Sending a message mid-transaction is simply unreliable — the send succeeds and the transaction later rolls back, or the reverse. The outbox sidesteps the distributed transaction: the event is inserted into an `outbox` table (message body, destination, headers) inside the very same local transaction as the business change — commit either makes both happen or neither. Publication then happens separately: a publisher reads unsent outbox rows and publishes them to the broker, marking them sent. The publisher half has two canonical implementations — its own pattern pages: [[How would you explain the polling publisher pattern]] and [[How would you explain transaction log tailing for integration]]. The delivery contract becomes at-least-once — a publisher crash between send and mark causes a redelivery — so consumers need [[What is the Idempotent Receiver pattern]]-style dedup, and outbox ordering should follow a monotonically increasing column.

```d2
direction: down
svc: "Service\nbusiness logic" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
tx: "Local ACID transaction\nUPDATE orders + INSERT outbox" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
pub: "Publisher\npoll / tail the outbox" {
  width: 240
  height: 65
  style.fill: "#fff3e0"
}
br: "Message broker" {
  width: 170
  height: 55
  style.fill: "#e8f5e9"
}
svc -> tx
tx -> pub: "read unsent rows"
pub -> br: "publish"```

**Fig. 1.** Atomicity comes from the local transaction; the broker sees the event only after the business data is committed.

## The outbox write is the whole trick

```sql
BEGIN;
UPDATE orders SET status = 'APPROVED' WHERE id = 42;
INSERT INTO outbox (aggregate_id, type, payload, sent)
VALUES (42, 'OrderApproved', '{"orderId":42}', false);
COMMIT;  -- both rows or neither: no dual-write gap
```

**Listing 1.** The event is just another row in the same transaction — atomic by construction, publishable later. The two relays that move those rows to the broker are [[What is the polling publisher pattern]] and transaction log tailing, and the events themselves are born inside [[What is the domain event pattern in microservices]].

> [!tip] Interview answer
> The Transactional Outbox fixes the dual-write problem by writing the event into an outbox table within the same local database transaction as the business change — atomically, without 2PC across database and broker. A separate publisher then ships unsent outbox rows to the broker, via polling or log tailing. Delivery is at-least-once, so consumers must dedup, and publisher lag is the metric to watch.
