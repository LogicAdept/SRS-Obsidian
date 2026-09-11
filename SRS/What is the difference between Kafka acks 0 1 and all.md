<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the difference between Kafka acks 0 1 and all?

> [!abstract] Short answer
> `acks` controls how many acknowledgements the leader must receive before the producer considers a request complete. `acks=0` waits for nothing — the record is considered sent the moment it hits the socket buffer. `acks=1` waits only for the leader to write it to its own log. `acks=all` waits for the full in-sync replica set and is the strongest available guarantee, which is why it is the default since Kafka 3.0 and required by idempotence.

## The three settings by what can be lost

With `acks=0` the producer adds the record to the socket buffer and moves on: no guarantee exists that the server received it, retries cannot take effect because the client never learns of failures, and the returned offset is always -1. With `acks=1` the leader appends the record to its local log and responds without waiting for followers — if the leader fails immediately after acknowledging but before any follower replicates, the record is lost. With `acks=all` the leader waits for the full set of in-sync replicas to acknowledge, and the record will not be lost as long as at least one in-sync replica remains alive. Latency and throughput run in the same order: 0 is fastest, all is slowest, and the difference is network round-trips to followers.

```d2
direction: right
p: "producer\nsends record" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
a0: "acks=0\nno wait, offset -1" {
  width: 250
  height: 80
  style.fill: "#ffebee"
}
a1: "acks=1\nleader's log only" {
  width: 250
  height: 80
  style.fill: "#fff3e0"
}
aa: "acks=all\nwhole ISR acks" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
p -> a0
p -> a1
p -> aa
```

**Fig. 1.** Three ack policies are three answers to "who must hold this record before the producer is told it succeeded".

Two producer facts sharpen the comparison. The default is `all` since Kafka 3.0 — deliberately, to pair with idempotence, which is enabled by default and *requires* `acks=all`; setting conflicting values with idempotence on throws a `ConfigException`. And `acks=all` alone still has a hole: it waits for the *current* ISR, so a partition down to one in-sync replica acknowledges one-copy writes — the hole `min.insync.replicas` plugs with `NotEnoughReplicas`.

> [!warning] "acks=all means all replicas have it" is the classic lie
> The documentation says it outright: acknowledgement by all replicas does not guarantee the full set of assigned replicas received the message — only the current in-sync set. With replication factor 3 and two dead followers, `acks=all` succeeds on a single copy. The other half-truth is "acks=0 is unsafe therefore never use it": for metrics and logging where losing records is acceptable, it buys real throughput. The durability floor that fixes the first lie is [[What is min.insync.replicas in Kafka]].

```java
props.put(ProducerConfig.ACKS_CONFIG, "all");          // wait for full ISR
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true); // requires acks=all
props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE); // resend transient failures
```

**Listing 1.** The durable-producer trio: `acks=all` for replication, idempotence so retries do not duplicate, unbounded retries bounded in time by `delivery.timeout.ms`.

`acks=all` does not change what "committed" means — a record still becomes visible to consumers only when the whole ISR has it and the ISR is at or above the min ISR floor, so weak acks mostly shorten the time the producer *believes* a record is safe. The replica bookkeeping behind all three settings is the ISR in [[What is the Kafka in-sync replica set]], and the way unbounded retries interact with duplicates and ordering is in [[Why can Kafka retries break ordering without idempotence]].

> [!tip] Interview answer
> `acks=0` is fire-and-forget with no guarantee and no effective retries; `acks=1` stops at the leader's log and loses records the leader takes down before replication; `acks=all` waits for the whole in-sync replica set and is the strongest setting, the default since 3.0, and a hard requirement for idempotence. The fine print is that "all" means the current ISR, so real durability needs `min.insync.replicas=2` at RF 3 on top.

