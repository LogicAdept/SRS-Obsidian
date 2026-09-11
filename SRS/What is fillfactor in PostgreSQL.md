<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS

# What is fillfactor in PostgreSQL?

> [!abstract] Short answer
> Fillfactor is a per-table or per-index storage parameter that reserves free space inside each page: 100 (the default for tables) means pages are packed full on insert; lowering it, say to 70, leaves 30 percent of every page empty so future updated row versions can stay on the same page and qualify for HOT updates. For B-tree leaf pages the default is 90, leaving room for index growth.

## What it controls

On the heap, fillfactor is the percentage of each page filled at insert time. Its only purpose is leaving room for updates: MVCC writes new versions ([[What is MVCC in PostgreSQL]]), and a version placed on the same page enables HOT updates ([[What is a HOT update in PostgreSQL]]) with no index maintenance. On indexes, fillfactor leaves room for new index tuples during splits; B-tree leaf pages default to 90 because index inserts are not append-only.

```sql
CREATE TABLE hot_table (id int PRIMARY KEY, status text, payload jsonb)
  WITH (fillfactor = 70);
ALTER TABLE orders SET (fillfactor = 80);   -- applies to future writes
CREATE INDEX ON hot_table (status) WITH (fillfactor = 80);
```

**Listing 1.** Fillfactor is set per relation; changing it on an existing table affects only newly written pages, so it is usually combined with a rewrite (VACUUM FULL, pg_repack) when you want the whole table re-padded.

## Choosing a value

- Update-heavy tables where updates hit a stable row set: 60-80 is typical; the tradeoff is roughly 20-40 percent more disk and cache for a higher HOT ratio.
- Insert-only or immutable tables (append logs, archives): keep 100 — reserved space is wasted.
- Indexes on hot updated columns: leave the 90 default or slightly lower; GIN does not use fillfactor.

```d2
packed: "fillfactor 100\npage packed, new version\ngoes to another page" {width: 290; height: 90}
spaced: "fillfactor 70\n30% reserved, new version\nstays, HOT applies" {width: 300; height: 90}
packed -> spaced: "rewrite with lower fillfactor"
```

**Fig. 1.** Reserving page space converts cross-page update chains into same-page HOT chains.

## How to judge it worked

Compare `n_tup_hot_upd` with `n_tup_upd` in `pg_stat_all_tables` before and after; watch table size growth and the autovacuum load. If HOT was already happening (pages naturally have room), lowering fillfactor just inflates storage for nothing ([[What is table bloat in PostgreSQL]] — distinguish reserved space from dead-tuple bloat).

> [!warning] Fillfactor is not a vacuum substitute
> Reserved page space does not shrink the table or remove dead tuples; it only positions new versions better. A table suffering bloat because autovacuum cannot keep up ([[What is autovacuum in PostgreSQL]]) gets worse with a low fillfactor — the file grows even faster.

> [!tip] Interview answer
> Fillfactor reserves free space per page — 100 by default for heaps, 90 for B-tree leaves. Lowering it on update-heavy tables lets new row versions stay on the original page, enabling HOT updates with no index writes. The cost is extra disk and cache; the win shows up as n_tup_hot_upd approaching n_tup_upd.
