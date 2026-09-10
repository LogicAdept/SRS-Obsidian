<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the consumer_offsets topic for?

> [!abstract] Short answer
> `__consumer_offsets` is the internal compacted topic where the group coordinator durably stores committed offsets — and the group's membership metadata. It is what lets a consumer restart, or a replacement take over after a crash, and resume exactly where the last commit happened.

## The commit path through it

When the coordinator receives an offset commit, it appends the request to `__consumer_offsets` and sends the successful response only after all replicas of that offsets partition have received the append; if replication does not finish within the timeout, the commit fails and the consumer retries after backing off. The durability story is the same log replication that governs any partition — the replica mechanics live in [[What is the Kafka in-sync replica set]].

The topic is **compacted**, because only the most recent commit per group-plus-partition key matters: compaction keeps the latest record per key so the log never grows with history. The coordinator additionally caches the latest offsets in an in-memory table to serve offset fetches quickly; if the coordinator has just loaded the offsets partition — after a broker restart or a leadership change — fetches fail with `CoordinatorLoadInProgressException` until the load finishes, and the consumer retries. The coordinator itself is found per group: groups are assigned to coordinators based on their group names, discovered via a `FindCoordinator` request — see [[What is a Kafka consumer group coordinator for]].

```d2
direction: right
c: "consumer\ncommitSync()" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
coord: "coordinator\n(broker for this group)" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
log: "__consumer_offsets\ncompacted, replicated\nkey = group + partition" {
  width: 300
  height: 110
  style.fill: "#e8f5e9"
}
cache: "in-memory offsets cache\nserves future fetches" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
c -> coord
coord -> log: append, wait for replicas
log -> cache
```

**Fig. 1.** A commit is not acknowledged until it is replicated into the offsets log; the coordinator's cache then answers later offset fetches without re-reading the log.

## What lives in it beyond offsets

Modern groups store more than raw offsets there: the coordinator keeps the group's membership and protocol state in the same internal-storage family, which is why broker restarts can rebuild group state by replaying these logs. The topic is managed entirely by the broker: partitions, replication and cleanup follow the broker configs, and the operational rule is strict — never manually increase partitions for `__consumer_offsets`, because that breaks coordinator mapping logic and can corrupt group state. For inspection, use the tooling rather than a raw consumer: `kafka-consumer-groups --describe` reads committed offsets and lag through the admin path, and `--reset-offsets` can move a group's stored offsets — the same mechanism you would use to rewind, described in [[How do you replay Kafka messages from an older offset]].

> [!warning] Treat it as infrastructure, not as a topic you read
> Reading `__consumer_offsets` with a normal consumer to "find where my group is" fails to pay off: the records are binary offset-commit messages and the internal format is not an API. Use `kafka-consumer-groups --describe` or the AdminClient. And because offset commits wait for the offsets partition's replicas, an unavailable `__consumer_offsets` replica set stalls commits group-wide — commits are only as durable as that internal topic's replication.

> [!tip] Interview answer
> __consumer_offsets is the compacted internal topic backing consumer groups: the coordinator appends each offset commit there, acknowledges only after the append is replicated, and serves offset fetches from its in-memory cache. Compaction keeps the latest commit per group-partition key, group state is rebuilt from it after failures, and you never touch it directly — describe, reset and monitor groups through kafka-consumer-groups or the AdminClient instead.

