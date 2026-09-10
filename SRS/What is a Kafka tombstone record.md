<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is a Kafka tombstone record?

> [!abstract] Short answer
> A record with a **non-null key and a null value**. On a compacted topic it is the delete operation: it removes prior values of that key from the compacted log. The marker itself stays readable for `delete.retention.ms` (default 24 hours) so consumers can observe the deletion, after which the cleaner removes it together with the key's older records.

## Sending and observing one

A tombstone is produced by writing a `ProducerRecord` whose value is null — with the raw client, a console producer emitting an explicit null, or a connector emitting a deletion event. On a compacted topic on Kafka 4.3.1, `key=k2 value=null` was sent after k2 already had values:

```console
$ kafka-console-consumer.sh --bootstrap-server localhost:9092 \
    --topic users-compact --from-beginning --timeout-ms 10000 \
    --formatter-property print.key=true
k1	k1=v3
k2	k2=v3
k3	k3=v3
k4	k4=v1
k2	null
```

**Listing 1.** The tombstone arrives as the last record, printed with a literal `null` value — and at this moment the log still contains k2's older values behind it.

After the cleaner's next pass over the closed segment, the superseded k2 values are gone while the marker may still sit in the log until its retention window and the next pass clear it. A caught-up consumer sees the delete; a consumer lagging longer than `delete.retention.ms` can miss the marker entirely and keep the pre-delete state, because marker removal happens concurrently with reads.

## How deletion completes

The sequence is: values for the key are written; a tombstone deletes the key; the marker stays readable for `delete.retention.ms` (default 24 hours) so consumers reading from offset 0 have time to observe the deletion; after the window, the next cleaner pass removes the marker and the key's older values together. The same setting doubles as a read bound: `delete.retention.ms` is also the time a consumer scanning from offset 0 must finish its read to get a valid snapshot — scan slower than that and the marker may be collected mid-scan. The mechanics sit on top of ordinary log storage ([[How does Kafka store data on disk as a log]]) and only come into force on topics with [[What is Kafka log compaction]] enabled. A tombstone's batch also carries a `deleteHorizonMs` stamp — the moment removal becomes eligible — which the log dump tool prints; ordinary batches show it as empty.

One more subtlety: the marker is a record like any other, so it has an offset, participates in ordering, and is duplicated to followers. Anyone replaying the log sees the delete in its historical position, which is exactly what makes tombstone-based deletes safe to reprocess.

## Semantics to state precisely

The tombstone means "this key is deleted", not "this value is empty": an empty string value is a normal record and compact keeps it as the latest value. And a tombstone only affects the partition it was written to — with a null key it is meaningless, because compaction groups records by key per partition. In integration pipelines, Connect source connectors emit tombstones to mirror row deletes, and stream processors emit them when a state-store entry is removed, so downstream compacted topics converge to the same key set.

> [!warning] Empty string is not a tombstone
> Feeding `user-7:` to the console producer with `parse.key=true` sends an **empty-string value**, not a null — the consumer shows it as an empty payload and compaction keeps it. The delete must carry an actual null value; when in doubt, verify with `--formatter-property print.key=true` that the record prints `null`.

> [!tip] Interview answer
> A tombstone is a keyed record with a null value; on compacted topics it marks the key deleted, and after delete.retention.ms the cleaner drops both the marker and the key's older records. Consumers must see the marker before that window closes, or they miss the deletion. It's a null value, not an empty string, and it only applies to the partition it lands on.

