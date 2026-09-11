<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# How do you debug a slow PostgreSQL query?

> [!abstract] Short answer
> Reproduce with EXPLAIN (ANALYZE, BUFFERS), then in order: check whether rows estimates match reality (statistics problem), whether the expected index is actually used with a real Index Cond (plan problem), and where the buffers go (I/O or spill problem). Add the context: locks from pg_stat_activity, vacuum state for index-only plans, and the query's share of the workload from pg_stat_statements.

## The procedure

```sql
-- 1. What is the real plan and cost?
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;

-- 2. Is the estimate sane at each node? (rows vs actual)
-- 3. Index Cond present? Filter removing thousands? (see plan counters)
-- 4. Spills? temp read/written in BUFFERS
-- 5. Blocking? who else holds locks on these rows/pages
SELECT pid, wait_event_type, state FROM pg_stat_activity
WHERE state <> 'idle';
```

**Listing 1.** The five steps in one breath; each failure mode has a distinct signature ([[How do you read EXPLAIN ANALYZE in PostgreSQL]]).

```d2
slow: "Slow query" {width: 180; height: 60}
est: "Estimates wrong?" {width: 240; height: 70}
idx: "Index disqualified?" {width: 250; height: 70}
io: "Buffers/temp heavy?" {width: 250; height: 70}
an: "ANALYZE + CREATE STATISTICS" {width: 300; height: 70}
fixidx: "Fix predicate / index" {width: 290; height: 70}
mem: "work_mem / covering index" {width: 290; height: 70}
slow -> est -> an
slow -> idx -> fixidx
slow -> io -> mem
```

**Fig. 1.** Three diagnosis branches; the plan counters tell you which branch you are on.

## The surrounding systems

- **Workload rank**: is this query even worth tuning? pg_stat_statements total time ([[What is pg_stat_statements]]); the general method overlaps with [[How do you systematically diagnose a slow SQL query]].
- **Freshness**: autovacuum state and Heap Fetches for index-only plans ([[What is autovacuum in PostgreSQL]], [[What is Heap Fetches in an EXPLAIN plan]]).
- **Contention**: wait_event = Lock plus pg_locks blocking chains; long transactions ([[Why do long-running transactions hurt PostgreSQL]], [[How does PostgreSQL handle locks and deadlocks]]).
- **Config**: shared_buffers/work_mem sizing ([[What are shared_buffers and work_mem in PostgreSQL]]).

## Common endings

Most slow-query stories end in one of: stale statistics after bulk load; a predicate that silently disqualifies the index; a sort spill on work_mem; or lock waits that make an otherwise fast plan look slow. The toolset above separates them in minutes.

> [!warning] EXPLAIN without ANALYZE is a hypothesis, not a diagnosis
> Estimated costs come from samples; the real plan may differ after execution starts. Worse, caching changes everything between runs — a cold run reads disk, a warm run does not. Measure at least twice and read BUFFERS, and never tune based on the estimate alone ([[How do stale statistics hurt a query plan]]).

> [!tip] Interview answer
> I reproduce with EXPLAIN ANALYZE BUFFERS: check row misestimates at each node, confirm Index Cond versus Filter waste, and look for temp spills or cold buffer reads. Around the plan I check pg_stat_activity for lock waits and transaction age, and pg_stat_statements for the query's workload share. Fixes usually are ANALYZE, an index the predicate can use, or memory/lock remediation.
