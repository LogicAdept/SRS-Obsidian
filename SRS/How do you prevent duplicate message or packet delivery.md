<!--
reps: 0
priority: 0
-->
#Networking/TCP #DistributedSystems/Communication #SRS
# How do you prevent duplicate message or packet delivery

> [!abstract] Short answer
> You cannot stop duplicates from appearing — networks retransmit and retry, so duplicates are normal. Prevention means making delivery **detectable and idempotent**: at the transport layer TCP uses sequence numbers so retransmitted segments collapse into one byte stream, and at the application layer a consumer deduplicates by a message id (or makes the same operation naturally idempotent) so "at-least-once" delivery behaves like "effectively once".

## Layer 1: TCP sequence numbers

TCP numbers every byte. A retransmitted segment carries the same sequence range as the original, and the receiver accepts whichever copy arrives first and discards the other — the application sees one ordered byte stream (RFC 9293). Deduplication happens implicitly because the receive buffer is keyed by sequence numbers, and the ACK number tells the sender which data actually landed. A stale duplicate from an old connection cannot leak in because each connection has a fresh pair of ISNs from the three-way handshake.

```java
// Conceptual: TCP hides duplicates, but the socket API stays a plain byte stream
InputStream in = socket.getInputStream();
byte[] buf = new byte[1024];
int n = in.read(buf); // retransmitted segments never surface here
```

**Listing 1.** The application never observes retransmissions — duplicate segments are filtered by sequence numbers inside TCP.

## Layer 2: application-level idempotency

TCP deduplicates within one connection only. Retries above TCP — an HTTP client resending after a timeout, a broker redelivering to a consumer — arrive on a new connection and TCP cannot help. The standard pattern:

1. Attach a unique **message/event id** (client-generated UUID, or a business key like `order-42-payment`).
2. On the consumer, store processed ids (a database unique constraint is the strongest form) or track the last applied offset/sequence per partition.
3. If the id is already processed, acknowledge and skip — the side effect happened exactly once.

```sql
CREATE TABLE processed_events (
    event_id TEXT PRIMARY KEY,
    result   TEXT NOT NULL
);
INSERT INTO processed_events(event_id, result) VALUES ($1, $2); -- second delivery fails -> skip
```

**Listing 2.** A unique key turns "already delivered" into a constraint violation, which the consumer treats as success.

> [!warning] Exactly-once is a delivery+processing contract, not a network property
> Networks and brokers offer at-most-once or at-least-once; "exactly-once" exists only where delivery is combined with idempotent processing (or transactional consumption). Claiming "TCP guarantees exactly-once delivery" is a classic interview lie: TCP guarantees an ordered, duplicate-free **byte stream for one connection**, nothing about what happens after a connection dies mid-transfer.

Related: [[What is the difference between TCP and UDP]] for why UDP applications must design their own dedup, [[What is the TCP three-way handshake]] for how fresh ISNs isolate old duplicates, and [[What is idempotency in HTTP and in messaging]] for the HTTP method semantics side.

> [!tip] Interview answer
> Duplicates are inherent — retries exist, so I design for detection instead of prevention. TCP already deduplicates inside a connection with sequence numbers. Across connections, I make processing idempotent: a unique message id plus a database unique constraint or a version/offset check, so redelivery is acknowledged but not applied. That is the honest form of exactly-once.
