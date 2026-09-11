<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka Partitioner interface for?

> [!abstract] Short answer
> `Partitioner` is the pluggable strategy that answers one question for every record that does not already name a partition: which partition does it go to? One method takes the serialized key and value plus cluster metadata and returns a partition index. The built-in default hashes keyed records and sticky-batches keyless ones; you implement the interface to salt hot keys or route by content.

## The contract

```java
public interface Partitioner extends Configurable, Closeable {
    int partition(String topic, Object key, byte[] keyBytes,
                  Object value, byte[] valueBytes, Cluster cluster);
}
```

**Listing 1.** `key` and `keyBytes` are null when the record has no key; `Cluster` exposes the topics and partitions known to the producer. `configure()` receives producer configs, `close()` runs at shutdown.

The producer calls it on the sending thread after serialization, only when the record carries no explicit partition. Which implementation runs is controlled by `partitioner.class`; unset (the default) means the built-in logic inside the client: a key selects a partition as the positive murmur2 hash of the key bytes modulo the partition count — the mapping [[Why do Kafka producer keys matter]] builds on — and a keyless record goes to the sticky partition, which changes only after `batch.size` bytes have been produced to it, keeping null-key streams batchable. `partitioner.ignore.keys=true` forces that keyless path even for keyed records, but it has no effect once a custom partitioner is configured. The other built-in, `RoundRobinPartitioner`, rotates per record; its rotation fragments batches (a documented unevenness issue), which is why sticky logic, not round-robin, is the null-key default.

## When you implement it yourself

Real reasons to override: spreading skewed keys with salting, routing by payload content instead of key, or pinning logical tenants to dedicated partitions. The salting sketch most interviews want:

```java
// Conceptual: record-level salting spreads a hot key's traffic
// across partitions, trading per-key ordering away on purpose
public class SaltedPartitioner implements Partitioner {
    private final Random random = new Random();

    @Override
    public int partition(String topic, Object key, byte[] keyBytes,
                         Object value, byte[] valueBytes, Cluster cluster) {
        int numPartitions = cluster.partitionsForTopic(topic).size();
        int salt = random.nextInt(4); // 4 salt buckets per key
        byte[] saltedKey = ((String) key + salt).getBytes();
        return Utils.toPositive(Utils.murmur2(saltedKey)) % numPartitions;
    }

    @Override
    public void configure(java.util.Map<String, ?> configs) {}

    @Override
    public void close() {}
}
```

**Listing 2.** Conceptual salting partitioner (imports omitted): the salt varies per record, so one key's stream fans out over partitions and downstream code must re-aggregate by the original key.

The choice must stay deterministic for plain routing — a partitioner that scatters one key's records across partitions over time breaks the same-key-same-partition invariant that downstream ordering and log compaction rely on ([[What ordering guarantees does Kafka provide for messages]]). Note also that any hash-based mapping is tied to the current partition count, so scaling the topic re-maps keys — [[What happens if you increase Kafka partition count later]].

> [!warning] A custom partitioner can silently break ordering and compaction
> Nothing in the interface stops an implementation from sending the same key to different partitions at different times. Per-key processing and compaction both assume a key lives in exactly one partition, and a randomized or stateful partitioner violates that assumption with no error at produce time. Mapping many keys onto few partitions, in turn, hand-builds [[What is a hot partition in Kafka]].

> [!tip] Interview answer
> The Partitioner is the strategy interface behind partition selection: one method, serialized key/value plus cluster metadata in, partition index out, invoked only when the record does not name a partition. The default is murmur2-hash for keyed records and sticky batching for keyless ones; implement it to salt hot keys or route by content — deterministically, or per-key ordering and compaction break.
