<!--
reps: 0
priority: 0
-->
#Databases/Transactions #SRS

# What is transaction

> [!abstract] Short answer
> **A transaction is a group of database operations that executes as one indivisible unit: either every operation in it is applied and durably committed, or none of them is.** It is the unit of work that turns a multi-step change (debit one account, credit another) into something that cannot be observed half-done.

## The boundaries and what they guarantee

A transaction spans from its opening statement (`BEGIN` / `START TRANSACTION`, or implicitly with the first statement under MySQL's autocommit) to `COMMIT` or `ROLLBACK`. The DBMS guarantees the ACID properties over that span: **atomicity** — a crash between the two UPDATEs rolls both back, so money cannot vanish; **consistency** — constraints and triggers hold at commit time; **isolation** — concurrent transactions do not observe your intermediate states, at least to the degree the isolation level promises; **durability** — once COMMIT returns, the change survives restart, because the write-ahead log (PostgreSQL's WAL, InnoDB's redo log) was fsynced before the commit acknowledged.

Every statement inside the transaction reads and writes through that unit: changes made inside it are visible to its own subsequent statements, but invisible to other transactions until commit. That visibility boundary is what makes "transfer 100" meaningful — without it, a concurrent report could see the debit without the credit.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;   -- or ROLLBACK; and both updates disappear
```

**Listing 1.** The transfer idiom: both updates commit together or neither does.

Transactions are also the natural **error-recovery boundary**: on any failure the code calls rollback and the database is exactly as it was, instead of the application hand-un-doing half a workflow. Nested units are expressed with savepoints (`SAVEPOINT sp; ... ROLLBACK TO sp`) rather than nested BEGINs, and frameworks layer Spring's `@Transactional` or Quarkus transactions over the same primitives.

```d2
direction: right
begin: "BEGIN\nunit of work opens" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
ops: "UPDATE, INSERT, ...\nvisible only inside" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
commit: "COMMIT\nWAL fsynced, visible to all" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
rb: "ROLLBACK\nnothing happened" {
  width: 210
  height: 80
  style.fill: "#ffebee"
}
begin -> ops
ops -> commit
ops -> rb: "any error"
```

**Fig. 1.** All intermediate work is private until commit; the two exits of a transaction are "everything applied" or "nothing applied".

> [!warning] A transaction is not a lock and not a batch primitive
> Keeping a transaction open "to hold rows" or "to process a big file" blocks vacuum (PostgreSQL), holds gap locks (InnoDB), bloats the log, and starves connection pools. The transaction should cover exactly the multi-step invariant — commit, then do the next unit. Long-running background work belongs in chunks, per the same reasoning that makes missing transactions dangerous in [[What problems can missing database transactions cause]].

Where the properties come from in detail: [[What are the ACID properties of database transactions]], and the concurrency dimension in [[What is database transaction isolation]].

> [!tip] Interview answer
> A transaction is the unit of work between BEGIN and COMMIT/ROLLBACK that the DBMS treats as indivisible: all of its changes apply and become durable, or none do. It gives ACID semantics over multi-step invariants like money transfers, makes error recovery exact via rollback, and is visible to other sessions only at commit.
