<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is a checkpoint in PostgreSQL?

> [!abstract] Short answer
> A checkpoint is the moment when PostgreSQL forces all dirty data pages to disk and writes a checkpoint record to the WAL. Everything before that point is durable in the data files, so crash recovery never needs to replay further back than the last checkpoint. Checkpoints trade recovery time against I/O bursts.

## What happens

The checkpointer writes all dirty shared buffers to the heap and index files, fsyncs them, then appends a checkpoint record (including the current WAL position) to the log. From then on, recovery on crash replays WAL only from that record. A checkpoint also happens on: explicit `CHECKPOINT;` command, clean shutdown, `pg_basebackup` start, and size-driven events like growing a relation.

```d2
t0: "Checkpoint N\nall dirty pages flushed\nposition recorded in WAL" {width: 340; height: 90}
t1: "Normal work\nWAL grows, pages dirty" {width: 300; height: 70}
t2: "Checkpoint N+1\ntriggered by time or size" {width: 330; height: 80}
crash: "Crash between N and N+1\nreplay from checkpoint N" {width: 340; height: 90}
t0 -> t1 -> t2
t1 -> crash
```

**Fig. 1.** Recovery cost is proportional to WAL volume since the last checkpoint; checkpoint frequency buys faster recovery at the price of more write I/O.

## What triggers it

- Time: `checkpoint_timeout` (default 5 minutes).
- Size: WAL grown to `max_wal_size` (default 1 GB; it is a soft limit — exceeded under load rather than forcing an emergency checkpoint).
- Manual `CHECKPOINT` and shutdown.

`checkpoint_completion_target` (0.9) spreads the writes over 90 percent of the interval between checkpoints instead of dumping them in one burst, keeping I/O smooth.

## Why it interacts with everything

- Bulk load tuning often raises `max_wal_size` and `checkpoint_timeout` to cut the number of full-page images written ([[What is the PostgreSQL WAL]]).
- `full_page_writes` writes a full page image to WAL the first time a page is touched after each checkpoint; longer intervals mean fewer full-page images.
- A checkpoint is also the anchor for file-system-level backups and PITR consistency ([[What is point-in-time recovery in PostgreSQL]]).

> [!warning] max_wal_size is a soft limit, not a cap
> It is a budget that nudges the checkpointer; bursts (big COPY, CREATE INDEX) can overshoot it, and setting it very low does not hard-limit WAL — it just forces frequent checkpoints and I/O storms. The "checkpoint storm" anti-pattern: too-low max_wal_size plus default timeouts makes every five minutes an I/O spike and every commit jitter ([[How do you debug a slow PostgreSQL query]]).

> [!tip] Interview answer
> A checkpoint flushes all dirty pages to disk and anchors the WAL: recovery only replays from the last checkpoint, so checkpoints control crash-recovery time. They fire on timeout (5 min), WAL size (max_wal_size, soft), or command, and completion_target spreads the I/O. Tune them together with WAL settings for bulk loads; never treat max_wal_size as a hard cap.
