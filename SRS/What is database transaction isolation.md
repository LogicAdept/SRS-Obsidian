<!--
reps: 0
priority: 0
-->
#Databases/Transactions #SRS

# What is database transaction isolation

> [!abstract] Short answer
> **Isolation defines which effects of concurrent transactions a transaction is allowed to see; the SQL standard grades it in four levels — READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE — each excluding a defined set of anomalies.** Higher isolation means fewer anomalies and less concurrency; the level is per-transaction and configurable.

## The ladder and what each rung forbids

The standard defines the levels by the phenomena they must prevent. **READ UNCOMMITTED** permits dirty reads — seeing uncommitted data. **READ COMMITTED** forbids dirty reads: each statement sees only committed data as of the statement start, so two statements in one transaction may see different results. **REPEATABLE READ** additionally forbids non-repeatable reads: all reads in the transaction see one snapshot taken at its start, though new rows matching a predicate may still appear (phantoms, in the standard's minimum guarantee). **SERIALIZABLE** forbids every anomaly including phantoms and serialization anomalies: committed results must be consistent with some one-at-a-time execution order.

Implementations overshoot the minimums. PostgreSQL maps READ UNCOMMITTED to READ COMMITTED (MVCC snapshots make dirty reads impossible) and its REPEATABLE READ — snapshot isolation — already prevents phantoms. InnoDB's default is REPEATABLE READ with gap and next-key locks blocking phantom inserts into scanned ranges; its READ COMMITTED takes a fresh snapshot per read and disables gap locking (except foreign-key and duplicate checks), which is exactly why phantoms become possible there. InnoDB SERIALIZABLE converts plain SELECTs to `SELECT ... FOR SHARE`.

```d2
direction: right
ru: "READ UNCOMMITTED\ndirty reads possible" {
  width: 230
  height: 90
  style.fill: "#ffebee"
}
rc: "READ COMMITTED\nno dirty; fresh snapshot per statement\n(PostgreSQL default)" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
rr: "REPEATABLE READ\nstable snapshot; InnoDB default\n(PG: no phantoms either)" {
  width: 310
  height: 100
  style.fill: "#e3f2fd"
}
ser: "SERIALIZABLE\none-at-a-time semantics" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
ru -> rc -> rr -> ser
```

**Fig. 1.** The standard's ladder with the vendor quirks annotated: PostgreSQL's default is READ COMMITTED, InnoDB's is REPEATABLE READ, and PostgreSQL's RR is stronger than the standard demands.

Choosing a level is a workload decision: reporting and dashboards usually live happily at READ COMMITTED; financial batch logic wants REPEATABLE READ or SERIALIZABLE plus retry loops. In PostgreSQL and InnoDB the higher levels are optimistic — they do not block readers, but a conflicting update fails with a serialization error the application must retry.

> [!warning] The defaults differ per vendor, and "REPEATABLE READ" does not mean the same thing everywhere
> Code that assumes one default breaks on the other engine: PostgreSQL defaults to READ COMMITTED, MySQL/InnoDB to REPEATABLE READ. And the standard's REPEATABLE READ permits phantoms while PostgreSQL's does not. Always state the engine and the level together — "REPEATABLE READ in InnoDB" and "REPEATABLE READ in PostgreSQL" are related, not identical, guarantees, and the anomalies in [[What problems appear when database transactions run in parallel]] shift accordingly.

Read the anomaly catalog in [[What are dirty reads in transaction isolation]] and [[What are phantom reads under weak isolation]], and the deep dive on the filled SQL-side drill [[How do you handle transaction isolation anomalies]].

> [!tip] Interview answer
> Isolation is the graded I of ACID: four standard levels, from READ UNCOMMITTED with dirty reads up to SERIALIZABLE with one-at-a-time semantics. Each level forbids a defined anomaly set — dirty, non-repeatable, phantom, serialization anomaly — and engines differ in defaults and strength: PostgreSQL defaults to READ COMMITTED and implements RR as snapshot isolation that already blocks phantoms; InnoDB defaults to REPEATABLE READ with gap locks. Pick the weakest level that keeps your invariants, and retry serialization failures.
