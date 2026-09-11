<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# How do you take a PostgreSQL backup?

> [!abstract] Short answer
> Three methods, layered in production: logical dumps with pg_dump (portable, per-database, restorable anywhere), physical base backups with pg_basebackup or a volume snapshot (the anchor for PITR and for standby provisioning), and file-system copies taken offline. A complete strategy combines a periodic base backup with archived WAL — that is what enables point-in-time recovery, not just full restores.

## The methods

```bash
# logical: one database, custom format, parallel restore
pg_dump -Fc mydb > mydb.dump
pg_restore -j 4 -d mydb_copy mydb.dump

# physical: base backup for a standby or PITR anchor
pg_basebackup -h primary -D /backup/base -X stream -P
```

**Listing 1.** pg_dump speaks SQL (portable across versions and platforms, selective per table, compressible); pg_basebackup copies the whole cluster's data files plus the required WAL ([[What is the PostgreSQL WAL]]).

- **pg_dump / pg_restore** — logical: consistent snapshot via a single transaction, no special locks beyond ACCESS SHARE (reads continue); restore speed is the weakness (rebuilds indexes, replays constraints); per-database only (roles and tablespaces live cluster-wide — pg_dumpall for globals).
- **pg_basebackup** — physical: full cluster image taken online via the replication protocol; the base for hot standbys and for archive-based recovery; restore = copy back + WAL replay. Requires space proportional to cluster size.
- **File-system snapshot** — physical, instant, only consistent if taken atomically (volume manager snapshot) with WAL available for replay ([[What is a checkpoint in PostgreSQL]] — the snapshot must not be older than retained WAL).

```d2
logical: "pg_dump\nSQL, portable, selective\nslow restore" {width: 320; height: 100}
phys: "pg_basebackup / snapshot\nfiles, cluster-wide\nfast restore, PITR anchor" {width: 340; height: 100}
pitr: "+ archived WAL\nrecovery to any point" {width: 300; height: 90}
phys -> pitr
```

**Fig. 1.** Logical for portability and selective restores; physical for speed and recovery-to-a-moment.

## What a real policy looks like

Base backup on a schedule (daily/weekly), continuous WAL archiving to off-site storage ([[What is point-in-time recovery in PostgreSQL]]), restore drills on a real calendar — an untested backup is a hypothesis. Logical dumps complement as an application-level safety net before risky migrations; pg_upgrade's own flow is a separate decision ([[How do you do a PostgreSQL major version upgrade]]).

> [!warning] Copying the data directory while the server runs is not a backup
> Without an atomic snapshot or the stopped server, a file-level copy mixes half-written pages and missing WAL — the restored cluster is corrupt in ways that appear later. The second classic: "I have a standby, that's my backup" — replication replays drops instantly ([[How would you explain PostgreSQL replication strategies]]). Backup answers recovery; replication answers availability.

> [!tip] Interview answer
> Three layers: pg_dump for portable, selective logical dumps; pg_basebackup or atomic snapshots for physical cluster images; and on top of the physical layer, continuous WAL archiving so you can recover to any point in time. Restore drills are part of the plan — and a standby is HA, not a backup.
