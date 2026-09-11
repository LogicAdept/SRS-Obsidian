<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# How do you materialize a skip index on existing ClickHouse data?

> [!abstract] Short answer
> `ALTER TABLE ... ADD INDEX` only changes metadata — existing parts stay unindexed, and queries over old data get no benefit. To build the index retroactively you run a materialize mutation: `ALTER TABLE t MATERIALIZE INDEX ix_name` (optionally `IN PARTITION p`), which asynchronously rewrites each part and populates its index files.

## Step by step

The mutation rewrites every active part — reading, recomputing the index, writing a replacement part — so it behaves like any other mutation: asynchronous by default, tracked in `system.mutations` with an `is_done` flag, and controlled by `mutations_sync` if you need blocking semantics. One statement can combine the metadata change and materialization (`ADD INDEX ... , MATERIALIZE INDEX ...`) for ordinary databases; the ALTER reference notes this packed form mixes alter and mutation segments and is rejected on DatabaseReplicated databases, where you keep them as separate statements. Materialization of a *projection* over existing data follows the same pattern with `MATERIALIZE PROJECTION` / `POPULATE PROJECTION` ([[What are projections in ClickHouse]]).

Two operational details matter. First, on a [[What is ReplicatedMergeTree]] table the materialize mutation runs independently on every replica through the replication queue, so check `system.mutations` per node rather than trusting one server's view. Second, scoping by partition (`MATERIALIZE INDEX ... IN PARTITION '202609'`) turns a single full-table job into a controlled sequence — the standard way to warm up indexes for the hot retention window first ([[What data skipping indexes exist in ClickHouse]]) while cold months materialize overnight.

```sql
ALTER TABLE events ADD INDEX user_ix user_id TYPE bloom_filter(0.01) GRANULARITY 1;

ALTER TABLE events MATERIALIZE INDEX user_ix;               -- all partitions
ALTER TABLE events MATERIALIZE INDEX user_ix IN PARTITION '202609';

SELECT command, is_done
FROM system.mutations
WHERE table = 'events' AND NOT is_done;
```

**Listing 1.** Add the index, materialize it (whole table or one partition), and watch the mutation in `system.mutations`.

> [!warning] Materialization rewrites parts — it is a full-table job
> Like [[What are mutations in ClickHouse]], it re-reads and re-writes every column of every part, consuming I/O and merge capacity; on a busy table run it partition by partition off-peak, or rely on natural rewrites: data reinserted via TTL moves and merges will pick the index up anyway. Skipping materialization is also a valid strategy when old data rarely gets filtered — the index silently serves only new parts.

> [!tip] Interview answer
> ADD INDEX is metadata-only; existing parts remain index-less until you issue MATERIALIZE INDEX, which is an asynchronous mutation that rebuilds each part with the index populated, per partition if you scope it. You monitor it in system.mutations, and like any mutation it's a heavy rewrite job — plan it off-peak or let new parts pick it up naturally.
