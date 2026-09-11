<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is point-in-time recovery in PostgreSQL?

> [!abstract] Short answer
> PITR is the ability to restore the cluster to any chosen moment, not just to the last backup: you restore a base backup, then replay archived WAL segments up to a target time, LSN, or transaction id, stopping exactly there (recovery_target_time and friends). It exists because continuous archiving keeps every WAL record — the replay can stop anywhere between commits.

## The machinery

1. **Continuous archiving** runs from the start: `archive_mode = on` plus `archive_command`/`archive_library` copies every filled 16 MB WAL segment to safe storage. Without archived WAL there is no PITR — only crash recovery ([[What is the PostgreSQL WAL]]).
2. **Base backup** (pg_basebackup or an atomic snapshot) is taken while archiving runs; the backup's `backup_label` records its starting WAL position.
3. **Recovery** = restore the base backup, provide the archived WAL, and a restore command; the server replays forward until the target or the end of the archive.

```bash
restore_command = 'cp /archive/%f %p'
recovery_target_time = '2026-09-10 14:59:00+03'
recovery_target_action = 'promote'
```

**Listing 1.** The recovery.signal-era settings: replay archived WAL and stop just before the named moment (the time boundary is transaction-granular: a transaction that committed at the target is included).

```d2
base: "Base backup\nMonday 02:00" {width: 260; height: 70}
wal: "Archived WAL\nMon..Fri segments" {width: 280; height: 70}
dis: "Disaster\nFriday 15:00: bad DELETE commits" {width: 340; height: 80}
rec: "Restore base + replay WAL\nstop at 14:59:59" {width: 330; height: 80}
base -> rec
wal -> rec
dis -> rec: "choose target before"
```

**Fig. 1.** Replay is forward-only and stops exactly where you aim; everything after the target (including the mistake) is discarded.

## What it is for

- Undoing logical disasters (bad migration, dropped table) — the only built-in answer, since replication replays mistakes too ([[How would you explain PostgreSQL replication strategies]]).
- Cloning the cluster to a specific moment (audit, forensics).
- Building delayed warm standbys by replaying with a time lag.

## Costs to state

Continuous archiving consumes storage and adds a small commit-time dependency (an archiving backlog must be monitored; a stuck archive_command eventually blocks WAL recycling); recovery time is proportional to the WAL volume to replay — recovering a week means replaying a week of writes. Retention policy (how much archive to keep) is a business decision.

> [!warning] PITR granularity is a transaction, and it is all-or-nothing cluster-wide
> You cannot restore one table to 14:59 — the whole cluster rewinds; anything else committed after the target is gone and must be re-derived. And archiving is a pipeline: if segments were never shipped (archive_command failing silently), the recovery stops at the last available segment — the drill must test the archive, not just the backup ([[How do you take a PostgreSQL backup]]).

> [!tip] Interview answer
> PITR is continuous-archiving recovery: a base backup plus archived WAL lets you replay to any moment — target time, LSN, or xid — and stop there. It is the undo mechanism for logical disasters, at the cost of storing all WAL, replaying it forward, and rewinding the entire cluster to one instant. Test the archive path, not only the base backup.
