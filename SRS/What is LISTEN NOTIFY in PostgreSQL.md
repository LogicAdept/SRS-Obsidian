<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is LISTEN NOTIFY in PostgreSQL?

> [!abstract] Short answer
> A transactional publish-subscribe mechanism inside one database: sessions register with LISTEN channel, and NOTIFY channel, 'payload' delivers an event to every listening session when the sending transaction commits. Delivery is at-most-once between transactions, payload is a short string (under 8000 bytes), and it is fully ACID-integrated — a rolled-back transaction notifies nobody.

## The contract

- NOTIFY inside a transaction queues events; they are delivered to listeners only at commit — abort discards them.
- A listening session in a transaction receives queued events just after its transaction ends: notifications are delivered between transactions, never inside one.
- Duplicate NOTIFY on the same channel with identical payload within one transaction collapses into one event; different payloads or different transactions stay distinct.
- Delivery order follows commit order.

```sql
-- sender
NOTIFY order_created, '12345';
-- listener (dedicated connection)
LISTEN order_created;
-- wait: notification arrives with channel, sender PID, payload
```

**Listing 1.** The minimal pair. Drivers expose it as a wait/poll on the dedicated connection ([[What is the difference between a process and a connection in PostgreSQL]] — session state lives in one backend).

```d2
pub: "Publisher transaction\nNOTIFY queued" {width: 300; height: 70}
commit: "COMMIT\nevents become deliverable" {width: 260; height: 60}
q: "Per-database queue\n(~8 GB, dedup identical payloads)" {width: 340; height: 80}
sub: "Listener backends\nevents between transactions" {width: 320; height: 80}
pub -> commit -> q -> sub
```

**Fig. 1.** Events ride a transactional queue and fan out to all listening sessions at commit boundaries.

## Typical uses

- Cache invalidation fan-out: any writer commits, all app instances drop the key ([[Is caching only used with databases]] patterns inside the DB).
- Triggering workers: a commit signals "new batch ready" without polling loops.
- Simple job ping: payload carries the row key; details go in a table ([[What is COPY in PostgreSQL]] for the bulk ingest side).

## Limits that decide architecture

No persistence: events are lost if no listener is connected at commit time; no replay, no acknowledgment, no ordering across sessions beyond commit order; one database's scope. For durable, replayable messaging you need a broker ([[What is the difference between Kafka and RabbitMQ]] is the nearest comparison in this vault); NOTIFY is a signal bus, not a message queue.

> [!warning] Transaction pooling breaks LISTEN
> With pgBouncer in transaction mode ([[Why use pgBouncer with PostgreSQL]]), a LISTEN may land on one server connection while the NOTIFY-waiting code waits on another — the event never arrives. LISTEN requires a dedicated, session-pinned connection; the second classic failure is a long-open listener transaction blocking queue cleanup until the queue fills and senders start failing at commit.

> [!tip] Interview answer
> LISTEN/NOTIFY is in-database pub/sub: listeners register on a channel, notifications queue with the sender's transaction and fan out at commit — transactional, deduplicated, sub-8000-byte payloads, no persistence or replay. Great for cache invalidation and worker wake-ups on a dedicated connection; under transaction pooling it breaks, and durable messaging belongs in a broker.
