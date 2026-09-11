<!--
reps: 0
priority: 0
-->
#Databases/Replication #SRS

# What is Master-Slave

> [!abstract] Short answer
> **Master-slave replication is the topology where one node (the master/primary) accepts all writes and streams its change log to replicas (slaves) that apply the same changes read-only.** It buys read scaling and a hot failover target at the price of replication lag on replicas and a single write bottleneck on the master. Modern terminology says primary-replica; PostgreSQL documentation uses primary and standby.

## The mechanics, per engine

Every mainstream engine implements the same contract. **MySQL:** the primary records committed events in its binary log; replica threads pull the binlog (I/O thread into the relay log, SQL thread to apply) — statement, row-based, or mixed formats, with GTIDs making replica position tracking and failover clean, and semi-sync optionally making the primary wait for one replica's ack. **PostgreSQL:** the standby receives WAL records — historically by shipping 16 MB WAL files, today by streaming replication over a TCP connection from wal sender to wal receiver; a standby applying received WAL continuously is a *warm standby*, and one also answering read-only queries is a *hot standby*; promotion (`pg_ctl promote`) turns the standby into a primary. Log shipping is asynchronous after commit, so a small window of recent commits can be lost if the primary dies — synchronous replication or MySQL's semisync narrows it at write-latency cost.

```d2
direction: right
m: "Master / primary\naccepts ALL writes" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
r1: "Replica 1\nreads only" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
r2: "Replica 2\nreads only" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
m -> r1: "WAL / binlog stream"
m -> r2: "WAL / binlog stream"
```

**Fig. 1.** One write path, many read paths: replicas replay the primary's change log and serve reads; nothing else may write.

What it buys: read scale-out (route reports and reads to replicas), a standby for HA failover, and backups taken from a replica without touching production. What it costs: **replication lag** — replicas trail the primary, so read-your-writes breaks unless the app pins causally-dependent reads to the primary or waits for lag to close; and the write ceiling of one node, which is why heavy horizontal write scaling moves to sharding — the boundary case in [[What is the difference between database replication and sharding]].

> [!warning] A replica is eventually consistent, and failover can lose tail commits
> Reading a replica answers with the state as of its last applied transaction — a report that reads a replica seconds after a commit may miss it; a user who just wrote may not read their own write from a lagging replica. And with asynchronous replication, promoting a lagging standby after primary death discards transactions the primary never shipped — the data-loss window every HA design must consciously size (sync/semisync vs write latency). Another classic trap: reads routed to replicas under an SLA built for the primary — decide per query, not per hope.

The lag-aware monitoring view: [[How do you monitor database health and load]]; the family split between copies and slices: [[What is the difference between database replication and sharding]]; a warehouse-style application of the same stream: [[How do you ingest Kafka into ClickHouse]].

> [!tip] Interview answer
> Master-slave — today primary-replica — is one node taking writes and streaming its change log to read-only replicas: MySQL ships the binlog, PostgreSQL streams WAL. It scales reads and gives a failover target, while replicas lag and the master caps write throughput. Synchronous or semi-sync modes shrink the tail-loss window on failover at the price of write latency.
