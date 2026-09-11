<!--
reps: 0
priority: 0
-->
#Databases #Observability #SRS

# How do you monitor database health and load

> [!abstract] Short answer
> **Watch four signal groups: query throughput and latency, connection and lock saturation, cache/IO efficiency, and replication or WAL lag — from the DBMS's own statistics views plus OS metrics.** In PostgreSQL that means pg_stat_activity, pg_stat_database, pg_stat_statements and pg_stat_replication; in MySQL, Performance Schema and the slow query log.

## The signal groups and where they live

**Active work.** `pg_stat_activity` shows one row per server process with its state and current query — it answers "what is running right now and what is it waiting on" (idle, running, waiting on a lock). MySQL's `performance_schema.threads` and `data_lock_waits` give the same picture. **Load over time.** `pg_stat_database` tracks commits, rollbacks, blocks read and hit per database — block hit ratio falling means the buffer cache stopped absorbing reads. `pg_stat_io` (PostgreSQL 16+) adds IO per backend type and context.

**Query cost.** The slow query log with `long_query_time` is MySQL's baseline; PostgreSQL prefers the `pg_stat_statements` extension, which aggregates normalized statements with execution counts, total and mean time, and rows — the fastest route to "top ten expensive queries this week". **Saturation.** Connection counts against `max_connections`, lock waits (pg_locks joined to pg_stat_activity; InnoDB `SHOW ENGINE INNODB STATUS`), disk latency and free space. Disk-full is still the classic silent killer: WAL that cannot be written halts a cluster completely. **Replication.** `pg_stat_replication` exposes the replay lag per standby; replication lag minutes behind means failover will lose data and replicas serve stale reads.

```d2
direction: right
views: "DBMS stats views\npg_stat_activity · pg_stat_database\npg_stat_statements · pg_stat_replication" {
  width: 380
  height: 120
  style.fill: "#e3f2fd"
}
collector: "Collector / exporter\n(postgres_exporter, PMM, CloudWatch)" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
dash: "Dashboards + alerts\nlatency p95 · connections · disk\nreplication lag · cache hit" {
  width: 300
  height: 120
  style.fill: "#e8f5e9"
}
views -> collector: "SQL scrape"
collector -> dash
```

**Fig. 1.** The DBMS already measures itself; monitoring chains those statistics into a time series with alerts, rather than polling by hand during an incident.

## What to alert on, not just chart

Chart everything, alert on thresholds that page someone: p95 query latency regression, connection pool exhaustion, replication lag beyond the failover budget, disk above 80%, long-running `idle in transaction` sessions (they hold vacuum and locks back), and vacuum/checkpoint backpressure. Every alert needs a runbook action — kill the offending query, add a replica, extend disk — otherwise it trains people to ignore pages.

> [!warning] A healthy-looking cache hit ratio hides a broken query
> 99% buffer hits and green CPU can coexist with one sequential scan over 100M rows that runs every minute. Aggregate stats say "system fine"; per-query stats say "this query regressed after the plan flipped". That is why `pg_stat_statements`/slow-log review is a routine, not an emergency tool — and why stale statistics deserve their own check after bulk loads, per [[How do you read EXPLAIN ANALYZE in PostgreSQL]].

Tie the numbers to the debugger's loop in [[How do you systematically diagnose a slow SQL query]], and to engine-specific views in [[How do you verify a ClickHouse index is used]].

> [!tip] Interview answer
> I monitor in four groups: current activity and waits (pg_stat_activity, Performance Schema), throughput and cost (pg_stat_statements or the slow query log), saturation (connections, locks, disk, IO), and replication lag. The DBMS exposes all of it; the job is scraping it into time series and alerting on the few thresholds that mean action — latency regressions, pool exhaustion, disk, lag, and idle-in-transaction buildup.
