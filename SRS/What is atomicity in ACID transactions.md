<!--
reps: 0
priority: 0
-->
#Databases/Transactions #SRS

# What is atomicity in ACID transactions

> [!abstract] Short answer
> **Atomicity is the all-or-nothing guarantee for one transaction: if any statement fails, if the client disconnects, or if the server crashes mid-way, every change the transaction made is undone — a partial transaction can never be observed or survive.** It is the A in ACID, and it is implemented with an undo mechanism, not by "trying harder".

## How a DBMS actually undoes work

Two designs dominate. **Undo logging** (InnoDB): before modifying a row, the old value goes to an undo log; rollback replays the undo records; the same log serves consistent reads for other transactions under MVCC. **Version storage** (PostgreSQL): UPDATE writes a new row version tagged with the creating transaction's id (xmin) and the replaced version's id (xmax); abort simply marks that transaction aborted, and its versions become invisible to every snapshot and dead to vacuum. Either way the commit point is a single log record — before it, the transaction's effects are uncommitted and reversible; after it, they are durable, per [[What are the ACID properties of database transactions]].

Crash recovery is where atomicity proves itself: after a power cut the server replays its log, finds transactions with no commit record, and undoes them with the same machinery. Clients cannot even tell a crash from a rollback.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- applied, uncommitted
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- fails: id does not exist
ROLLBACK;  -- the first update is undone; balance of id=1 unchanged
```

**Listing 1.** A failing statement inside the unit triggers full undo of the earlier statement — half a transfer is never stored.

Atomicity also defines what the application may assume at the failure boundary: after a rollback error, the session's writes are gone and the code must either retry the whole unit or abandon it — inventing "compensation" by hand-issuing inverse UPDATEs is a smell that the work was never wrapped in one transaction to begin with. The flip side of the same guarantee is what breaks when it is absent: see [[What problems can missing database transactions cause]].

```d2
direction: right
t: "Transaction\nUPDATE A; UPDATE B" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
ok: "COMMIT\nboth durable" {
  width: 180
  height: 80
  style.fill: "#e8f5e9"
}
undo: "Any failure\nundo log / dead versions\nneither applied" {
  width: 260
  height: 100
  style.fill: "#ffebee"
}
t -> ok
t -> undo: "error / crash"
```

**Fig. 1.** Exactly two outcomes exist. The undo path is a first-class mechanism — undo logs or dead row versions — not an exception handler in the application.

> [!warning] Atomicity covers the transaction, not the surrounding business saga
> A committed transaction cannot be rolled back by the DBMS afterwards. If unit-of-work 2 fails after unit-of-work 1 committed — booking the payment but failing to reserve stock — that is a distributed-workflow problem, solved with outbox patterns and compensations, not with rollback. Blurring "transaction" with "business operation" is the classic architecture trap; keep the DBMS guarantee scoped to the multi-statement unit, and compare with multi-document transactions in [[How do you use multi-document transactions in Spring Data MongoDB]].

The isolation sibling of the same boundary: [[What problems appear when database transactions run in parallel]].

> [!tip] Interview answer
> Atomicity says a transaction is indivisible: any error, disconnect, or crash inside it undoes all its changes, so a partial unit is never visible or durable. Mechanically it is undo logs (InnoDB) or dead row versions plus vacuum (PostgreSQL); the commit record in the WAL is the point of no return between the two outcomes.
