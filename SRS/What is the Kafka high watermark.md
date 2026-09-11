<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka high watermark?

> [!abstract] Short answer
> The high watermark (HW) is the offset that separates the committed prefix of a partition's log from the still-unreplicated tail: every in-sync replica has applied everything below it. Consumers are only ever given committed messages, so a fetch never returns records at or above the watermark. The leader advances the watermark as followers catch up, and under the strict min ISR rule the watermark cannot advance at all while the ISR is smaller than `min.insync.replicas`.

## How the watermark advances

The leader appends records at its log end offset and hands them to followers, which pull them like ordinary consumers. Each time the in-sync replicas have applied another record, the leader moves the high watermark forward over it. A message is considered committed only when all replicas in the ISR have applied it to their logs — the watermark is precisely the boundary of that committed region. Only committed messages are ever given out to the consumer, so a consumer that races ahead of replication simply sees the partition end at the watermark and polls again later.

```d2
direction: right
log: "Leader log\noffsets 0 … 119" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
leo: "log end offset: 120\nwritten by leader only" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
hw: "high watermark: 117\nreplicated by all ISR" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
consumer: "consumer reads\noffsets below HW" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
log -> leo
leo -> hw: followers catch up
hw -> consumer
```

**Fig. 1.** The tail between the high watermark and the log end offset exists only on the leader until followers replicate it; consumers never see that tail.

Visibility for consumers has two conditions that hold regardless of how the producer acknowledged: the records must be replicated to all in-sync replicas, and the number of in-sync replicas must be no less than the `min.insync.replicas` setting. The second condition is the strict min ISR rule that came in with the Eligible Leader Replicas feature (Kafka 4.0, default on new clusters from 4.1): the high watermark for a partition cannot advance while the ISR is smaller than `min.insync.replicas`, which is what makes previously out-of-sync replicas safe promotion candidates during leader election.

## What the watermark is not

It is not the log end offset — the LEO includes records the leader accepted that followers have not yet applied, and exactly that tail is what `acks=1` can acknowledge and then lose if the leader dies before replication. It is also not the transactional read boundary: for `read_committed` consumers open transactions raise another limit, the last stable offset, so they may read even less than the watermark allows — the mechanics are in [[What does isolation.level read_committed do in Kafka]].

> [!warning] The watermark is a durability boundary, not a lag measurement
> A follower's progress is judged against the leader's log end offset — `replica.lag.time.max.ms` evicts followers that cannot reach the LEO — while the watermark tracks the committed prefix. Treating the HW as "where the slowest follower is" is a popular lie: the leader advances the watermark as soon as the whole ISR has applied the record, and an evicted follower no longer gates it at all. The membership side of that gate is the ISR in [[What is the Kafka in-sync replica set]].

```properties
# the write must be replicated to the whole ISR before
# the record becomes visible to consumers at all
min.insync.replicas=2
acks=all
```

**Listing 1.** The producer-side pair that puts the strict min ISR rule to work: a record only crosses the watermark once every in-sync replica has it and the ISR is at or above the floor.

> [!tip] Interview answer
> The high watermark is the offset below which every in-sync replica has replicated the log — Kafka only hands consumers records below it, which is what makes "committed" concrete. The leader advances it as followers catch up, and since Kafka 4.0 it freezes whenever the ISR drops below `min.insync.replicas`. Records above the watermark exist only on the leader, and that is the part of the log an `acks=1` write can lose.

