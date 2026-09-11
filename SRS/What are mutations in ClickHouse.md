<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What are mutations in ClickHouse?

> [!abstract] Short answer
> Mutations are the heavyweight way to change existing data: `ALTER TABLE ... UPDATE` or `ALTER TABLE ... DELETE` re-merge affected parts to rewrite them, asynchronously by default. They are tracked in `system.mutations`, replicated per replica, and expensive — for targeted deletes the lightweight `DELETE FROM` (lightweight `DELETE FROM` pattern via the hidden `_row_exists` mask) is usually the better tool.

## Mechanics

A mutation command is registered as an entry in `system.mutations` (with an `is_done` flag), then each replica applies it in its own queue: parts containing rows matching the WHERE clause are entirely re-read and re-written — not in-place edits — so a mutation over a wide table is a rewrite job proportional to matched parts. `mutations_sync = 1` (or 2 for replicas) makes the statement block until done; by default it returns immediately. The ALTER guide documents the mutation family broadly: `UPDATE`/`DELETE`, `MATERIALIZE INDEX`/`PROJECTION`/`COLUMN`, TTL materializations — all part-rewriting mutation commands with the same synchronicity control. `ON CLUSTER` distributes the command to every node; on replicated tables it replicates like any mutation ([[How do you ALTER a replicated ClickHouse table]]).

The contrast with the lightweight path is worth memorizing: `DELETE FROM` marks rows through a hidden `_row_exists` mask column and is synchronous by default (`lightweight_deletes_sync`), while `ALTER DELETE` rewrites parts and is asynchronous by default (`mutations_sync`) — the two knobs are almost opposite. Either way, physically reclaiming disk waits for merges; and because all mutations of one table execute sequentially, one long rewrite delays every queued correction behind it.

```sql
ALTER TABLE hits UPDATE visitor_ids = dictGet('visitors', 'new_id', visitor_id)
WHERE event_date = '2026-09-01';          -- async part rewrite

SELECT command, is_done, latest_fail_reason
FROM system.mutations
WHERE table = 'hits' AND NOT is_done;
```

**Listing 1.** A dictionary-backed correction as a mutation, and the queue check that tells you when it finished.

> [!warning] The mutations queue is sequential per table
> All mutations on one table execute in order — pile up a few long rewrites and every subsequent mutation (including lightweight deletes) waits behind them, stalling both writes' hygiene and delete semantics. The docs' best-practice page is literally titled "avoid mutations": design for append + ReplacingMergeTree upserts ([[What is ReplacingMergeTree]]) or TTL-based cleanup, and reserve mutations for batch corrections (GDPR erasure, backfills), not application-path updates.

> [!tip] Interview answer
> A mutation is ALTER TABLE UPDATE/DELETE — an asynchronous, part-rewriting job tracked in system.mutations and applied per replica; mutations_sync can make it blocking. Because each mutation rewrites matched parts and queues sequentially per table, they're for batch corrections, not frequent updates — lightweight DELETE and versioned engines exist for the frequent cases.
