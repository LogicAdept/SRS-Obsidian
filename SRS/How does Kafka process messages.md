<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How does Kafka process messages?

> [!abstract] Short answer
> A record's life is three stages: a producer appends it to the tail of a partition log on the partition leader, replication copies it to follower brokers and the high watermark advances, and consumers fetch it from the leader by offset. Storage is sequential file appends served through the OS page cache, so the same path scales from ingest to replay ([[What are the main components of Apache Kafka]]).

## The path of one record

```d2
direction: right
p: "Producer\npartitioner picks p" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
leader: "Partition leader\nappend to log tail" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
followers: "Followers\nfetch + ack" {
  width: 200
  height: 90
  style.fill: "#fff3e0"
}
hw: "High watermark\nadvances" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
c: "Consumer\nfetch by offset" {
  width: 210
  height: 90
  style.fill: "#e3f2fd"
}
p -> leader
leader -> followers
followers -> hw
hw -> c: visible up to HW
```

**Fig. 1.** Produce → replicate → advance the watermark → consume: a record becomes visible to consumers only when the leader has decided it is committed ([[What is the Kafka high watermark]]).

On the produce side, the record is assigned to a partition — explicitly, or by hashing the key, or by the sticky partitioner when neither exists — and sent to that partition's leader, which appends it to the last segment of its log ([[How does a Kafka producer send a record internally]]). The append is a sequential write to disk buffered by the page cache; durability to followers, not fsync, is the main durability lever, which is why `acks=all` with `min.insync.replicas` matters ([[What is the difference between Kafka acks 0 1 and all]], [[What is min.insync.replicas in Kafka]]). Followers pull the same records and acknowledge them; once all in-sync replicas have the record, the leader advances the high watermark and consumers see it.

## Storage: a log of segments, not a queue of messages

Physically a topic partition is a directory of segment files named by the offset of their first record; writes always go to the active segment, which rolls over at a configured size. Reads give a 64-bit offset plus a max chunk: the broker locates the segment, computes the file-relative position, and streams the bytes — a binary search over an in-memory range index, so a read is O(log segments) plus one sequential scan ([[How does Kafka store data on disk as a log]], [[What is a Kafka log segment]]). There is no per-message index and no in-place update: retention deletes whole old segments by time or size, and compaction rewrites segments to keep the last value per key ([[What is Kafka log compaction]]). This shape is what lets the same stored bytes serve a fresh consumer, a lagging consumer, and a replay — the position is just an offset, nothing is removed on read.

## Consumption: fetch, position, commit

Consumers pull: a `fetch` request names a partition and an offset, and the leader responds with records starting there, up to the fetch size cap ([[How do Kafka consumers fetch messages from a broker]]). The client advances its fetch position as records are returned and separately commits positions to the group's offsets topic so a restart resumes in the right place ([[What is Kafka Consumer position for]], [[What is the consumer_offsets topic for]]). Group membership decides which member fetches which partitions, and rebalancing redistributes them as members come and go ([[What triggers a Kafka consumer group rebalance]]).

> [!warning] Consuming does not delete anything
> Kafka has no "remove from queue" operation: reading is non-destructive, and data disappears only by retention, compaction, or explicit topic deletion. Teams used to AMQP brokers are surprised that a consumer that never commits can re-read the same records forever — and that "handled" messages still occupy disk until retention expires.

> [!tip] Interview answer
> A producer appends a record to the tail of the chosen partition's log on the leader; followers replicate it, and the high watermark marks it visible. Storage is size-rolled sequential segment files read through the page cache by offset lookup. Consumers fetch by offset, keep positions in the client, and commit them to the offsets topic — so consume is a cursor move, not a delete, and replay is just seeking to an older offset.

