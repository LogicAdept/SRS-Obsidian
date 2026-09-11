<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is change data capture with Kafka?

> [!abstract] Short answer
> Turning a database's row-level changes into events on a topic: a Connect source connector continuously reads the changes — ideally by tailing the database's transaction log, not by polling tables — and publishes each insert, update, and delete as a record. Kafka then distributes the change stream to caches, search indexes, analytics, and other stores ([[What is the Kafka Connector API for]]).

## Query-based versus log-based capture

```d2
direction: down
db: "Database\nredo/WAL/binlog" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
log: "Log-based connector\nreads the transaction log" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
poll: "Polling connector\nqueries updated rows" {
  width: 270
  height: 100
  style.fill: "#fff3e0"
}
kafka: "Kafka topics\none event per row change" {
  width: 270
  height: 90
  style.fill: "#e3f2fd"
}
db -> log -> kafka
db -> poll -> kafka
```

**Fig. 1.** Two capture strategies: the log-based path reads the change stream the database already writes for replication; polling queries the tables and must infer what changed.

Transaction log tailing is the strong form: the database commits a change and the connector reads it from the log (MySQL binlog, Postgres WAL and so on), so capture adds no query load on business tables, sees every change exactly as committed — including those made outside your application — and preserves the commit order ([[How would you explain transaction log tailing for integration]]). Polling is the fallback: incremental queries against timestamp or version columns, simpler to deploy but with query load, missed deletes, and clock-skew hazards — the classic weaknesses the polling-publisher pattern documents ([[How would you explain the polling publisher pattern]]). Log-based connectors are the backbone of CDC with Kafka in practice, and the pattern needs no changes to application code: the database's own durability mechanism becomes the event feed.

## What the events look like and what Kafka adds

The connector emits a record per row change: key = primary key, value = before/after image (with schemas), plus operation type and metadata; deletes naturally become tombstone records when the value is null, which compacted downstream topics handle correctly ([[What is a Kafka tombstone record]]). Kafka then adds what a raw log feed lacks: durable multi-consumer distribution with per-key ordering by primary key, replay for new consumers, and retention independent of the source database's log window ([[What ordering guarantees does Kafka provide for messages]]). Snapshotting makes a new connector usable on existing tables — it reads a consistent initial snapshot into the topic, then switches to streaming the log — so a consumer can rebuild full current state, not only changes from today ([[What is Kafka log compaction]]).

> [!warning] CDC is at-least-once, and the log is not a schema contract
> Restarts and offset translation can re-emit records — deduplication belongs to the consumer or the sink. And the change stream's shape follows the database's internal format, which evolves with the database itself; teams that pipe raw binlog-shaped events to every downstream consumer end up coupling all of them to one database's internals instead of to an application schema.

> [!tip] Interview answer
> CDC with Kafka means streaming a database's row changes into topics: a Connect source connector captures changes, preferably by tailing the transaction log so capture is ordered, complete, and free of query load, with a snapshot for existing rows. Each change becomes a keyed event — deletes become tombstones — and Kafka's replay, retention, and per-key ordering distribute that change stream to every downstream store.

