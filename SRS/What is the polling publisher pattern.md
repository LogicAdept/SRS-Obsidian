<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Data #Messaging #Databases/Transactions #SRS

# What is the polling publisher pattern

> [!abstract] Short answer
> Polling publisher moves outbox rows to the message broker by periodically querying the outbox table: poll for rows newer than the last published ID, publish them, advance the marker. It is the simple relay companion of [[How would you explain the transactional outbox pattern]] - works with any SQL database, at the price of polling latency and tricky strict ordering.

## Mechanism: table as queue, ID as cursor

The outbox table is insert-only, and its primary key is monotonic (auto-increment or a sequence), which makes it a natural cursor source. The publisher loop: SELECT rows WHERE id greater than lastPublishedId ORDER BY id LIMIT batch, publish each to the broker, then persist lastPublishedId. The marker must live durably outside the process - its own table or row - so a restarted publisher resumes where the previous one died instead of replaying everything. My verified micro-case shows exactly that: three rows published, marker at id=3, a simulated crash, a new process restoring the marker, then two later rows published once, in ID order (MS03 in empirics). Two consequences follow directly. Latency: consumers learn of an event only on the next poll cycle, so the cadence trades latency for database load. Duplicates: if the process dies between publishing a row and advancing the marker, the restarted publisher re-publishes that row - at-least-once semantics, which pushes deduplication to the consumer ([[What is the Idempotent Receiver pattern]] is the receiver-side pattern; a concrete broker example is [[Why must RabbitMQ consumers be idempotent]]).

```d2
direction: right
svc: "Service
business tx writes
entity + outbox row" {style.fill: "#e8f5e9"}
tbl: "Outbox table
id 1..N, insert-only" {style.fill: "#fff3e0"}
poller: "Polling publisher
SELECT id > marker" {style.fill: "#ffe0b2"}
mark: "Marker
lastPublishedId" {style.fill: "#ffe0b2"}
broker: "Message broker" {style.fill: "#eceff1"}
svc -> tbl: same local transaction
poller -> tbl: poll batch
poller -> broker: publish
poller -> mark: advance after publish
```

**Fig. 1.** The poller walks the outbox in primary-key order; the durable marker defines what is already published.
```java
void pollOnce() {
    for (OutboxRow r : outbox.selectAfter(lastPublishedId, 100)) {
        System.out.println("  publish id=" + r.id + " " + r.event);
        lastPublishedId = r.id;              // advance only after publish succeeds
    }
}
```

**Listing 1.** Verified on JDK 21 (MS03_PollingPublisher in empirics): cycle 1 publishes ids 1-3 and parks the durable marker at 3; after a simulated crash the restarted poller restores the marker and publishes only `publish id=4 OrderShipped id=8` and `publish id=5 OrderDelivered id=9` — no gaps, no replays.


## Why the alternative exists

Richardson's stated drawbacks: publishing events in order is tricky (multiple poller instances or retry loops can reorder rows - consumers must tolerate duplicates and often out-of-order arrival), and NoSQL stores without queryable monotonic IDs do not support the pattern. Transaction log tailing reads the database's change log instead - lower latency, no extra polling load on the database, but it couples the relay to database-internal formats (Debezium-style CDC). The interview-shaped comparison: polling is the boring default for modest throughput and SQL stores; tailing is the upgrade when latency or database load becomes the constraint. Both share the same contract with consumers: at-least-once delivery, so idempotence is not optional downstream.

> [!warning] The marker and the poll are the whole pattern
> Get either wrong and the failure is invisible until production: a marker stored only in the publisher's memory means a restart replays the entire outbox to consumers; polling with ORDER BY id but no index on it scans the growing table on every cycle; deleting published rows to keep the table small breaks the "resume from marker" recovery. A second trap: running multiple poller instances against one outbox without partitioning - both publish the same rows, in racing order.

> [!tip] Interview answer
> Polling publisher relays outbox rows to the broker by querying the outbox table in primary-key order and advancing a durable last-published marker. It is simple, works with any SQL database, and gives at-least-once delivery - duplicates on crash, so consumers must be idempotent. Latency is bounded by the poll cycle; when that or DB load hurts, I switch to transaction log tailing.
