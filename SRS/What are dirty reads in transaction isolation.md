<!--
reps: 0
priority: 0
-->
#Databases/Transactions #Problems/Persistence #SRS

# What are dirty reads in transaction isolation

> [!abstract] Short answer
> **A dirty read is reading data that another transaction has written but not committed — data that may still be rolled back.** If the writer aborts, the reader has made decisions based on state that never existed; the READ COMMITTED level exists to forbid exactly this.

## The two-session anatomy

Session A moves 100 between accounts inside an open transaction. Session B, before A commits, reads the new balance and approves a payment against it. A rolls back — the transfer never happened — but B's decision is already made. Every result B derived is contaminated: not because of a bug in either query, but because B read the intermediate, uncommitted version. The SQL standard calls this the first phenomenon its isolation ladder must forbid: from READ COMMITTED upward, a statement may only see data committed before the statement (or transaction, at higher levels) began.

Engines reach that guarantee differently. PostgreSQL's MVCC gives each statement a snapshot of committed data, so dirty reads are impossible at any requested level — even READ UNCOMMITTED behaves as READ COMMITTED. InnoDB's consistent nonlocking reads do the same via its read view and undo log. Implementing a genuine READ UNCOMMITTED — which InnoDB defines as possibly reading an earlier row version, "also called a dirty read" — is essentially obsolete in mainstream engines.

```d2
direction: right
w: "Session A\nUPDATE balance\nNOT committed yet" {
  width: 230
  height: 100
  style.fill: "#fff3e0"
}
r: "Session B\nreads the new balance\nand acts on it" {
  width: 240
  height: 100
  style.fill: "#e3f2fd"
}
bad: "A: ROLLBACK\nB acted on data that never existed" {
  width: 330
  height: 90
  style.fill: "#ffebee"
}
w -> r: "uncommitted read"
w -> bad
```

**Fig. 1.** The dirty-read triangle: the reader's decision survives the writer's rollback, which is why the guarantee "read only committed data" is the floor of sane isolation.

> [!warning] Dirty read is not "wrong value read" — it is uncommitted value read
> A non-repeatable read or a phantom shows *committed* data that changed; only a dirty read exposes never-committed data. Mixing these up in an interview answer collapses the level ladder. Related but distinct: a dirty *write* — overwriting another transaction's uncommitted change — is forbidden even below READ COMMITTED by engines that lock written rows; and reading via a *stale MVCC snapshot* is not dirty, it is repeatable-read behavior.

Where the level ladder puts this anomaly: [[What is database transaction isolation]]; the sibling anomalies in [[What problems appear when database transactions run in parallel]] and [[What are phantom reads under weak isolation]]; the SQL-side drill with all three in [[How do you handle transaction isolation anomalies]].

> [!tip] Interview answer
> A dirty read means reading another transaction's uncommitted changes — data that a rollback will erase. It is the first anomaly the isolation ladder forbids: from READ COMMITTED up, statements see only committed data. PostgreSQL and InnoDB both make dirty reads effectively impossible via MVCC snapshots; the danger lives in the concept and in engines or settings that genuinely expose intermediate versions.
