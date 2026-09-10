<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How does Kafka store data on disk as a log?

> [!abstract] Short answer
> Each partition is an **append-only log on disk**: writes go to the end of the active segment file, never in place; every record gets a sequential **offset** that never changes. Reads use per-segment indexes to jump to a file position, and I/O is mostly sequential with the OS page cache in front — durability comes from replication, not from syncing every record.

## On-disk layout

One directory per partition, one file set per segment: the data file `.log`, the offset-to-position index `.index`, the timestamp index `.timeindex`, plus `leader-epoch-checkpoint` and `partition.metadata`. The listing below is a real single-partition topic on a Kafka 4.3.1 broker:

```console
$ ls /var/lib/kafka/data/orders-0
00000000000000000000.index
00000000000000000000.log
00000000000000000000.timeindex
leader-epoch-checkpoint
partition.metadata
```

**Listing 1.** A partition directory with one fresh segment: the base offset (0) is the segment file name.

Records are appended as **record batches**; the dump tool shows one:

```console
$ kafka-dump-log.sh --files orders-0/00000000000000000000.log --print-data-log
Log starting offset: 0
baseOffset: 0 lastOffset: 2 count: 3 baseSequence: 0 lastSequence: 2 producerId: 3000 producerEpoch: 0 partitionLeaderEpoch: 0 isTransactional: false isControl: false deleteHorizonMs: OptionalLong.empty position: 0 CreateTime: 1789062150202 size: 132 magic: 2 compresscodec: none crc: 4162661697 isvalid: true
| offset: 0 CreateTime: 1789062150189 keySize: 2 valueSize: 13 sequence: 0 headerKeys: [] key: u1 payload: order-created
| offset: 1 CreateTime: 1789062150202 keySize: 2 valueSize: 18 sequence: 1 headerKeys: [] key: u2 payload: payment-authorized
| offset: 2 CreateTime: 1789062150202 keySize: 2 valueSize: 13 sequence: 2 headerKeys: [] key: u1 payload: order-shipped
```

**Listing 2.** Three records in one batch: sequential offsets, a per-batch CRC, and compression recorded per batch, not per record.

## Reads, flushes, retention

A read by offset first finds the right segment, then binary-searches its `.index` for the file position and scans forward. Kafka groups writes and lets the OS page cache absorb them, so throughput stays nearly constant as the log grows; forced per-message fsync is not the model — the flush settings exist for special cases, and normal durability is `acks=all` with enough in-sync replicas. Old data leaves by **retention** (time or size per topic) deleting whole segments, or by [[What is Kafka log compaction]] keeping the latest value per key; segments themselves are described in [[What is a Kafka log segment]].

> [!warning] Offsets are permanent, even where records are gone
> Compaction and retention remove records but never renumber offsets: a read at a compacted-away offset silently returns the next surviving record. Code that treats offsets as dense counters, or assumes `logEndOffset - earliest == record count`, will drift.

> [!tip] Interview answer
> Kafka stores each partition as an append-only sequence of segment files with offset and time indexes beside them, writing only at the end and reading by binary search through an index. It leans on sequential I/O and the page cache instead of per-record fsync, and guarantees durability through replicas. Data leaves the log by retention deleting whole segments or by compaction keeping the latest per key — offsets themselves never change.

