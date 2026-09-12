<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration #Databases/Transactions #Messaging/Tools/Kafka #Patterns/Architecture/Microservices/TransactionalMessaging #SRS

# How would you explain transaction log tailing for integration?

> [!abstract] Short answer
> **Transaction log tailing** publishes outbox (or table) changes to a broker by **reading the database's own transaction log** — the mechanism the database already writes for replication — turning commits into change events with no queries against the business tables.

## The database already wrote the event stream

Every modern database records changes in a transaction log — MySQL's binlog, PostgreSQL's WAL — primarily for replication and recovery. The same stream is the physical substrate that event-sourced designs build on deliberately ([[How would you explain the event sourcing pattern]] keeps the log as the system of record); tailing is how a conventional database plays the same role without re-architecting. Log tailing reuses that stream for integration: a reader (Kafka Connect's source connectors being the standard tooling, including Debezium-style setups) subscribes to the log, decodes committed changes to the outbox table, and publishes each one to the broker. Compared with [[How would you explain the polling publisher pattern]] it inverts the trade-offs: events flow **at commit speed** rather than on a poll interval, the business database sees **no extra query load**, and the stream is **guaranteed accurate** — it is the same source replication trusts, ordered per the log. The costs are equally real: the mechanism is **database-specific** (binlog reader vs WAL logical decoding are different integrations), the tooling is comparatively **obscure** though increasingly common, and **duplicate publishing is tricky to avoid** — log readers replay from checkpoints, so consumers still see at-least-once. Common production shapes: Kafka Connect reading the WAL/binlog into Kafka topics; DynamoDB table streams as the managed-cloud analogue. Inside Kafka the resulting stream then obeys the platform's own rules — per-partition ordering and offsets — covered in [[What ordering guarantees does Kafka provide for messages]].

```d2
direction: right
svc: "Service\ncommits outbox row" {
  width: 210
  height: 65
  style.fill: "#e3f2fd"
}
wal: "Transaction log\nWAL / binlog" {
  width: 200
  height: 65
  style.fill: "#fff3e0"
}
tail: "Log reader\n(Kafka Connect)" {
  width: 200
  height: 65
  style.fill: "#fff3e0"
}
br: "Broker / Kafka" {
  width: 170
  height: 55
  style.fill: "#e8f5e9"
}
svc -> wal -> tail -> br```

**Fig. 1.** The commit itself becomes the trigger: the log reader decodes what the database already wrote.

## Where the events come from

```text
Database     Log              Reader mechanism
-----------  ---------------  --------------------------------------
PostgreSQL   WAL              logical decoding slot -> connector
MySQL        binlog           row-format binlog reader
DynamoDB     (managed)        table streams -> Lambda / connector
```

**Listing 1.** Each database exposes the log differently, which is the pattern's portability tax — the outbox table shape can stay identical.

> [!warning] Log tailing is at-least-once and operationally invasive
> Checkpoint restarts republish committed changes, so consumers dedup regardless of the "accurate log" framing; logical decoding holds replication slots — an abandoned slot keeps WAL piling up until the database runs out of disk; and reader versions must track database upgrades. Treat the tailing infrastructure as a production-critical component, not a plugin.

> [!tip] Interview answer
> Transaction log tailing publishes integration events by reading the database's transaction log — WAL in PostgreSQL, binlog in MySQL — usually via Kafka Connect: no polling queries, commit-latency delivery, and an ordered, accurate stream. The trade-offs: database-specific tooling, replication-slot and checkpoint operations to run, and at-least-once semantics that still require consumer dedup.
