<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Replication #SRS

# What is the PostgreSQL WAL?

> [!abstract] Short answer
> The Write-Ahead Log is an append-only journal on disk: before any data page is modified, PostgreSQL records the change in the WAL and flushes it. On a crash the database replays the WAL to restore consistency. The same stream powers replication (standbys receive it), PITR (archive it), and logical decoding (decode it into row changes).

## The write path

A committing transaction must ensure its changes survive a crash. Writing every dirty page to the heap would be random I/O; instead PostgreSQL writes a compact sequential WAL record first (fsync on commit by default — `synchronous_commit = on`), while data pages reach disk later via checkpoints or the background writer. This is the "write ahead" rule: log first, data later.

```d2
txn: "Transaction commit" {width: 240; height: 60}
wal: "WAL buffer -> fsync to pg_wal\nsequential append" {width: 300; height: 80}
page: "Dirty page in shared buffers\nflushed later, spread out" {width: 340; height: 80}
disk: "Heap / index files" {width: 240; height: 60}
txn -> wal: "commit waits for WAL flush"
wal -> page: "record references the page"
page -> disk: "checkpoint or bgwriter"
```

**Fig. 1.** Commit latency is bound to a sequential WAL fsync; the random-I/O page writes happen asynchronously afterwards.

## One stream, four consumers

1. **Crash recovery** — after a crash, replay from the last checkpoint restores consistency.
2. **Physical streaming replication** — `wal_level = replica` ships WAL records to standby servers ([[What is the difference between streaming and logical replication in PostgreSQL]]).
3. **Archiving and PITR** — archived segments let you recover to any point in time ([[What is point-in-time recovery in PostgreSQL]]).
4. **Logical decoding** — `wal_level = logical` adds the information needed to decode changes into row images ([[What is the difference between streaming and logical replication in PostgreSQL]]).

## Anatomy: segments, writers, recycling

The log lives in pg_wal as 16 MB segment files, served by dedicated WAL writer and WAL sender processes; filled segments are recycled in place once no consumer needs them. Every retention consumer — archiving, a replication slot, a lagging standby — can hold segments from recycling, which is why all of them surface as pg_wal growth: the slowest consumer sets the floor.

## Segments and settings that matter

WAL lives in `pg_wal` as 16 MB segment files. Key knobs: `wal_level` (replica by default), `fsync` (on — never disable in production), `full_page_writes` (on — protects against torn pages after a crash), `wal_compression` (off by default; compresses full-page images), and `max_wal_size`, which steers checkpoint frequency ([[What is a checkpoint in PostgreSQL]]).

> [!warning] synchronous_commit = off trades durability, not consistency
> Turning `synchronous_commit` off means the client is told "committed" before the WAL is flushed; a crash can lose the last few transactions (up to about three times `wal_writer_delay`). It never corrupts the database — the transactions are simply lost as if aborted — but for money-bearing paths it is a real durability change, unlike a plain performance knob.

> [!tip] Interview answer
> The WAL is the sequential journal PostgreSQL writes before touching data pages: commit only waits for a WAL fsync, pages flush later. It is the backbone of the whole storage engine — crash recovery replays it, standbys stream it, archiving enables PITR, and logical decoding turns it into row-level change streams for logical replication and CDC.
