<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What should you check first when PostgreSQL is slow?

> [!abstract] Short answer
> Triage order: (1) pg_stat_activity — who is running, what are they waiting on, any idle-in-transaction elders; (2) lock waits — wait_event Lock plus the pg_locks blocking chain; (3) pg_stat_statements — is it one query shape or everything; (4) system resources — CPU, I/O wait, disk latency; (5) vacuum and bloat state. The point is to separate "one bad query" from "everyone is blocked" from "the box is saturated" before touching anything.

## The first five minutes

```sql
-- 1. current activity, oldest first
SELECT pid, state, wait_event_type, wait_event,
       now() - xact_start AS tx_age, left(query, 50) AS q
FROM pg_stat_activity WHERE state <> 'idle'
ORDER BY xact_start NULLS LAST;

-- 2. workload ranking (is it one query?)
SELECT calls, total_exec_time, query FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 5;
```

**Listing 1.** Two queries answer most of "why is it slow right now": blocked or busy, one offender or many ([[How would you explain pg_stat_activity pg_stat_statements]]).

```d2
q1: "Activity:\nLock waits? idle in transaction?" {width: 330; height: 80}
q2: "Lock chain via pg_locks\nkill/rollback the blocker" {width: 320; height: 80}
q3: "Statements:\none shape dominates?" {width: 310; height: 80}
q4: "Tune that query\n(EXPLAIN ANALYZE loop)" {width: 300; height: 70}
q5: "System: CPU, I/O, checkpoints,\nautovacuum storms" {width: 330; height: 80}
q1 -> q2
q1 -> q3 -> q4
q3 -> q5
```

**Fig. 1.** The triage tree: contention first, workload second, infrastructure third.

## Reading the signals

- Many sessions in `wait_event_type = Lock` with one blocker — a lock queue, not a query problem ([[How does PostgreSQL handle locks and deadlocks]]).
- Everything active, wait_event IO, high disk latency — I/O saturation: checkpoints ([[What is a checkpoint in PostgreSQL]]), autovacuum storms, or cold cache pressure ([[What are shared_buffers and work_mem in PostgreSQL]]).
- One fingerprint owning total_exec_time — go into the query ([[How do you debug a slow PostgreSQL query]]).
- Nothing active but complaints — look at connection queueing: max_connections, pooler saturation ([[Why use pgBouncer with PostgreSQL]]).

This card is the triage layer above the general SQL method in [[How do you systematically diagnose a slow SQL query]] and the health overview in [[How do you monitor database health and load]].

> [!warning] Do not restart the database first
> A restart clears the evidence: pg_stat_activity empties, statements statistics may survive only if preloaded, lock chains dissolve into mystery. The first five minutes of read-only checks above are what turns "the DB was slow" into a root cause. And in a primary-standby setup, confirm which node you are on before tuning — the lagging replica is a classic false alarm ([[What is the difference between streaming and logical replication in PostgreSQL]]).

> [!tip] Interview answer
> First pg_stat_activity: who is waiting, on what, and is there an ancient idle-in-transaction session. Then pg_locks for the blocking chain, then pg_stat_statements to see whether one query shape dominates, then the OS layer — CPU, I/O, checkpoint and autovacuum storms. Lock contention, single query, or saturated box: three different playbooks, and this order tells you which one you are in.
