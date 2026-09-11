<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Transactions #SRS

# What is a dead tuple in PostgreSQL?

> [!abstract] Short answer
> A dead tuple is a row version that no transaction can see anymore — its deleting transaction (`xmax`) is committed and no live snapshot can still reach it. Dead tuples are the garbage MVCC produces; VACUUM is the garbage collector that removes them and makes the space reusable.

## How a tuple becomes dead

An `UPDATE` writes a new version and stamps the old one with the updater's XID in `xmax`; a `DELETE` only stamps. The version is not removed at that moment because concurrent snapshots may still need it. Once the oldest running transaction in the cluster is newer than the deleting transaction, the version is unreachable garbage. See [[What are xmin and xmax in PostgreSQL]] for the stamps and [[What is MVCC in PostgreSQL]] for the snapshot model.

```d2
live: "Live tuple\nxmin committed, xmax unset\nor xmax not yet visible" {width: 300; height: 90}
pending: "Expiring tuple\nxmax committed, but an old\nsnapshot can still see it" {width: 310; height: 90}
dead: "Dead tuple\nno snapshot can see it\n(VACUUM will remove)" {width: 300; height: 90}
live -> pending: "UPDATE / DELETE\nstamps xmax"
pending -> dead: "oldest snapshot\nmoves past xmax"
```

**Fig. 1.** Death is a two-step process: first the tuple is expired for future snapshots, then — after the vacuum horizon passes — it becomes removable garbage.

## How you observe them

- `pg_stat_user_tables`: `n_dead_tup`, `last_autovacuum`, `n_tup_upd` vs `n_tup_hot_upd`.
- The `pgstattuple` extension returns the exact fraction of dead tuples and free space in a table.
- Query plans: a heavily bloated table shows an inflated `rows` estimate base and high page counts. See [[What is table bloat in PostgreSQL]] for the file-level effect.

One nuance keeps the model honest: HOT-updated chains are partially self-cleaning — intermediate versions of the same row can be pruned during ordinary selects without a vacuum pass ([[What is a HOT update in PostgreSQL]]). Dead tuples from non-HOT updates and deletes always wait for vacuum, which is why update-heavy tables with indexed columns are the ones that fight the cleaner the hardest.

One more practical distinction: dead tuples are counted per table, but their cost is felt per query — a seq scan must read past them, an index scan may follow pointers to them, and the planner's page-level cost estimates inflate with the bloat ([[What is table bloat in PostgreSQL]]). The counters are diagnostic; the slowdowns are where the business notices.

The flip side of the same coin: dead tuples are also the reason PostgreSQL rolls back instantly. No undo to apply — the "deleted" version was never physically removed, and the reader's snapshot simply stops seeing it. Frame dead tuples as the deferred cost of that design and the whole MVCC story lines up: cheap aborts now, vacuum work later ([[What is MVCC in PostgreSQL]] for the design, [[What is autovacuum in PostgreSQL]] for the bill payer).

## What removes them

VACUUM scans the heap, consults each tuple's stamps against the oldest snapshot, and marks dead lines as free space (kept in the Free Space Map for future inserts). Autovacuum does this automatically when dead tuples cross `autovacuum_vacuum_threshold + autovacuum_vacuum_scale_factor * reltuples` (defaults 50 + 0.2 of the table). HOT updates let intermediate versions be removed even during plain selects ([[What is a HOT update in PostgreSQL]]). Long transactions delay all of it ([[Why do long-running transactions hurt PostgreSQL]]).

> [!warning] Dead tuples still occupy space and slow scans
> Until VACUUM runs, dead tuples are physically present: seq scans read them, indexes may point at them, and the table file grows. "The row is deleted, so the space is free" is false — it is free only after vacuum, and even then the file usually does not shrink (see [[What is the difference between VACUUM and VACUUM FULL]]).

> [!tip] Interview answer
> A dead tuple is an expired row version — created by MVCC on every update or delete — that no snapshot can see anymore. VACUUM (usually autovacuum) removes them by comparing tuple stamps against the oldest running snapshot. Until then they inflate the table, slow scans, and are the direct link between MVCC, bloat, and vacuum tuning.
