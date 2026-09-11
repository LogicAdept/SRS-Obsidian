<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is CollapsingMergeTree?

> [!abstract] Short answer
> CollapsingMergeTree represents mutations as paired rows: a `Sign` column of 1 (state) and -1 (cancel). When a background merge meets a 1/-1 pair with identical sorting-key values, both rows disappear — an insert-plus-cancel pair implements an update, a lone -1 implements a delete. An object's current value is `sum(Sign)`-weighted, and queries read it through that aggregation, not by fetching "the" row.

## Mechanics

Declared `CollapsingMergeTree(Sign)` with `Sign Int8`. Writing value v for key k inserts `(k, v, Sign=1)`; changing it inserts `(k, v2, 1)` plus a cancel row `(k, v, -1)` for the old value; removing it inserts `(k, v, -1)`. Merges cancel out pairs, so storage trends toward one row per live object — but only *eventually*: until the merge, both rows exist and correctness depends on reading `sum(Sign)` (or aggregating value columns as `sum(v * Sign)`). The failure mode the docs call out: if the same state value is written twice, the pair count goes odd and one row survives — duplication by design; and cancel rows can merge with the *wrong* instance of the value when updates arrive out of order.

```sql
CREATE TABLE queue
(
    id UInt64,
    views UInt64,
    Sign Int8
)
ENGINE = CollapsingMergeTree(Sign)
ORDER BY id;

INSERT INTO queue VALUES (7, 100, 1);   -- state
INSERT INTO queue VALUES (7, 100, -1);  -- cancel old value
INSERT INTO queue VALUES (7, 150, 1);   -- new state
SELECT id, sum(views * Sign) AS views, sum(Sign) AS alive FROM queue GROUP BY id;
```

**Listing 1.** An update as cancel-plus-state, and the aggregate read that stays correct before and after merges.

## VersionedCollapsingMergeTree

Out-of-order arrival — normal with parallel writers — can pair a -1 with the wrong 1. `VersionedCollapsingMergeTree(Sign, Version)` fixes pairing by matching rows on identical key *and* version, letting merges collapse correctly even when rows were written out of order; it is the default recommendation whenever multiple writers update the same object. When the use case is pure CDC upserts rather than cancel-based mutation, [[What is ReplacingMergeTree]] is the simpler engine, and [[What is the Kafka to ClickHouse materialized view pattern]] shows the ingestion side.

> [!warning] Collapsing is not a row update — it is a bookkeeping protocol
> Every read must be aggregation-aware (`sum(Sign)`), every writer must emit cancel rows, and an odd sign count silently means duplicated or lost state. The engine cannot repair an application that just inserts 1-rows forever — table size grows and "current value" doubles. Interview answers that skip the application-side protocol miss the whole point of the engine.

> [!tip] Interview answer
> CollapsingMergeTree encodes updates and deletes as +/- row pairs on a Sign column; merges cancel the pairs, and reads compute current state with sum(Sign). It's eventually-collapsing, protocol-dependent bookkeeping — and VersionedCollapsingMergeTree extends it with a version column so out-of-order writes still pair correctly.
