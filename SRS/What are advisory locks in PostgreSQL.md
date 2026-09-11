<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What are advisory locks in PostgreSQL?

> [!abstract] Short answer
> Application-defined locks on arbitrary 64-bit keys (or two ints): the engine enforces mutual exclusion, the application defines what the key means. Two scoping levels — session locks held until explicitly unlocked or disconnect, and transaction locks released at commit or rollback automatically. Faster than flag tables, bloat-free, cleaned up by the server — and completely conventional: nothing forces anyone to honor them.

## The API

```sql
SELECT pg_advisory_lock(42);        -- session level, blocks until free
SELECT pg_advisory_unlock(42);
SELECT pg_try_advisory_lock(42);    -- non-blocking attempt

BEGIN;
SELECT pg_advisory_xact_lock(42);   -- transaction level: auto-released
UPDATE jobs SET state = 'running' WHERE id = 42;
COMMIT;
```

**Listing 1.** Session functions vs xact functions; shared variants (pg_advisory_lock_shared) provide reader-writer semantics.

```d2
key: "Application key\n42 = 'cron compaction job'" {width: 300; height: 70}
sess: "Session lock\nheld until unlock/disconnect" {width: 320; height: 80}
xact: "Transaction lock\nreleased at COMMIT/ROLLBACK" {width: 330; height: 80}
mem: "Shared memory lock table\n(pg_locks shows all)" {width: 320; height: 80}
key -> sess -> mem
key -> xact -> mem
```

**Fig. 1.** Both levels live in the shared lock table visible through pg_locks; neither touches table data.

## What they are used for

- Single-instance cron or migration jobs: every worker tries the same key; one wins.
- Serializing cache refreshes or export pipelines per resource id.
- Emulating pessimistic application-level locking where MVCC's optimistic behavior ([[What is MVCC in PostgreSQL]]) does not fit — the documentation names this as the canonical use.
- Coordinating with SKIP LOCKED queue consumers ([[What is SELECT FOR UPDATE SKIP LOCKED in PostgreSQL]] covers the row-lock alternative when the work itself is rows).

## The mechanics that matter

Locks live in shared memory sized by `max_locks_per_transaction * max_connections` — exhaustion makes the server unable to grant any locks. Session locks stack (each acquire needs a matching unlock). And because they are advisory, code that ignores the convention simply does not block — there is no enforcement at the data level ([[What lock granularities exist in a relational database]] for the engine's own lock families).

> [!warning] Lock ordering inside a query is not guaranteed
> The documentation's own example: `SELECT pg_advisory_lock(id) FROM t WHERE id > x LIMIT 10` can lock more rows than intended because the LIMIT may be applied after the function runs — locking arbitrary rows the app then never unlocks until session end. Wrap the selection in a subquery, or lock one known key per call. Under transaction pooling, session-level locks also outlive the client's logical transaction ([[Why use pgBouncer with PostgreSQL]]).

> [!tip] Interview answer
> Advisory locks are engine-enforced mutexes on application-chosen keys: session-scoped until unlock or disconnect, or transaction-scoped with automatic release. They serialize jobs and resources without touching table data — no bloat, pg_locks-visible, shared-memory bounded. The traps: advisory means no enforcement, LIMIT plus lock functions can over-lock, and session locks leak under poolers.
