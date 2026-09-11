<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka in-sync replica set?

> [!abstract] Short answer
> The in-sync replica set (ISR) is the set of replicas of a partition that are fully caught up to the leader's log end offset. The leader tracks it and drops any follower that has not sent fetches or caught up with the end of the leader's log within `replica.lag.time.max.ms` (default 30000 ms). Only in-sync replicas are eligible for leader election, and a record is considered committed only when every replica in the ISR has applied it to its own log — so with f+1 replicas Kafka tolerates f failures without losing committed records.

## How a replica stays in sync

Under non-failure conditions each partition has a single leader and zero or more followers, and the total number of replicas including the leader is the replication factor. All writes go to the leader, while followers consume messages from the leader exactly as a normal Kafka consumer would and append them to their own logs — pulling lets each follower batch log entries naturally. Broker liveness is defined by two conditions: the broker must maintain an active session with the controller (periodic heartbeats in KRaft mode, timed out by `broker.session.timeout.ms`), and followers must keep replicating the leader's writes without falling "too far" behind. A node satisfying both is called in sync — Kafka deliberately avoids the vague words "alive" and "failed".

```d2
direction: right
leader: "Leader\nlog end offset 120" {
  width: 250
  height: 80
  style.fill: "#e3f2fd"
}
f1: "Follower A\ncaught up at 120" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
f2: "Follower B\nstuck at 105" {
  width: 250
  height: 80
  style.fill: "#fff3e0"
}
f3: "replica.lag.time.max.ms\n(30 s) expires" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
out: "B removed from ISR\nnot eligible for election" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}
leader -> f1: fetch + apply
leader -> f2: fetch + apply
f2 -> f3: no progress
f3 -> out
```

**Fig. 1.** Followers pull from the leader; one that cannot reach the leader's log end offset within `replica.lag.time.max.ms` is evicted from the ISR by the leader.

The leader can also shrink the ISR when a follower lags but keeps its session, and the controller shrinks it when a follower dies and its session is lost. The set is persisted in the cluster metadata whenever it changes, which is what makes any in-sync replica safe to elect. The ISR shrink and expand rates are observable as `IsrShrinksPerSec` and `IsrExpandsPerSec`; outside of broker restarts both are expected to sit at 0, and after a broker comes back its replicas expand the ISR again once they are fully caught up.

## What membership buys you

A write is committed only when all in-sync replicas have applied it, and once committed it will not be lost as long as one broker replicating that partition stays alive. Because the ISR is persisted, every member of it can be elected leader — this is Kafka's alternative to majority-vote quorums: with f+1 replicas Kafka tolerates f failures, the same count a majority quorum needs acknowledgements from, but without requiring 2f+1 disks and writes to carry the throughput cost. Election eligibility has one recent refinement: since Kafka 4.0 the controller may also track Eligible Leader Replicas (ELR), and the promotion order is ISR first, then unfenced ELR members — see [[What is unclean leader election in Kafka]].

> [!warning] acks=all waits for the ISR, not for every assigned replica
> When all replicas are in sync the two sets coincide, but if two of three replicas are down, an `acks=all` write is acknowledged by the single remaining in-sync replica. If you want a floor under how far the ISR may shrink before writes are rejected, that is `min.insync.replicas` — see [[What is min.insync.replicas in Kafka]].

```properties
# how long a follower may lag before eviction from the ISR
replica.lag.time.max.ms=30000
# session timeout between the broker and the controller (KRaft)
broker.session.timeout.ms=9000
```

**Listing 1.** The two timeouts behind the two liveness conditions: replication lag is judged by the leader, session loss by the controller.

A shrinking ISR is also what raises `UnderReplicatedPartitions` on the leader's broker — the mechanics of that alert are in [[What are under-replicated partitions in Kafka]], and the read-side boundary the ISR produces is the high watermark in [[What is the Kafka high watermark]].

> [!tip] Interview answer
> The ISR is the leader's set of followers that are caught up with its log end offset within `replica.lag.time.max.ms`. Only ISR members can become leader, and a record counts as committed when the whole ISR has it, which is why f+1 replicas survive f failures. The set is persisted in cluster metadata, so election never picks a replica that is missing committed records.

