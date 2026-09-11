<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is a data part in ClickHouse?

> [!abstract] Short answer
> A data part (part) is the unit of storage in a MergeTree table: every `INSERT` that lands on a table creates one part — a directory on disk containing compressed column files, their mark files, the sparse primary index, checksums, and min-max statistics. Parts are self-contained, merged in the background, and are the granularity at which writes, merges, TTL, and mutations all operate.

## Inside a part

A part directory holds, per column, a compressed binary stream (`*.bin`) and a mark file (`*.mrk2`) mapping index marks to byte offsets; plus `primary.idx` (the part's sparse primary index), checksums, partition min-max metadata, and secondary skipping index files if defined. Parts are self-contained: all metadata needed to interpret the data travels with the part, so a query reads the parts that existed when the query started — inserts and merges never corrupt an in-flight scan. Active parts are visible in `system.parts` and via the `_part` virtual column, which exposes the directory name.

```sql
INSERT INTO events (EventDate, UserID) VALUES (today(), 42);
-- creates one part for this INSERT block
SELECT name, rows, bytes_on_disk
FROM system.parts
WHERE active AND table = 'events';
```

**Listing 1.** One INSERT creates one part; `system.parts` lists the physical directories currently serving the table.

## Lifecycle

Background merges continuously combine small parts into larger ones (a form of LSM-like compaction), and a merged part is atomically swapped in while the inputs are retired. Merges are also where lazy work happens: Replacing/Summing/Collapsing merges, TTL moves and drops, and materialization of skipping indexes. Too-frequent small inserts create parts faster than merges retire them, which is exactly [[What causes Too many parts in ClickHouse]] — hence batching or [[What are async inserts in ClickHouse]]. In a [[What is ReplicatedMergeTree]] setup, parts (identified by a content hash block number) are the replication and deduplication unit across replicas.

```d2
insert1: "INSERT\npart 202609_x" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
insert2: "INSERT\npart 202609_y" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
insert3: "INSERT\npart 202609_z" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
merged: "Merged part\nsame rows, sorted\none set of column files" {
  width: 320
  height: 100
  style.fill: "#e8f5e9"
}
insert1 -> merged
insert2 -> merged
insert3 -> merged: background merge
```

**Fig. 1.** Three inserted parts become one merged part; the swap is atomic and queries never see a half-built part.

> [!warning] A part per INSERT is not free
> The per-insert cost is not "one row" — it is one directory with dozens of files, checksums, and an index. INSERTing rows one by one can produce tens of parts per second per table and trip the parts-per-partition limits, so the docs recommend batches of at least tens of thousands of rows or the async insert buffer. This is the single most common ClickHouse production mistake.

> [!tip] Interview answer
> A part is a MergeTree table's storage unit: one INSERT creates one directory with compressed per-column files, mark files, and the sparse primary index. Parts are immutable and self-contained, merged in the background, and they are the unit of replication, TTL, and mutations. Writing too many tiny parts overwhelms merging — that's why batching or async inserts matter.
