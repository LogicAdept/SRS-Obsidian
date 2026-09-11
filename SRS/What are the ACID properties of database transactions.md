<!--
reps: 0
priority: 0
-->
#Databases/Transactions #SRS

# What are the ACID properties of database transactions

> [!abstract] Short answer
> **Atomicity — all or nothing; Consistency — from one valid state to another; Isolation — concurrent executions do not see each other's partial work (per level); Durability — committed changes survive crashes.** ACID is the contract a transactional DBMS makes for every unit of work.

## Each letter, mechanically

**Atomicity** is implemented with an undo path: PostgreSQL writes changes as new row versions and marks aborted transactions' versions dead (later cleaned by vacuum); InnoDB keeps undo logs and rolls back by applying them. **Consistency** in the ACID sense means the database's declared rules — constraints, foreign keys, triggers, data types — hold when the transaction commits; the DBMS enforces the declared part, while the application owns business invariants like "balance may not go below the overdraft limit" unless those are expressed as CHECK constraints. **Isolation** is graded: the SQL standard defines levels from READ UNCOMMITTED to SERIALIZABLE, and each level trades which anomalies are possible against how much concurrency survives — the full ladder in [[What is database transaction isolation]]. **Durability** is the write-ahead log: the log record must reach stable storage (fsync) before the commit is acknowledged; PostgreSQL's `synchronous_commit` and InnoDB's `innodb_flush_log_at_trx_commit` control that handshake, and MySQL's ACID guide lists the doublewrite buffer and binlog sync as the other durability-critical knobs.

```d2
direction: right
a: "Atomicity\nundo log / row versions\nall or nothing" {
  width: 220
  height: 100
  style.fill: "#e3f2fd"
}
c: "Consistency\nconstraints hold at commit" {
  width: 240
  height: 100
  style.fill: "#fff3e0"
}
i: "Isolation\nsnapshots / locks\nper level" {
  width: 210
  height: 100
  style.fill: "#e8f5e9"
}
d: "Durability\nWAL fsync before ack" {
  width: 220
  height: 100
  style.fill: "#ffebee"
}
```

**Fig. 1.** Four independent guarantees with different mechanisms behind them — undo for A, constraint checking for C, MVCC/locking for I, write-ahead logging for D.

## Why the contract matters to application code

ACID is what lets a service write three tables in one method and stop worrying about a crash in the middle — the DBMS finishes or erases all three. It is also the dividing line from most NoSQL stores, which commonly trade full multi-row ACID for horizontal scale and instead offer single-document atomicity or tunable consistency, per [[How do NoSQL databases scale compared with SQL databases]]. MongoDB closed part of the gap by adding multi-document transactions, but the default design remains application-level, per [[How do you use multi-document transactions in Spring Data MongoDB]].

> [!warning] "C" is not the DBMS vouching for your business rules
> A transaction that commits `balance = -1000` on an account without a CHECK constraint is perfectly ACID-compliant: atomic, isolated, durable — and violates your business. Consistency means the declared schema rules held, nothing more. Interviewers probe exactly this: name the trap of assuming the DBMS enforces invariants it was never told about, and put money-critical ones into constraints — see [[Can the same primary key value appear in two rows of one table]] for a key-integrity example.

Drill the individual properties next: [[What is atomicity in ACID transactions]], and the isolation ladder in [[What is database transaction isolation]].

> [!tip] Interview answer
> Atomicity: a transaction applies fully or not at all, via undo logs or row versions. Consistency: declared rules — constraints, keys — hold at commit. Isolation: concurrent transactions are separated to the level's degree, from READ UNCOMMITTED to SERIALIZABLE. Durability: commits survive crashes because the WAL is fsynced before the ack. Together they make multi-step changes safe to write.
