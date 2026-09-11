<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> PostgreSQL's `VACUUM` reclaims the space of **dead tuples** — rows made obsolete by UPDATE/DELETE that MVCC keeps visible to older snapshots — and makes pages reusable; without it, tables and indexes bloat monotonically. Plain VACUUM reclaims space *for reuse within the table* (file does not shrink); `VACUUM FULL` rewrites the table and returns space to the OS, at the price of an exclusive lock. Autovacuum runs it continuously in the background; SQLite's identically-named VACUUM rebuilds the database file and *does* shrink it ([[How do stale statistics hurt a query plan]]).

The verified demo demonstrates the storage mechanics on SQLite: after inserting 512-byte-page bulk data the file holds 54 pages; deleting every second row leaves page_count **unchanged at 54** — the pages are marked free internally, not released (this is precisely the PostgreSQL plain-VACUUM model); after `VACUUM`, the page count drops to 28 — the rewrite compacted the file. That arc *is* the answer's skeleton: deletes do not shrink storage in MVCC engines, vacuum work is what makes dead space reusable, and only a rewrite (SQLite VACUUM, PG VACUUM FULL, or pg_repack) returns it to the OS. The PostgreSQL specifics the question expects: MVCC creates a dead-tuple stream on every UPDATE (even no-op ones — a full row rewrite), autovacuum lazily cleans per-table based on thresholds, and vacuum also **freezes** transaction IDs (wraparound protection — the documented reason vacuum is not optional), updates visibility-map bits that enable index-only scans, and optionally refreshes planner statistics (ANALYZE) ([[How do you optimize COUNT star on a large table]]). The bloat story interviewers love: a churned table that autovacuum cannot keep up with (misconfigured thresholds, long transactions pinning xmin) grows until queries slow and disk fills — the cure is tuning autovacuum, shortening transactions, and scheduled VACUUM FULL windows on pathological tables ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
PRAGMA page_size = 512;
CREATE TABLE bulk (id INTEGER PRIMARY KEY, payload TEXT);
INSERT INTO bulk (payload) SELECT '0123456789abcdef...';   -- 512-byte rows
PRAGMA page_count;
-- 54
DELETE FROM bulk WHERE id % 2 = 0;
PRAGMA page_count;
-- 54
-- (deleted rows free their space for reuse -- the file does NOT shrink)
VACUUM;
PRAGMA page_count;
-- 28
-- (VACUUM rebuilt the file: dead space reclaimed and returned)
```

**Listing 1.** Verified on SQLite 3.53.1. The three-page-count arc — 54, 54, 28 — is the whole story: deletes mark space dead, reuse keeps the size, and VACUUM's rebuild returns it. PostgreSQL's VACUUM adds the MVCC-specific parts: dead-tuple cleanup, freezing, visibility-map maintenance.

```d2
direction: right
u: "UPDATE / DELETE
old tuples become dead" {width: 210; height: 80}
v: "VACUUM
scan, remove dead tuples,
free pages for reuse" {width: 230; height: 90}
f: "VACUUM FULL / rewrite
compact + return to OS
(exclusive lock)" {width: 240; height: 90}
u -> v -> f
```

**Fig. 1.** The bloat pipeline and its two valves: routine vacuum makes dead space reusable in place; the full rewrite is the only step that actually shrinks the object.

> [!warning] Long-running transactions block vacuum everywhere — the delayed bloat bomb
> A week-old open transaction (idle-in-transaction session, a stuck replication slot) pins the oldest snapshot, so vacuum cannot remove tuples newer than it; the table and indexes bloat under a perfectly configured autovacuum. Monitor oldest-xmin lag and idle transactions — the bloat is downstream of them, not of vacuum settings alone ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> VACUUM is MVCC housekeeping: UPDATE and DELETE leave dead tuples visible to old snapshots, and VACUUM reclaims them for reuse, freezes transaction IDs against wraparound, and maintains the visibility map for index-only scans. My SQLite demo shows the same storage physics — delete leaves page_count unchanged, VACUUM's rebuild halves it. Plain VACUUM reuses space in place, VACUUM FULL rewrites and shrinks under an exclusive lock, autovacuum keeps up normally — unless a long-open transaction pins xmin, which is the first thing I check on a bloating table.
