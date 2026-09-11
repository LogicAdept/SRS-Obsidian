<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# How do you do a PostgreSQL major version upgrade?

> [!abstract] Short answer
> Major upgrades (17 to 18) require a data format migration; the on-disk files are not compatible. Three methods: pg_upgrade — in-place, converts system catalogs in place, minutes to hours with --link; dump and restore with pg_dump/pg_restore — slow but bulletproof and version-jumping; logical replication — dual-write to a new major-version cluster and switch over with near-zero downtime. Minor upgrades (18.5 to 18.6) are drop-in replacements, not upgrades.

## The three paths

```bash
# 1. in-place
pg_upgrade --old-datadir ... --new-datadir ... --link --check  # rehearse first

# 2. dump and restore
pg_dumpall | psql -d new_cluster        # simple, slow for TBs

# 3. logical replication cutover
# create PG18 cluster -> publications on old, subscriptions on new
# catch up, then switch application connections
```

**Listing 1.** The three families; the decision variables are downtime budget, cluster size, and schema-extension compatibility ([[What is the difference between streaming and logical replication in PostgreSQL]] — the subscription mechanism powering path 3).

| Method | Downtime | Duration | Notes |
|---|---|---|---|
| pg_upgrade | full (server down) | minutes-hours | runs both binaries; --link avoids full copy but makes rollback destructive |
| dump/restore | full | longest | portable, also migrates across architectures |
| logical replication | near zero | setup hours/days | tables must have PKs/replica identity; sequences need special handling |

```d2
old: "Old cluster\nPG 17" {width: 220; height: 70}
chk: "pg_upgrade --check\non a restored copy" {width: 300; height: 80}
new: "New cluster\nPG 18" {width: 220; height: 70}
cutover: "Stop apps -> pg_upgrade / cutover\n-> analyze -> smoke tests" {width: 400; height: 90}
old -> chk -> new -> cutover
```

**Fig. 1.** Whatever the method, the shape is the same: rehearse, verify compatibility, migrate, validate.

## The checklist that saves the upgrade

- Read the release notes for breaking changes in the target major version — removed GUCs, changed defaults, planner behavior shifts.
- Extensions must exist in the new version's binaries ([[What are PostgreSQL extensions]]); DROP/reCREATE or upgrade them per their own instructions.
- After the upgrade: run ANALYZE (statistics do not transfer) — plans are freshly guessed ([[How do stale statistics hurt a query plan]]).
- Rehearse on a restored copy with production scale; time it; write the rollback.
- Rollback plan: pg_upgrade without --link keeps the old cluster intact; with --link the old data dir is mutated — keep the backup ([[How do you take a PostgreSQL backup]]).

> [!warning] An upgrade is a planner change, not just a file conversion
> New major versions ship new optimizer behavior, statistics targets and defaults; a query plan that was fine on 17 can be wrong on 18. The mitigation is not skipping upgrades — it is post-upgrade ANALYZE, plan regression testing on real workloads, and keeping pg_stat_statements history to compare ([[What is pg_stat_statements]]). "It upgraded cleanly" and "it performs the same" are different claims.

> [!tip] Interview answer
> Major versions need a real migration: pg_upgrade for in-place with minutes of downtime, dump-restore for simplicity and portability, or logical replication into a new cluster for a near-zero-downtime cutover. Rehearse with --check on a copy, verify extensions, ANALYZE after, and keep a tested rollback — plus remember minor versions need none of this, just a restart on new binaries.
