<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is Kafka consumer lag and how do you debug it?

> [!abstract] Short answer
> Lag is the distance between a partition's log end and the group's committed offset — per partition, never an average. Debug it by separating arrival rate from processing rate, then localizing: the consumer is processing-bound, there are too few consumers, or one partition is skewed.

## Measuring it

```console
$ bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group my-group
TOPIC       PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG      CONSUMER-ID     HOST        CLIENT-ID
my-topic    0          2               4               2        consumer-1-...  /127.0.0.1  consumer-1
my-topic    1          2               3               1        consumer-1-...  /127.0.0.1  consumer-1
my-topic    2          2               3               1        consumer-2-...  /127.0.0.1  consumer-2
```

**Listing 1.** `LAG` is `LOG-END-OFFSET` minus `CURRENT-OFFSET` for each partition — the group's progress against the log tail. In JMX the same signal is `records-lag-max` on `consumer-fetch-manager-metrics`, with per-partition lag metrics alongside.

The two numbers have clear owners: only the broker can advance the log end as records arrive, and only the group's members advance the committed offset as they process. Lag is therefore the race between two independent writers, which is why it can grow on a perfectly healthy broker (arrival spike) and why it can persist on a perfectly healthy consumer (processing ceiling).

First classify: transient or sustained. A restart or deploy produces lag that drains at the processing rate — harmless if the recovery slope beats the arrival rate. Sustained lag means arrival rate exceeds processing rate somewhere, and the poll metrics tell you where: `poll-idle-ratio-avg` near zero says the consumer spends its time in user processing, not waiting for data — processing-bound; `last-poll-seconds-ago` creeping toward `max.poll.interval.ms` says eviction is next, and the resulting rebalance redistributes partitions while lag is already growing ([[What is the difference between session.timeout.ms and max.poll.interval.ms]]).

## Localizing the bottleneck

Walk the standard suspects in order. Processing-bound handler — slow downstream calls or GC inside the loop. Not enough consumers — a group can never exceed one consumer per partition ([[What happens when there are more Kafka partitions than consumers]]), so check whether all partitions are even assigned. Skew — one partition's lag dwarfing the rest points at a hot key ([[What is a hot partition in Kafka]]). Poison-pill-style records that stall a batch need their own exit path ([[How do you handle a poison pill message in Kafka]]). Fixes follow the diagnosis: scale consumers up to the partition count, speed up or parallelize the handler, re-key or salt the skewed topic, and shrink `max.poll.records` if the batch itself keeps breaching the poll interval.

One false positive to rule out first: lag that shrank to zero and stays there can mean producers stopped, not that processing speeded up — confirm the topic still receives by cross-checking its `BytesInPerSec` ([[What Kafka metrics do you monitor in production]]) before crediting the group.

> [!example] Capacity math on one topic
> Arrival 1,000 records/s across 12 partitions; one consumer processes 500 records/s. Two members process 1,000/s — zero headroom, so every hiccup becomes growing lag; three members give real margin, and the ceiling is 12 members. The partition count caps the fix, which is why lag on an under-partitioned topic ends in a partition-count decision ([[What happens if you increase Kafka partition count later]]).

Two alerting practices keep the signal usable. Trend, not absolute value: alert on lag that keeps growing across minutes, because a snapshot number can't distinguish a burst from a ceiling. And shape, not just size: a batch job that polls occasionally shows sawtooth lag by design — judge it by its end-of-window position and drain time, since the number that pages an engineer on a streaming consumer is normal on a batch one. Membership churn is a separate alert worth having: a group that keeps rebalancing never stabilizes long enough to drain ([[What triggers a Kafka consumer group rebalance]]).

One deliberate lag source belongs in the toolbox: rewinding. Resetting a group to an older offset (or switching from `latest` to `earliest` on a fresh group) manufactures lag on purpose — the group replays history at its normal processing rate, so planned reprocessing needs the same drain-rate math as an incident, and the mechanics are in [[How do you replay Kafka messages from an older offset]].

> [!warning] A lag number without an arrival rate means nothing
> Ten thousand records behind at 100k records/s of throughput is a second of work; a hundred behind at a trickle can never catch up. Compare lag against the drain rate and trend — and read partitions individually, because an average across a skewed topic hides the one partition that is actually burning ([[What is a hot partition in Kafka]]).

> [!tip] Interview answer
> Lag is log-end offset minus committed offset per partition, read from the consumer-groups describe tool or lag JMX metrics. I first separate transient catch-up from sustained growth, then use poll metrics to tell processing-bound from data-starved, check consumer count against partition count, and look for single-partition skew. Fixes scale consumers, speed up handlers, or fix the key distribution — never averages, always per partition.
