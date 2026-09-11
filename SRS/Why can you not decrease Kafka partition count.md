<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# Why can you not decrease Kafka partition count?

> [!abstract] Short answer
> Because the partition mapping is load-bearing twice: the key hash picks a partition by `hash(key) mod N`, and every record's identity is its offset within a specific partition's log. Shrinking N would remap existing keys onto different partitions and would require deleting replicas' data — so the API only grows: `createPartitions` raises counts, nothing lowers them ([[What happens if you increase Kafka partition count later]]).

## What a decrease would actually break

```d2
direction: down
keys: "Key space\nhash(key) mod 6" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
six: "6 partitions\nk1 -> 3, k2 -> 5, ..." {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
four: "4 partitions\nk1 -> 1, k2 -> 1, ..." {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
lost: "Data in partitions 4 and 5\nunreachable or must be deleted" {
  width: 300
  height: 100
  style.fill: "#ffebee"
}
keys -> six
keys -> four: "decrease mod 6 -> mod 4"
four -> lost
```

**Fig. 1.** The hash partitioning of existing keys changes wholesale when N shrinks: keys that used to map to surviving partitions remap, and the partitions being removed hold data that must either vanish or break the mapping.

Three concrete consequences. First, per-key ordering: the guarantee is that all records of one key land in one partition in produce order; with a changed modulus, the same key starts going to a different partition, and consumers of the new partition see records interleaved without history — the order guarantee silently inverts ([[What ordering guarantees does Kafka provide for messages]], [[Why do Kafka producer keys matter]]). Second, data location: a partition is a log with segments on disk and consumers holding offsets into it; "deleting partitions 4 and 5" means discarding live records — a retention decision, not a resize — and orphaning any committed offsets in `__consumer_offsets` that point at them ([[What is Kafka Consumer position for]]). Third, the protocol has no operation for it: the Admin API's `createPartitions` only increases counts, and the broker treats a lower count as an error — there is no shrunk cluster state to even model, because offsets are partition-local monotonic counters ([[What is the Kafka AdminClient API for]]).

## The growth direction has its own caveats

Growing is supported but is also a remap: new partitions start empty, and the `hash(key) mod N` change means new records for old keys may land elsewhere while old records stay put — the same order caveat in milder form ([[What happens if you increase Kafka partition count later]]). That asymmetry is why partition count is treated as a capacity decision made up front: size it for the next few years of throughput and consumer parallelism, accept a modest over-provision, and leave the headroom rather than planning to "fix it later" in either direction ([[How do you choose the number of partitions for a Kafka topic]]).

> [!warning] There is no supported shrink, only a rebuild
> Teams that truly must reduce partition count rebuild: create a new topic with fewer partitions, migrate data with a copy pipeline or Connect, and switch consumers — accepting a cutover and new offsets. Config tricks do not exist here; anything that looks like in-place shrinking is either unsupported tooling or data loss.

> [!tip] Interview answer
> You cannot decrease Kafka partition count because it would break both identity and ordering: partition assignment is hash-of-key mod N, so shrinking remaps every existing key, and removing partitions means deleting live log data and orphaning committed offsets. The API deliberately only supports createPartitions upward, so partition count is an up-front capacity decision — grow carefully, never plan to shrink.

