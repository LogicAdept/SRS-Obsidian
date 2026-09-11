<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is transaction ID wraparound in PostgreSQL?

> [!abstract] Short answer
> PostgreSQL transaction IDs are 32-bit, so the counter eventually wraps around and old transactions would suddenly look like they are from the future — making their rows invisible, i.e. silent data loss. To prevent it, VACUUM freezes old tuples, and if a table goes unvacuumed for about two billion transactions the system first warns, then stops accepting new transactions.

## The circular XID space

XIDs are compared modulo 2 to the 32nd power: for every XID there are two billion "older" and two billion "newer" IDs. A row version stays visible "in the past" for the next two billion transactions — after that it would fall into the future unless handled. The fix: aggressive vacuum rewrites old `xmin` stamps to a special frozen marker that always counts as the oldest, so the tuple stays visible no matter how the counter wraps ([[What are xmin and xmax in PostgreSQL]]).

```d2
ok: "Age < 2 billion\nrows visible, vacuum on schedule" {width: 330; height: 80}
warn: "40 million left\nwarnings in the log:\n'not accepting commands'" {width: 330; height: 90}
stop: "3 million left\nERROR: database is not accepting\ncommands that assign new transaction IDs" {width: 380; height: 100}
ok -> warn: "no vacuum"
warn -> stop: "still no vacuum"
```

**Fig. 1.** The failure ladder: warnings start when the oldest unfrozen XID is 40 million transactions from wraparound; the database refuses new XIDs at 3 million left.

## What forces freezing

- `autovacuum_freeze_max_age` (200 million transactions): a table whose oldest unfrozen XID is older is vacuumed even with autovacuum disabled.
- `vacuum_freeze_min_age` decides how old an XID must be before rows are frozen; `vacuum_freeze_table_age` triggers aggressive full scans.

## Monitoring the age

Track XID age before warnings start: `age(relfrozenxid)` over pg_class per table and `age(datfrozenxid)` over pg_database per cluster. A healthy graph is sawtooth — ages grow between aggressive vacuums and reset when freezing passes. A monotonically climbing oldest table is the early-warning shape: intervene weeks before the 40-million-transactions warning, not after ([[What is autovacuum in PostgreSQL]] for the trigger settings).

Remember the horizon coupling: age can only advance to the oldest active snapshot, so wraparound protection is hostage to the same long transactions that block bloat cleanup ([[Why do long-running transactions hurt PostgreSQL]]). A cluster with strict timeouts and short transactions never meets the wraparound emergency — prevention lives in application hygiene more than in vacuum tuning.

## Operational signs and fixes

Signs: warnings about database `mydb` with `... not accepting commands ...`, `SELECT relname, age(relfrozenxid) FROM pg_class WHERE relkind = 'r' ORDER BY age DESC` showing old tables. Fix: run VACUUM (not VACUUM FULL — it needs an XID) on the oldest tables, usually in single-table order. Large idle-in-transaction sessions and abandoned replication slots hold horizons and accelerate aging ([[Why do long-running transactions hurt PostgreSQL]], [[What is a replication slot in PostgreSQL]]).

> [!warning] Do not confuse the two vacuum emergencies
> "Autovacuum is stuck on my big table" (space reclamation) and "database is not accepting commands" (wraparound) are different problems with different fixes. The second one is a full-stop condition: the database is read-only-ish for any command that assigns XIDs, and the remedy is a manual aggressive VACUUM, not config tweaks.

> [!tip] Interview answer
> XIDs are 32-bit and compared modulo, so after about two billion transactions un-frozen rows would appear to be from the future — catastrophic data loss. VACUUM freezes old tuples to a special always-oldest stamp; autovacuum enforces this via autovacuum_freeze_max_age (200 million), warns at 40 million remaining, and hard-stops the database at 3 million unless a vacuum advances relfrozenxid.
