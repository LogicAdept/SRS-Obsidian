<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SystemDesign/Performance #SRS

# When should you not use ClickHouse?

> [!abstract] Short answer
> Avoid ClickHouse when the workload is OLTP-shaped: many small transactions, single-row point lookups by key, high-rate small updates or deletes, or joins across heavily normalized mutable entities. The official docs name the limitations explicitly: no full-fledged transactions, expensive low-latency modification of inserted data, and a sparse index that is not built to fetch individual rows.

## Consequences of the design

Everything follows from the [[What is the MergeTree engine in ClickHouse]] architecture. A point lookup cannot use a B-tree descent to one row; the [[What is a sparse primary index in ClickHouse]] locates a granule of 8192 rows, so fetching one row still reads and decompresses a whole granule per column. An `UPDATE` is a [[What are mutations in ClickHouse]] that rewrites entire parts asynchronously, and a delete is either another mutation or a lightweight `DELETE FROM` that marks rows by a hidden `_row_exists` column — both far heavier than a row-store's in-place update. There is no multi-statement transaction with row-level locking, so money movement or inventory decrement patterns do not belong here.

```sql
-- OLTP shape: kills ClickHouse
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 7;  -- mutation, async part rewrite
SELECT balance FROM accounts WHERE id = 7;                 -- granule read, not a row fetch
COMMIT;                                                    -- no real MVCC transaction
```

**Listing 1.** The same statements that are routine in PostgreSQL become anti-patterns here; [[What is the difference between PostgreSQL and ClickHouse]] expands on the split.

## Where it still fits despite "not OLTP"

Batch corrections (GDPR erasure of whole users, backfills) are explicitly supported — the limitation is rate and latency, not existence. Long-lived analytical aggregations, event funnels, time-series and log search ([[How do you search logs in ClickHouse]]) are the sweet spot. A hybrid is common: OLTP in PostgreSQL, CDC or Kafka ingestion into ClickHouse — see [[How do you ingest Kafka into ClickHouse]] and [[What is the Kafka to ClickHouse materialized view pattern]].

> [!warning] Popular lie: "ClickHouse cannot UPDATE or DELETE"
> It can — `ALTER TABLE ... UPDATE/DELETE` ([[What are mutations in ClickHouse]]) and lightweight `DELETE FROM` exist. The real rule: these operations are asynchronous, part-rewriting batch jobs, so they fail at high rate and low latency, not at low volume. Word it as a rate limitation, not an existence one, in an interview.

> [!tip] Interview answer
> Don't use ClickHouse when you need OLTP semantics: high-frequency small transactions, per-row updates and deletes, point lookups by key, or strict multi-statement transactions. Its sparse index reads granules, not rows, and its mutations rewrite parts asynchronously. It is an analytics and event-data engine; pair it with a row store rather than replacing one.
