<!--
reps: 0
priority: 0
-->
#Databases/Indexes #Databases/NoSQL #SRS

# What are SSTables and LSM trees

> [!abstract] Short answer
> An SSTable is an immutable, sorted file of key-value pairs with a block index. An LSM-tree is a write-optimized index design that buffers writes in a memory component and periodically flushes and merges them into a cascade of SSTables on disk. It trades slower reads and background compaction for very fast sequential writes.

## Where the names come from

SSTable (sorted string table) comes from Google's Bigtable paper: it is a file containing a sequence of sorted, immutable key-value pairs, organized into blocks with a block index loaded into memory, so lookups find the right block with one disk read. The LSM-tree comes from O'Neil, Cheng, Gawlick, and O'Neil's 1996 paper "The Log-Structured Merge-Tree": a disk-based data structure for low-cost indexing under heavy inserts, which defers and batches index changes, cascading them from a memory component through one or more disk components in a merge-sort-like manner, keeping all entries retrievable from either component meanwhile.

## The write and read paths

Writes go to the memory component (RocksDB calls it the memtable; Bigtable, a commit log plus memtable) and are appended to a write-ahead log for durability. When memory fills, the sorted contents flush as a new SSTable at the youngest level. Reads must check the memtable and then the levels, newest first, stopping at the first match; because a key can live in several SSTables, engines keep bloom filters per file to skip files that cannot contain the key. Background compaction merges overlapping SSTables, dropping overwritten and deleted entries; RocksDB's leveled style keeps L0 files small and overlapping and deeper levels as non-overlapping runs about ten times larger each.

```d2
direction: right
write: "PUT k=v" {
  width: 160
  height: 70
  style.fill: "#e3f2fd"
}
mem: "Memtable (sorted)\n+ WAL" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
l0: "L0 SSTables\noverlapping" {
  width: 200
  height: 90
  style.fill: "#ffebee"
}
ln: "L1..L6\nnon-overlapping runs" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
write -> mem
mem -> l0: "flush"
l0 -> ln: "compaction merges"```

**Fig. 1.** Writes land in the memtable, flush into young SSTables, and background compaction merges them into deeper, larger, non-overlapping runs.

## Why engines choose it, and what it costs

For write-heavy histories, logs, and time-series tables, avoiding per-insert random page updates to a B-tree is decisive; the LSM paper's motivation was exactly that B-tree maintenance could double insert I/O. The cost is read amplification (checking multiple components), write amplification during compaction (each key rewritten several times), and compaction CPU/IO pressure. RocksDB documents both effects and uses per-SST bloom filters and compaction tuning to control them; this is the storage engine underneath Cassandra and RocksDB-based stores. It is the write-optimized counterpart to the B-tree families in [[What types of database indexes exist]], while ClickHouse keeps the sorted-parts idea with a different, sparse index read model in [[What is a sparse primary index in ClickHouse]].

> [!warning] "LSM reads are slow" and "LSM has no indexes" are both wrong
> Reads are not linear scans: each SSTable is sorted with a block index, and bloom filters eliminate most irrelevant files. The real trade-offs are compaction-driven write amplification and tail-latency pressure, plus tombstone handling. Conversely, claiming LSM engines have no indexes ignores that the SSTable cascade plus per-file indexes and bloom filters is itself an index structure.

> [!tip] Interview answer
> An SSTable is an immutable sorted key-value file with a block index, a term from Bigtable. An LSM-tree buffers writes in a memtable, flushes it as SSTables, and compacts them into larger sorted runs, trading read amplification and compaction work for fast sequential writes. It is the standard storage design for write-heavy stores like RocksDB and Cassandra, and bloom filters per file keep point reads cheap.
