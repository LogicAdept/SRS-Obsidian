<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS

# What is a HOT update in PostgreSQL?

> [!abstract] Short answer
> Heap-Only Tuple (HOT) is an update optimization: when the update changes no indexed column and the new version fits on the same page, PostgreSQL skips writing new index entries and chains the old version to the new one inside the page. It cuts write amplification dramatically and lets intermediate versions be cleaned without an index pass.

## The two conditions

1. The update does not modify any column referenced by an index on the table (BRIN summarizing indexes are the exception — they tolerate HOT).
2. The new tuple fits in free space on the same page as the old one.

```d2
upd: "UPDATE row" {width: 180; height: 60}
q1: "Any indexed column\nchanged?" {width: 250; height: 70}
q2: "Fits on\nthe same page?" {width: 230; height: 70}
hot: "HOT update\nno new index entries,\nchain via item pointer" {width: 300; height: 90}
cold: "Regular update\nnew index entry in EVERY index" {width: 330; height: 90}
upd -> q1
q1 -> cold: yes
q1 -> q2: no
q2 -> cold: no
q2 -> hot: yes
```

**Fig. 1.** HOT is checked after the indexed-column test; failing either condition falls back to a regular update that touches every index.

## Why it matters

- Write cost: a regular update inserts an entry into each index on the table; a HOT update inserts into none.
- Cleanup: intermediate HOT versions can be pruned during normal selects — vacuum does not need to touch the indexes.
- Monitoring: `pg_stat_all_tables` shows `n_tup_upd` versus `n_tup_hot_upd`; a low HOT ratio on an update-heavy table is a tuning signal.

```sql
CREATE TABLE events (id int PRIMARY KEY, status text, payload text);
UPDATE events SET payload = 'new';  -- payload not indexed: HOT-eligible
UPDATE events SET status  = 'done'; -- if status is indexed: never HOT
```

**Listing 1.** The column list decides eligibility: updating an indexed column always defeats HOT, regardless of page space.

## Interaction with fillfactor

Condition 2 is where [[What is fillfactor in PostgreSQL]] comes in: leaving free space per page raises the HOT ratio for tables that update the same rows repeatedly. If you do not lower fillfactor, HOT still happens when pages happen to have room, but predictable HOT behavior needs deliberate space.

> [!warning] A "useless" index can silently disable HOT
> One extra index on a frequently updated column changes every update on the table into a full non-HOT rewrite touching all indexes. When `n_tup_hot_upd` is near zero, look for rarely used indexes first — [[How do you find unused indexes in PostgreSQL]] — before blaming autovacuum.

> [!tip] Interview answer
> HOT means Heap-Only Tuple: if an update touches no indexed column and the new version fits on the same page, PostgreSQL chains versions inside the page and skips all index maintenance. It lowers write amplification and speeds cleanup; the knobs are not indexing updated columns and lowering fillfactor, and the metric is n_tup_hot_upd versus n_tup_upd.
