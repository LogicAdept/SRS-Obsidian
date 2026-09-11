<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# How would you explain pg_stat_activity and pg_stat_statements?

> [!abstract] Short answer
> pg_stat_activity is the live webcam: one row per server process, showing what each backend is doing right now — state, current query, wait event, transaction start. pg_stat_statements is the DVR: cumulative per-query-shape statistics since the last reset. You watch activity to catch incidents; you read statements to find the chronic workload.

## The split

| | pg_stat_activity | pg_stat_statements |
|---|---|---|
| Granularity | one row per backend, current moment | one row per query fingerprint, cumulative |
| Answer | who is stuck on what right now | which query shapes cost the most |
| Setup | always available | preload + CREATE EXTENSION |
| Reset | none (it is a snapshot) | pg_stat_statements_reset() |

```d2
act: "pg_stat_activity\nstate, wait_event, query,\nxact_start, backend_xid" {width: 330; height: 100}
st: "pg_stat_statements\ncalls, total/mean time, rows,\nblocks read/written" {width: 330; height: 100}
inc: "Incident\n'everything is slow now'" {width: 300; height: 70}
trend: "Triage\n'what hurts in general'" {width: 300; height: 70}
act -> inc
st -> trend
```

**Fig. 1.** Two different questions: present state versus aggregate history.

## What each column buys you

- In activity: `state` = active / idle in transaction / idle; `wait_event_type` and `wait_event` (Lock, IO, LWLock...) name the block; `xact_start` age finds the horizon-holding transaction ([[Why do long-running transactions hurt PostgreSQL]]); join `pg_locks` for the blocking chain ([[How does PostgreSQL handle locks and deadlocks]]).
- In statements: rank by `total_exec_time`, inspect `mean_exec_time`, `rows`, `shared_blks_read`, `temp_blks_written` ([[What is pg_stat_statements]]).

```sql
SELECT pid, state, wait_event_type, now() - xact_start AS age, left(query, 60)
FROM pg_stat_activity
WHERE state <> 'idle' ORDER BY age DESC;
```

**Listing 1.** The standard "what is happening right now" query — oldest transactions first.

> [!warning] Activity shows idle backends too — read the state column
> "100 rows in pg_stat_activity" is not "100 busy queries": most are idle. The dangerous states are `idle in transaction` (holds a snapshot) and long `active` with `wait_event_type = Lock`. And statistics in statements-view rows lag up to about a second before flush — for the current query text, activity is always current ([[How do you debug a slow PostgreSQL query]]).

> [!tip] Interview answer
> pg_stat_activity is the per-process live snapshot — state, wait event, current query, transaction age — for incidents and lock chains. pg_stat_statements is the cumulative per-fingerprint workload profile for finding chronic offenders. Incident: activity plus pg_locks. Capacity work: statements ranked by total time. Together they cover present and history.
