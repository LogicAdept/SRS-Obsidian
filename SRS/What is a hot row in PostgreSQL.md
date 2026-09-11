<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is a hot row in PostgreSQL?

> [!abstract] Short answer
> A row that many concurrent transactions try to update at once — a counter, a stock level, a balance, a queue head. The row-level lock serializes them: everyone queues behind the first updater, each wait surfaces as lock waits, and the row's MVCC churn multiplies ([[What is MVCC in PostgreSQL]]). The fixes are architectural (spread the contention), mechanical (SKIP LOCKED, advisory locks, short transactions), or eventual (queue the change).

## Why it hurts

Row locks in PostgreSQL are held to transaction end ([[What are xmin and xmax in PostgreSQL]] — the lock stamps xmax). Under a hot row, each new updater waits on the holder; with Read Committed it then re-evaluates its WHERE on the new version and may update it — under Repeatable Read it gets a serialization error. Latency grows linearly with queue length, and every update writes a new tuple (HOT-eligible only if no indexed column changed — [[What is a HOT update in PostgreSQL]]).

```d2
t1: "TX 1: UPDATE counter" {width: 260; height: 60}
t2: "TX 2: waits on row lock" {width: 280; height: 60}
t3: "TX 3: waits behind TX 2" {width: 280; height: 60}
t4: "TX 4: waits behind TX 3" {width: 280; height: 60}
t1 -> t2 -> t3 -> t4: "queue"
```

**Fig. 1.** The lock chain: throughput of the row is one transaction at a time, by definition.

## The toolbox

```sql
-- 1. do not block: take only what is unlocked (queue consumers)
SELECT id FROM jobs WHERE state = 'new'
ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED;

-- 2. fail fast instead of queueing
UPDATE stock SET qty = qty - 1 WHERE sku = 'A-1' AND qty > 0;

-- 3. serialize at the app level instead of the row
SELECT pg_advisory_xact_lock(9527);

-- 4. break the row apart (sharded counters: 16 slots, sum on read)
UPDATE counters SET n = n + 1 WHERE key = 'views' AND slot = random_slot();
```

**Listing 1.** The standard escapes: skip contention, atomic guard, external mutex, or shard the counter ([[What is SELECT FOR UPDATE SKIP LOCKED in PostgreSQL]], [[What are advisory locks in PostgreSQL]]).

## Diagnosis

pg_stat_activity: many active sessions with wait_event_type = Lock on the same tuples; pg_locks joins the waiters; the slow-query triage ([[What should you check first when PostgreSQL is slow]]) catches it as a lock storm rather than a plan problem.

> [!warning] "Just add an index" does not apply; "just commit faster" only mitigates
> A hot row is a serialization point, not a missing index — the lock is the design. Shorter transactions shrink the window but the queue remains; the real cures remove the shared mutable row (shard, batch, queue) or change who waits (SKIP LOCKED, NOWAIT, advisory coordination). And under transaction pooling, holding row locks across pool handovers multiplies the damage ([[Why do long-running transactions hurt PostgreSQL]]).

> [!tip] Interview answer
> A hot row is one row updated by many transactions — counters, balances, queue heads. Row locks serialize them to transaction end, so latency queues up and MVCC churn grows. Options: atomic guarded updates that fail fast, SKIP LOCKED for consumers, advisory locks for app-level serialization, or sharding the counter into slots and summing on read.
