<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is Kafka log compaction?

> [!abstract] Short answer
> A retention mode (`cleanup.policy=compact`) where the log keeps, **for every key, at least its latest value**: background cleaner threads recopy closed segments and drop records whose key has a newer one. The recent uncompacted head keeps everything; ordering and original offsets are preserved; deletes are tombstones. Used for `__consumer_offsets`, changelog topics, and keyed state that must survive restarts.

## How the cleaner works

Compaction runs on **closed segments only**: the active segment keeps appending. The cleaner (a pool of background threads) picks logs by dirty ratio, builds an index of the newest offset per key from the clean part, then rewrites the dirty segments dropping superseded keys — throttled, and without blocking reads. Cleaning is triggered when the dirty part exceeds `min.cleanable.dirty.ratio` (default 0.5), bounded by `min.compaction.lag.ms` and `max.compaction.lag.ms`; the offset of any record never changes even after records around it vanish.

A real run on Kafka 4.3.1 — topic created with `cleanup.policy=compact`, three keys written three times each, then one more key:

```console
$ kafka-configs.sh --bootstrap-server localhost:9092 --describe --topic users-compact
Dynamic configs for topic users-compact are:
  cleanup.policy=compact sensitive=false synonyms={DYNAMIC_TOPIC_CONFIG:cleanup.policy=compact, DEFAULT_CONFIG:log.cleanup.policy=delete}
  delete.retention.ms=100 sensitive=false synonyms={DYNAMIC_TOPIC_CONFIG:delete.retention.ms=100, DEFAULT_CONFIG:log.cleaner.delete.retention.ms=86400000}
  min.cleanable.dirty.ratio=0.01 sensitive=false synonyms={DYNAMIC_TOPIC_CONFIG:min.cleanable.dirty.ratio=0.01, DEFAULT_CONFIG:log.cleaner.min.cleanable.ratio=0.5}
  segment.ms=3000 sensitive=false synonyms={DYNAMIC_TOPIC_CONFIG:segment.ms=3000}
```

**Listing 1.** The topic overrides: compact policy, a tiny dirty-ratio threshold, and short segments to force the demo.

```console
$ kafka-console-consumer.sh --bootstrap-server localhost:9092 \
    --topic users-compact --from-beginning --timeout-ms 10000 \
    --formatter-property print.key=true
k1	k1=v3
k2	k2=v3
k3	k3=v3
k4	k4=v1
```

**Listing 2.** Twelve records were written (k1–k3 × v1–v3, then k4); a consumer reading from offset 0 now sees only the newest value per key — the "final state" view compaction guarantees.

## What compaction guarantees

A consumer starting at offset 0 sees **at least the final state** of every key, in write order; a caught-up consumer sees every written record including all intermediate values. Order is never rearranged, only thinned. Reads at removed offsets return the next surviving record, as explained in [[How does Kafka store data on disk as a log]]; the delete path through [[What is a Kafka tombstone record]] is what makes "remove this key" possible at all.

> [!warning] Compaction is not deletion, and keys are per partition
> A `compact`-only topic never discards data by age: with unbounded key cardinality the log grows forever, and real setups usually pick `cleanup.policy=compact,delete`. And compaction is per partition — the same key on different partitions keeps a copy in each, so "one latest value per key" only holds if a key lives on one partition.

> [!tip] Interview answer
> Log compaction keeps the most recent value for each key instead of time-bounding the log: background cleaner threads rewrite closed segments, dropping superseded keys while preserving order and offsets. Consumers from offset 0 get at least the final state per key, and deletes happen via tombstones that live for delete.retention.ms. It's the storage model behind __consumer_offsets and Streams changelogs.

