<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is a Kafka log segment?

> [!abstract] Short answer
> The partition log is **split into segment files**: each segment is one `.log` file named by its **base offset**, with an offset index and a time index beside it. Appends go only to the **active segment**; when it reaches `segment.bytes` (default 1 GiB) or lives past `segment.ms` (default 7 days), it closes and a new one starts. Retention and compaction operate on whole segments.

## Base offsets and roll

A segment file name is the offset of its first record, so scanning a partition directory tells you the log's history at a glance. Here a compacted test topic rolled after `segment.ms=3000` forced a new segment while ten records had been appended (Kafka 4.3.1):

```console
$ ls /var/lib/kafka/data/users-compact-0
00000000000000000000.index
00000000000000000000.log
00000000000000000000.timeindex
00000000000000000009.index
00000000000000000009.log
00000000000000000009.snapshot
00000000000000000009.timeindex
leader-epoch-checkpoint
partition.metadata
```

**Listing 1.** Two segments: the first holds offsets 0–8, the active one starts at offset 9. `.snapshot` files track producer state for the segment.

The `.index` file maps a record's offset, relative to the segment base, to a position in the `.log` file, so lookups are a binary search plus a short scan; `.timeindex` answers "give me the log as of 14:00". Index entries are sparse — `index.interval.bytes` (default 4096) adds an index entry roughly every 4 KiB of log, trading a slightly longer final scan for a small index. Index files are preallocated (`segment.index.bytes`, 10 MiB by default) and shrink back to the used size when the segment rolls, so a growing active segment does not re-grow its index on every append. The `.snapshot` files record producer-state (producer id, sequence numbers) so idempotence and transactions survive a broker restart.

Because cleanup works a file at a time, segment size is really a retention-granularity knob: smaller segments delete and compact more precisely but multiply file handles and index overhead — this trade-off is part of [[How does Kafka store data on disk as a log]].

## Why segments matter for ops

Retention (delete) drops whole segments once their newest record ages out, and the log cleaner rewrites closed segments when compacting; the active segment is never touched by either, which is why a topic with one huge active segment keeps "deleted" data until new appends roll the file. `segment.bytes` is therefore also the main lever for bounding the tail of a compacted topic ([[What is Kafka log compaction]]). For inspection, `kafka-dump-log.sh` decodes the batches inside a segment and `kafka-log-dirs.sh` reports per-partition sizes, so segment boundaries stay visible during day-to-day debugging.

Note also what the listing did not show: there is exactly one active segment per partition at any moment, and its file name keeps moving forward as rolls happen. Anything that pauses appends — an idle topic, a stalled producer — also pauses rolling, which is the innocent explanation for most "retention is broken" reports.

> [!warning] segment.bytes has a hard floor of 1 MiB
> Asking for tiny segments fails at topic creation — Kafka 4.3.1 rejects it with `Invalid value 256 for configuration segment.bytes: Value must be at least 1048576`. To roll frequently for testing, lower `segment.ms` (which has no such floor) instead of `segment.bytes`.

> [!tip] Interview answer
> A segment is one data file of a partition log named by its base offset, plus offset and time indexes; appends go to the single active segment until it hits segment.bytes or segment.ms. Segments are the unit of deletion and compaction, so their size controls how granular retention is. The active segment never gets cleaned, which surprises people waiting for old data to disappear.

