<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# How would you explain Repeatable Read in PostgreSQL?

> [!abstract] Short answer
> Repeatable Read fixes one snapshot per transaction — taken at the first non-transaction-control statement — so every read in the transaction sees the same data, and PostgreSQL's MVCC implementation additionally prevents phantom reads, which the SQL standard permits at this level. The costs: writes that conflict with concurrent commits fail with a serialization error that the application must retry.

## The snapshot semantics

Read Committed takes a new snapshot per statement; Repeatable Read pins the one from the transaction's first query. Re-reading the same rows returns the same values, and newly committed rows from other transactions stay invisible for the whole transaction — including rows that would match a re-run range query, which is why phantoms cannot appear ([[What is MVCC in PostgreSQL]] for the snapshot machinery).

```sql
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT sum(total) FROM orders WHERE created_at::date = '2026-09-01';  -- snapshot fixed
-- another session inserts more orders for that date and commits
SELECT sum(total) FROM orders WHERE created_at::date = '2026-09-01';  -- same number
COMMIT;
```

**Listing 1.** Both sums read the same frozen snapshot; the concurrent insert never becomes visible here.

## The write contract

If this transaction updates a row that another transaction modified (and committed) after the snapshot was taken, PostgreSQL aborts it:

```
ERROR: could not serialize access due to concurrent update
```

**Listing 2.** The cost of the guarantee: read-then-write patterns must retry. This is the documented behavior — first updater wins, later conflicting writers fail rather than silently overwrite ([[How do you handle transaction isolation anomalies]] for the retry discipline).

```d2
rc: "Read Committed\nsnapshot per statement\nsees latest commits" {width: 320; height: 90}
rr: "Repeatable Read\nsnapshot fixed at first statement\nno phantoms; conflicts abort" {width: 340; height: 100}
si: "Serializable\nSSI on top: read-write\ndependency detection" {width: 320; height: 100}
rc -> rr -> si: "stronger guarantees"
```

**Fig. 1.** Repeatable Read sits in the middle: consistency of reads without Serializable's full anomaly detection ([[What is PostgreSQL Serializable Snapshot Isolation]]).

## Where it fits

- Reporting and exports that must be internally consistent across many statements, without paying Serializable's conflict rates.
- Long read-modify-write cycles where re-reading changed data mid-way would corrupt the business decision — RR converts that hazard into an explicit retry.
- The phantom-read detail is the interview separator: the standard says phantoms are allowed at RR; PostgreSQL forbids them ([[How does Repeatable Read prevent phantom reads in PostgreSQL]] has the mechanism — snapshot visibility of the range, not locks).

> [!warning] Repeatable Read does not make writes safe by magic
> It detects the conflict you hit directly (row was modified), but a business invariant spanning several rows ("no more than 3 active subscriptions per user") can still be violated by two RR transactions that read disjoint rows and write different rows — RR is not serializable. Either add explicit locking or step up to Serializable ([[What is PostgreSQL Serializable Snapshot Isolation]] / [[What is SELECT FOR UPDATE SKIP LOCKED in PostgreSQL]]).

> [!tip] Interview answer
> Repeatable Read pins one snapshot for the whole transaction — taken at the first real statement — so re-reads are stable and, in PostgreSQL, phantoms are also impossible because visibility is snapshot-based. The price is explicit: writing a row changed since your snapshot fails with a serialization error, so the application retries. Stronger than the standard requires, weaker than Serializable's full anomaly detection.
