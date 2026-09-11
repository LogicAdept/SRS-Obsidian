<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Partitioning #SRS

# How does PostgreSQL declarative partitioning work?

> [!abstract] Short answer
> You declare a table as partitioned with PARTITION BY (range, list, or hash) and a key; each partition is a real child table holding the rows whose key falls in its bounds, and queries name the parent. The planner prunes partitions by key predicates, indexes are created once on the parent and mirrored per partition, and rows route automatically on insert — with a documented limitation: a unique constraint must include the partition key.

## The three methods

| Method | Key shape | Typical use |
|---|---|---|
| RANGE | bounds per partition, lower inclusive, upper exclusive | time series, archival |
| LIST | explicit value lists | regions, categories, tenants |
| HASH | modulus and remainder | even spread, no natural ranges |

```sql
CREATE TABLE measurement (
  city_id int, logdate date, value numeric
) PARTITION BY RANGE (logdate);

CREATE TABLE measurement_2026_08 PARTITION OF measurement
  FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
```

**Listing 1.** The minimal range setup; partitions can themselves be partitioned (sub-partitioning).

```d2
ins: "INSERT INTO measurement" {width: 280; height: 60}
key: "Route by key\nlogdate in bounds?" {width: 250; height: 70}
p1: "partition 2026_08" {width: 230; height: 60}
p2: "partition 2026_09" {width: 230; height: 60}
err: "no partition: error\n(DEFAULT partition catches)" {width: 300; height: 70}
ins -> key
key -> p1: yes_08
key -> p2: yes_09
key -> err: none
```

**Fig. 1.** Insert routing by the partition key; a DEFAULT partition absorbs unbounded rows.

## What the planner and the DDL give you

- **Partition pruning**: predicates on the key eliminate partitions at plan time (and at execution time for prepared statements) — the general mechanism is in [[How does partition pruning speed up a query]] and the design guidance in [[How do you design good database partitioning]].
- **Parent-level indexes**: CREATE INDEX on the parent creates matching indexes on all partitions (and on new ones); unique constraints must include every partition key column, because uniqueness can only be enforced per-partition plus routing guarantees.
- **Maintenance via ATTACH/DETACH**: DETACH PARTITION instantly "drops" old data as a standalone table (with CONCURRENTLY it needs only SHARE UPDATE EXCLUSIVE on the parent); ATTACH validates bounds — pre-create a CHECK constraint to avoid the full scan ([[How do you drop old data quickly in ClickHouse]] is the analytical twin of this pattern).
- Row movement: updating a row's partition key moves it between partitions under the hood.

## Costs and limits

No cross-partition unique constraint without the key; no global index across partitions; many partitions increase planning time; a partitioned table cannot be turned into a regular table in place. The inheritance-based legacy method remains for non-standard splits.

> [!warning] "Partitioned table" is not one table with hidden files
> Each partition is an independent relation with its own storage, indexes and statistics; the parent is routing metadata. Consequences: autovacuum, ANALYZE and bloat are per-partition concerns ([[What is autovacuum in PostgreSQL]]), and a unique constraint missing the partition key is rejected — trying to bolt on global uniqueness after the fact is the classic redesign moment ([[What is a unique database constraint for]]).

> [!tip] Interview answer
> Declarative partitioning: PARTITION BY range, list or hash on a key; partitions are real child tables; inserts route by key, the planner prunes by key predicates, and indexes propagate from parent to children. You get cheap archival via DETACH, and you pay with the rule that unique constraints must include the partition key and with per-partition maintenance.
