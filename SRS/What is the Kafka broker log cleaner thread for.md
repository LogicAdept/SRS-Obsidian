<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka broker log cleaner thread for?

> [!abstract] Short answer
> It is the background machinery that actually performs log compaction: a pool of cleaner threads on the broker that rewrites the "dirty" part of compacted topics' logs, dropping records whose key already has a newer value in the clean tail — the mechanism behind `cleanup.policy=compact` ([[What is Kafka log compaction]]).

## What the cleaner actually does

```d2
direction: right
head: "Dirty head\nrecent records,\nmay contain superseded keys" {
  width: 240
  height: 100
  style.fill: "#ffebee"
}
clean: "Clean tail\nlast value per key,\nnever rewritten" {
  width: 230
  height: 100
  style.fill: "#e8f5e9"
}
map: "Offset-position summary\ncompact hash table\n~24 bytes per key" {
  width: 250
  height: 100
  style.fill: "#e3f2fd"
}
out: "Rewritten segments\nhead minus dead keys" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
head -> map: build summary
head -> out: copy keeping\nlast per key
clean -> out: copied through
```

**Fig. 1.** The cleaner picks the log with the best head-to-clean ratio, builds a space-compact hash table of the head's keys, and recopies the head — the clean tail is copied through untouched, so compaction never rewrites the whole log.

Log compaction is the retention policy that keeps at least the last value for every key; the log cleaner is the broker-side pool of background threads that does the rewriting ([[What is Kafka log compaction]]). Each compactor thread selects an eligible log — one with `cleanup.policy=compact` whose uncompacted head is large enough by `min.cleanable.dirty.ratio` — builds an offset-position summary of the head in a compact hash table (about 24 bytes per entry: with 8 GB of cleaner buffer one pass can cover roughly 366 GB of head at 1 KB messages), and then recopies the log segments, skipping records whose key appears later in the log. The active segment is never compacted, and tombstones get special handling: the record itself is removed after `log.cleaner.delete.retention.ms`, so consumers of a compacted topic still see deletes for a bounded window ([[What is a Kafka tombstone record]]).

## The knobs that shape it

```properties
cleanup.policy=compact                    # topic-level: cleaner works here
log.cleaner.enable=true                   # broker default: pool is running
min.cleanable.dirty.ratio=0.5             # clean only when head is 50% of log
log.cleaner.min.compaction.lag.ms=0       # keep recent records uncompacted
log.cleaner.max.compaction.lag.ms         # deadline forcing compaction
log.cleaner.delete.retention.ms=86400000  # tombstones linger one day
log.cleaner.io.max.bytes.per.second       # throttle rewriting I/O
```

**Listing 1.** The cleaner's lease of life: topic policy flags it in, broker settings bound its memory, lag windows, and I/O rate.

The lag windows exist because compaction is destructive: `min.compaction.lag.ms` protects recent records from being collapsed while consumers may still be catching up, and `max.compaction.lag.ms` prevents a low-traffic topic from never crossing the dirty-ratio threshold and growing unbounded — though the deadline is not a hard guarantee, since it depends on cleaner thread availability. The cleaner throttles its own I/O so rewriting does not starve the data path; monitoring watches uncleanable-partitions-count and max-compaction-delay metrics ([[What Kafka metrics do you monitor in production]]). This machinery is also what makes Kafka Streams' changelog topics and Kafka's own internal state restorable: a compacted changelog replays into the full current state ([[What is Kafka log compaction]]).

> [!warning] Compaction is per key, not per record, and it keeps "at least" the last value
> Records with no key are simply not compactable, and duplicate keys can temporarily survive in the log — the cleaner guarantees at least the latest value, never exactly one record per key at every instant. Building state machines that assume a single record per key must tolerate the changelog's transient history.

> [!tip] Interview answer
> The log cleaner is the broker's pool of background compactor threads: for topics with cleanup.policy=compact it recopies the dirty head of each log, dropping records superseded by a newer value of the same key, keeping the clean tail and the active segment untouched. Tombstones expire after delete.retention.ms. It is memory- and I/O-throttled, and it is what makes compacted topics usable as restorable state stores.

