<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Partitioning #SRS

# What is TTL in ClickHouse?

> [!abstract] Short answer
> TTL rules attached to columns or the table say what happens when data ages out: rows get deleted (`TTL expr DELETE`), columns zeroed and then dropped, data recompressed, aggregated, or moved between storage tiers (`TO DISK`/`TO VOLUME`). Rules are applied during background merges (or forced with `MATERIALIZE TTL`), so expiry is eventually-consistent, not instant.

## The rule set

A column-level `TTL timestamp + INTERVAL 1 MONTH` replaces the column's value with the type default after the interval, and drops the column from disk once a part's values are all expired; a table-level `TTL expr DELETE` removes whole rows; `TTL ... RECOMPRESS codec(...)` re-compresses aged data; `TTL ... TO DISK "volume"/TO VOLUME "policy"` moves parts between storage policies (SSD to HDD tiering); and aggregate rollups via `TTL ... GROUP BY` fold old detail rows into summaries. Expressions must be on Date/DateTime. Rules are declared at CREATE and changed with `ALTER TABLE ... MODIFY TTL`; enforcement happens in merges — a merge rewrites parts and drops what expired — with `ttl_only_drop_parts = 1` allowing whole-partition drops without rewriting when all rows in a part expire together.

```sql
CREATE TABLE events
(
    ts DateTime,
    payload String,
    old_col String TTL ts + INTERVAL 1 DAY
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(ts)
ORDER BY ts
TTL ts + INTERVAL 90 DAY DELETE,          -- rows leave after 90 days
    ts + INTERVAL 30 DAY TO VOLUME "slow"; -- then 30 days on slow storage

ALTER TABLE events MATERIALIZE TTL;        -- force rules onto existing parts
```

**Listing 1.** Column expiry, tiered storage, and row deletion in one table — plus the manual materialization for existing data.

> [!warning] TTL-expired rows remain visible until a merge touches their part
> Deletion happens at merge time; a cold part that never merges keeps serving expired rows, which surprises everyone exactly once (compliance teams second). The standard mitigations: partition by the TTL time field at day/month granularity so merges and [[How do you drop old data quickly in ClickHouse]]-style partition drops align with expiry, set `ttl_only_drop_parts = 1` for whole-part drops, and run `MATERIALIZE TTL` when back-applying new rules. This merge-lag behavior is the flip side of every append-only design here, including [[What is a data part in ClickHouse]].

> [!tip] Interview answer
> TTL is declarative data aging: table-level DELETE for rows, column-level expiry, RECOMPRESS, TO DISK/TO VOLUME tiering, and GROUP BY rollups. Rules execute during merges — so expiry is eventual — and the best practice is partitioning by the TTL time field with ttl_only_drop_parts so whole partitions drop instead of being rewritten.
