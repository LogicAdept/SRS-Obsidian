<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How is a Kafka topic structured?

> [!abstract] Short answer
> A topic is a **named log split into partitions**. Each partition is an independent append-only log with its own offset sequence, hosted on one leader broker with follower replicas. A record carries key, value, timestamp, and headers, and lands on exactly one partition — records with the same key always go to the same partition, which is where per-key ordering comes from.

## Partitions, leaders, replicas

The partition count is the topic's unit of parallelism: producers write to partitions concurrently, consumer group members each own a subset of partitions, and throughput scales with partition spread across brokers. Every partition has one **leader** (all reads and writes) plus followers for fault tolerance; replication factor 3 is the common production shape. Reading a topic means reading its partition logs, as [[What is Apache Kafka]] puts it — the topic itself is just a name over them.

```console
$ kafka-topics.sh --bootstrap-server localhost:9092 \
    --describe --topic payments
Topic: payments	TopicId: pEAVk4NpS3Kt4uth9CUNEA	PartitionCount: 3	ReplicationFactor: 1	Configs: min.insync.replicas=1,segment.bytes=1073741824
	Topic: payments	Partition: 0	Leader: 1	Replicas: 1	Isr: 1	Elr: 	LastKnownElr:
	Topic: payments	Partition: 1	Leader: 1	Replicas: 1	Isr: 1	Elr: 	LastKnownElr:
	Topic: payments	Partition: 2	Leader: 1	Replicas: 1	Isr: 1	Elr: 	LastKnownElr:
```

**Listing 1.** Real output from Kafka 4.3.1: three partitions, and per partition the leader broker, the replica list, and the in-sync replica set. With replication factor 3 the Replicas and Isr columns would each list three broker ids.

```d2
direction: down
topic: "topic payments" {
  width: 200
  height: 44
  style.fill: "#fff3e0"
}
p0: "partition 0\nleader on broker 1" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
p1: "partition 1\nleader on broker 1" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
p2: "partition 2\nleader on broker 1" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
log0: "log: 0, 1, 2…" {
  width: 170
  height: 44
  style.fill: "#e8f5e9"
}
topic -> p0
topic -> p1
topic -> p2
p0 -> log0
```

**Fig. 1.** The topic fans out into partition logs; each log is an independent ordered sequence, and each would carry its own replicas on other brokers.

## Keys choose partitions

When a record has a key, the producer hashes it (murmur2 by default) and maps the result onto the partition count, so the same key always reaches the same partition — and Kafka guarantees a consumer reads a partition in exactly the write order. Keyless records are spread by sticky round-batching instead, as [[Why do Kafka producer keys matter]] details.

> [!warning] Changing the partition count re-buckets keys
> The mapping is `hash(key) % N`; after you raise N, the same key hashes to a different partition, so per-key order across the resize is broken and old records live in a different partition than new ones. If a consumer relies on per-key ordering, treat [[What happens if you increase Kafka partition count later]] as a migration decision, not a knob.

> [!tip] Interview answer
> A topic is a logical stream made of N partitions, each an append-only log with its own offsets, one leader broker, and follower replicas that form the ISR. Keys map onto partitions by hash, which gives per-partition and per-key ordering; the partition count is the parallelism and, implicitly, the ordering budget. Describe output shows each partition's leader, replicas, and in-sync set.

