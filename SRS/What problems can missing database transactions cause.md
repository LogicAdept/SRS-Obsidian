<!--
reps: 0
priority: 0
-->
#Databases/Transactions #Problems/Persistence #SRS

# What problems can missing database transactions cause

> [!abstract] Short answer
> **Without a transaction, every statement commits on its own — so a failure between statements leaves the database persistently half-updated: money debited without the credit, an order without its lines, a foreign key pointing nowhere.** You also lose batch performance and the clean rollback boundary, because each statement is its own durability point.

## The failure modes, concretely

**Partial application on error.** The debit UPDATE commits, the credit INSERT throws (constraint violation, connection drop, process kill) — and there is no mechanism to undo the debit: each statement was already committed and durable. What remains is inconsistent state that every later reader trusts. **Inconsistent intermediate visibility.** Even without failures, other sessions see the debit before the credit — reports, caching layers, and replicas (reading the binlog/WAL stream) happily consume the broken intermediate state. **No recovery point.** With autocommit on every statement, a retry of the failed step may double-apply the succeeded ones; idempotency has to be hand-rolled where a single transaction would have made "all or nothing" free.

```sql
-- autocommit on: three independent commits
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- committed
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- server dies here
-- id=1 lost 100; nobody received it; no rollback is possible anymore
```

**Listing 1.** The same transfer without a transaction: the crash boundary falls between two independent commits, and the money is gone until manual reconciliation.

Beyond correctness, batching matters: wrapping a thousand inserts in one transaction lets the engine fsync the log once at commit, while autocommit per row forces a durability round trip each row — bulk loads drop from minutes to seconds when grouped, per the batch-insert drill [[How do you organize batch inserts for many rows]].

```d2
direction: right
with: "With transaction\nBEGIN; s1; s2; COMMIT\ncrash between s1 and s2\n-> nothing applied" {
  width: 300
  height: 120
  style.fill: "#e8f5e9"
}
without: "Without transaction\ns1 commits, s2 commits\ncrash between them\n-> half-state persists" {
  width: 300
  height: 120
  style.fill: "#ffebee"
}
```

**Fig. 1.** Same two statements, same crash point: the transaction erases the accident, autocommit makes it permanent.

> [!warning] Frameworks default to per-statement transactions — silence is not safety
> Spring without `@Transactional`, a raw JdbcTemplate writing three statements, or an ORM flushing per statement all execute autocommit-style even though the code "looks" atomic. The failure shows up only on real errors, which is why it surfaces in production. Multi-statement invariants must be explicitly wrapped; where the unit genuinely spans services, a transaction cannot cover it — that is the outbox/saga territory, not an excuse to hold a giant DB transaction open.

The positive definition of the guarantee: [[What is transaction]]; the price of parallel execution when transactions *do* exist: [[What problems appear when database transactions run in parallel]].

> [!tip] Interview answer
> Without transactions each statement commits alone, so a failure between statements leaves permanent half-states — debit without credit, parent without children — and other sessions read the broken intermediate. You also lose the single-fsync batching and exact rollback. Any multi-statement invariant must be wrapped explicitly; cross-service units need outbox or saga patterns instead of a fat database transaction.
