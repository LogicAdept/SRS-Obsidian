<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What Kafka topic settings matter in practice?

> [!abstract] Short answer
> Two decisions happen at creation — partition count and replication factor; the rest are per-topic overrides of broker defaults: retention (`retention.ms`/`retention.bytes`), `cleanup.policy`, segment sizing, `min.insync.replicas`, and `max.message.bytes`.

## Creation time and per-topic overrides

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders \
    --partitions 20 --replication-factor 3 \
    --config retention.ms=604800000 --config min.insync.replicas=2
```

**Listing 1.** The creation-time decisions: partition count (consumer parallelism ceiling), replication factor, and any config overrides. The docs recommend a factor of 2–3; with 3 the topic survives two broker failures.

Partition count is the one setting that is painful to revisit — consumers cannot exceed it, and growing it later re-maps keys ([[What happens if you increase Kafka partition count later]], [[How do you choose the number of partitions for a Kafka topic]]). Retention is two-dimensional by default: `retention.ms` (7 days) and `retention.bytes` (-1, unlimited) with `cleanup.policy=delete`; `compact` switches to key-based retention for state topics ([[What is Kafka log compaction]]), where `delete.retention.ms` (1 day) bounds how long tombstones survive ([[What is a Kafka tombstone record]]). Retention is enforced per segment — `segment.bytes` (1 GiB) and `segment.ms` (7 days) decide how much margin the clock has ([[What is a Kafka log segment]]). Durability can be tightened per topic with `min.insync.replicas` — pair 2 with replication factor 3 ([[What is min.insync.replicas in Kafka]]) — and `max.message.bytes` (1048588) caps record size per topic, overriding the broker's `message.max.bytes`.

Precedence is worth stating out loud: per-topic configs override broker defaults, so a topic-level `min.insync.replicas` or retention sticks even if the broker later changes its default — which is exactly why explicit topic creation beats relying on whatever the broker currently ships. Two smaller per-topic knobs round out the picture: `compression.type` defaults to `producer` (keep whatever the producer chose; set `gzip`/`lz4`/`zstd` to force, or `uncompressed` to forbid), and `message.timestamp.type` picks `CreateTime` (default) or `LogAppendTime` — the field downstream consumers and time-based retention actually read.

```d2
direction: down
policy: "cleanup.policy?" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
del: "delete — time/size window\nretention.ms (7 d), retention.bytes\nwhole-segment removal" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
comp: "compact — keep latest per key\nmin.cleanable.dirty.ratio (0.5)\ndirty segment share to trigger cleaning" {
  width: 340
  height: 90
  style.fill: "#fff3e0"
}
both: "delete,compact — hybrid\nwindow first, then compaction" {
  width: 280
  height: 70
  style.fill: "#f3e5f5"
}
tomb: "tombstones kept\ndelete.retention.ms (1 d)" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
policy -> del: stateless events
policy -> comp: keyed state
comp -> tomb
policy -> both
```

**Fig. 1.** The cleanup-policy choice and its companion knobs: events live on a time/size window, keyed state compacts to the latest value per key, and tombstones get their own shorter retention inside compacted topics.

> [!warning] Time-only retention has no size ceiling
> `retention.bytes=-1` means nothing bounds the topic but the 7-day clock. One traffic spike or a broken consumer that stops draining compacted segments, and disks fill before retention does anything — the partition then degrades further ([[What happens when a Kafka broker disk fills up]]). Size-critical topics get both dimensions: a `retention.bytes` that matches disk headroom and the time cap.

> [!tip] Interview answer
> At creation I fix partitions for parallelism headroom and replication factor 3; then per topic I set retention in both dimensions — time and bytes — pick delete versus compact for the cleanup policy, and raise `min.insync.replicas` to 2 wherever the producer uses acks all. The two failure modes to remember: growing partitions later breaks key-to-partition mapping, and time-only retention leaves disk usage unbounded.
