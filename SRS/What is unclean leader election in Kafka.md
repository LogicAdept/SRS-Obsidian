<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is unclean leader election in Kafka?

> [!abstract] Short answer
> Unclean leader election is electing a partition leader from a replica that is *not* in the in-sync replica set — a last resort used only when no in-sync replica is available. It is disabled by default (`unclean.leader.election.enable=false`): the out-of-sync replica's log becomes the source of truth even though it is not guaranteed to contain every committed record, so enabling it trades consistency for availability.

## The all-replicas-dead dilemma

Kafka's loss guarantee for committed records holds only while at least one in-sync replica survives. If every replica of a partition is unavailable, a practical system still has to do something, and there are exactly two documented strategies: wait for a replica in the ISR to come back and elect it, hoping its data is intact — which can mean the partition stays offline for as long as those replicas are down, possibly forever if their data was destroyed — or elect the first replica that comes back regardless of sync state, which restores service but may silently rewind the log. Since Kafka 0.11 the default is the first strategy: prefer waiting for a consistent replica. The property `unclean.leader.election.enable` switches the behavior for clusters where uptime beats consistency.

```d2
direction: down
dead: "no in-sync replica\navailable for partition" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
wait: "unclean.leader.election.enable=false\ndefault" {
  width: 340
  height: 90
  style.fill: "#e3f2fd"
}
unclean: "unclean.leader.election.enable=true" {
  width: 340
  height: 90
  style.fill: "#fff3e0"
}
isr: "wait for an ISR replica\npartition unavailable meanwhile" {
  width: 340
  height: 90
  style.fill: "#e8f5e9"
}
any: "first replica back becomes leader\ncommitted records may be lost" {
  width: 360
  height: 90
  style.fill: "#ffebee"
}
dead -> wait
dead -> unclean
wait -> isr
unclean -> any
```

**Fig. 1.** One boolean splits the recovery path: stay unavailable but consistent, or resume on a stale log and accept possible loss of acknowledged records.

In KRaft mode there is an operational wrinkle: enabling this config dynamically does not trigger elections immediately — an unclean-election thread runs periodically (every 5 minutes by default), and if you need it now you run the leader-election tool with the unclean option instead of waiting.

## How Eligible Leader Replicas change the picture

Since Kafka 4.0 the controller tracks an Eligible Leader Replicas (ELR) list per partition, enabled by default on new clusters starting with 4.1 (`eligible.leader.replicas.version=1` opts a server in). Because the strict min ISR rule now freezes the high watermark whenever the ISR is smaller than `min.insync.replicas`, replicas outside the ISR are no longer automatically dangerous — they provably lack nothing that crossed the watermark. During leader election the controller therefore picks in this order: a member of the ISR if one exists, otherwise an unfenced member of the ELR, otherwise the last known leader — the closest behavior to pre-4.0 elections. This shrinks the set of situations where an actually unclean election is the only way out, but it does not change what the flag means when everything is dead.

> [!warning] "Unclean election" and "ELR promotion" are not the same thing
> Promoting an ELR member keeps the committed prefix intact by construction; promoting a random out-of-sync replica under `unclean.leader.election.enable=true` does not — that record may be missing acknowledged messages, and consumers will see previously visible records disappear. The monitoring signal for the difference is `UncleanLeaderElectionsPerSec`, whose healthy value is 0. The replica bookkeeping behind the order is in [[What is the Kafka in-sync replica set]] and [[What is the Kafka controller]].

```properties
# cluster-wide dynamic broker config; default false
unclean.leader.election.enable=false
# typical durability pairing
min.insync.replicas=2
```

**Listing 1.** Leave unclean election off when durability matters, and pair it with a minimum ISR floor so writes fail fast instead of landing on a shrunken ISR — see [[What is min.insync.replicas in Kafka]].

> [!tip] Interview answer
> Unclean leader election lets Kafka promote an out-of-sync replica when no in-sync replica is left, trading correctness for uptime; it is off by default since 0.11 and the tradeoff is explicit in the design docs. With Kafka 4.0 the controller also tracks Eligible Leader Replicas and promotes ISR → ELR → last known leader, which covers most elections cleanly because the strict min ISR rule guarantees ELR members hold everything below the watermark.

