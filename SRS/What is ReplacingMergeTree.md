<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is ReplacingMergeTree?

> [!abstract] Short answer
> ReplacingMergeTree handles updates in an insert-only world: you insert multiple versions of the same row, and background merges keep only the one with the highest version — where "same row" means equal values of every `ORDER BY` column. Deduplication happens only at merge time and only within a part's merge lineage, so queries that need a guaranteed single row use `FINAL` or aggregation tricks.

## Mechanics

The engine is declared `ReplacingMergeTree([ver[, is_deleted]])`. The `ORDER BY` clause defines identity: two rows equal on all key columns are duplicates, no primary-key constraint is enforced. The optional `ver` column (UInt*/Date/DateTime) picks the winner — the row with the largest version survives; without it, an arbitrary one of the duplicates is kept (effectively the last processed). Since version 23.x it can also take a soft-delete column: a row with `is_deleted = 1` marks itself and all its duplicates as deleted — but deleted rows are *retained* and only physically removed by `OPTIMIZE ... FINAL CLEANUP` under an experimental setting, so soft deletes hide rows without shrinking data.

```sql
CREATE TABLE users
(
    id UInt64,
    name String,
    updated_at DateTime
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY id;

INSERT INTO users VALUES (1, 'old', '2026-01-01 00:00:00');
INSERT INTO users VALUES (1, 'new', '2026-09-01 00:00:00');
SELECT * FROM users FINAL WHERE id = 1;   -- 'new', after merge or query-time merge
```

**Listing 1.** Two versions of id=1 inserted; `FINAL` forces the highest-`updated_at` row to win at read time.

```d2
insert: "Two inserts\nid=1 ver=1, id=1 ver=2" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
parts: "Different parts\nduplicates coexist" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
merge: "Background merge\nkeeps max(ver) row" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
query: "SELECT ... FINAL\nquery-time merge if not yet merged" {
  width: 340
  height: 90
  style.fill: "#f3e5f5"
}
insert -> parts
parts -> merge: eventually
parts -> query: correct answer now
```

**Fig. 1.** Duplicates live in separate parts until a merge; `FINAL` gives a correct answer without waiting for that merge.

> [!warning] "Replacing" does not mean "replaced"
> Between insert and merge the table holds *both* versions — plain `SELECT` without `FINAL` returns duplicates, and even `FINAL` cannot shrink the soft-deleted tombstones. The common production bug is reading the table without FINAL, seeing two rows, and "fixing" it with constant OPTIMIZE. The correct model: read-side dedup ([[What is FINAL in ClickHouse]] or `argMax`-style aggregation), and the engine as storage hygiene. This is exactly the pattern [[What is the Kafka to ClickHouse materialized view pattern]] relies on for CDC upserts.

> [!tip] Interview answer
> ReplacingMergeTree deduplicates rows with identical ORDER BY key values during background merges, keeping the highest version column value — inserts stay immutable, updates become newer inserts. Queries need FINAL or aggregation to be sure they see one row per key, and soft-deleted tombstones persist until a cleanup optimize. It's update emulation, not OLTP update semantics.
