<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What Kafka broker settings matter in practice?

> [!abstract] Short answer
> The broker defaults are dev-grade, so a handful of settings decide whether a cluster survives production: the replication trio (`default.replication.factor`, `min.insync.replicas`, `unclean.leader.election.enable`), retention (`log.retention.hours`, `log.segment.bytes`), the thread counts, and topic auto-creation. Most other knobs are performance tuning, not correctness.

## Durability and the auto-create trap

Auto-created topics inherit `num.partitions` (default 1) and `default.replication.factor` (default 1), and auto-creation itself is on (`auto.create.topics.enable=true`). With `min.insync.replicas=1` (default), even `acks=all` producers tolerate one replica copy being the whole ISR. Production clusters usually run replication factor 3 with `min.insync.replicas=2` — the same posture the internal topics get by default (`offsets.topic.replication.factor=3`, `transaction.state.log.replication.factor=3`, `transaction.state.log.min.isr=2`) — and `unclean.leader.election.enable=false` so a stale replica never becomes leader ([[What is unclean leader election in Kafka]], [[What is min.insync.replicas in Kafka]]).

```properties
# replication topology
default.replication.factor=3
min.insync.replicas=2
unclean.leader.election.enable=false   # default false
auto.create.topics.enable=false        # default true; disable and manage topics as code
# retention and storage
log.retention.hours=168                # default: 7 days
log.retention.check.interval.ms=300000 # deletion eligibility is checked every 5 min
log.segment.bytes=1073741824           # 1 GiB segments; retention works per segment
# threads and caps
num.network.threads=3
num.io.threads=8
message.max.bytes=1048588              # broker cap; topic max.message.bytes can override
```

**Listing 1.** The production-posture broker block; comments show the shipped defaults where they differ.

## Throughput and internal topics

`num.network.threads` (3) handles request reading, `num.io.threads` (8) handles disk work; both default sizes are reasonable starting points, and the request handler pool idling under 30% is a saturation signal to watch. Retention is enforced by a periodic check (`log.retention.check.interval.ms`, 5 minutes) over whole segments (`log.segment.bytes`, 1 GiB default) — [[What is a Kafka log segment]] explains the roll. One more practical knob is `group.initial.rebalance.delay.ms` (3 s default), which batches joins of a freshly starting group instead of rebalancing per member.

Internal topics carry their own copies of the durability story and deserve the same review: the consumer-offsets topic is pre-split into 50 partitions by default (`offsets.topic.num.partitions=50`), and both the offsets topic and the transaction-state log ship with replication factor 3 and transaction min ISR 2. These get created on first use with whatever the broker says at that moment, so the broker's durability defaults must already be production-grade before the first client connects, not after. One deliberate non-setting completes the storage picture: Kafka does not flush to disk on its own (`log.flush.interval.messages` defaults to "effectively never") — data lands in the OS page cache and durability comes from replication, which is why forcing frequent flushes only burns throughput without adding safety.

Deletion is also config: `delete.topic.enable` defaults to true, so a topic delete command really removes the topic's data rather than marking it — combined with auto-creation off, topics exist because someone declared them, and disappear when someone deletes them.

> [!warning] A typo can create a one-replica topic
> With auto-creation left on, the first `send()` to a misspelled topic succeeds — and silently provisions that topic with the broker defaults: 1 partition, replication factor 1. The data flows, dashboards stay green, and the topic is unprotected until someone notices. Disable auto-creation on production clusters and create topics explicitly with the replication factor you actually want.

> [!tip] Interview answer
> The settings that matter are the ones that change failure behavior: replication factor and `min.insync.replicas` decide durability with `acks=all`, `unclean.leader.election.enable=false` prevents data loss at the cost of availability, retention settings bound disk usage, and auto-create is usually off because typo topics inherit dev-grade defaults. Everything else is tuning after metrics show pressure.
