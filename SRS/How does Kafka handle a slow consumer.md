<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How does Kafka handle a slow consumer?

> [!abstract] Short answer
> Kafka deliberately does nothing to the data: a pull-based broker lets the consumer fall behind and catch up when it can. Unread records stay in the log until retention expires, lag is a single number per partition, and the pressure points are client-side — the poll-gap timeout, fetch batching, and how you size partitions and members.

## Why the broker never pushes back

The pull design makes that safe by construction: in a push system the broker controls the rate and consumers tend to be overwhelmed when their consumption rate falls below the production rate — a denial of service in essence. Kafka's pull model has the nicer property that the consumer simply falls behind and catches up when it can, and pull also enables aggressive batching: the consumer pulls everything available after its position up to a size cap. The broker keeps no per-message consumption state to manage, so a slow group costs it nothing — the records sit in segments that already exist, retained until the retention policy expires them.

Progress is measured, not assumed. Each partition's position moves only as fast as the consumer drains it, and the gap between the log end and the consumer is consumer lag — the operational signal for "slow consumer" and the subject of [[What is Kafka consumer lag and how do you debug it]]. The watermark machinery that defines the log end is covered in [[What is the Kafka high watermark]].

## The three guards, and which one fires first

```d2
direction: down
slow: "consumer too slow\nlag grows" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
poll: "poll gap exceeds\nmax.poll.interval.ms (5 min)" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
leave: "client leaves the group\npartitions reassigned" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
fetch: "still polling but behind\nfetch long-poll buffers data" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
log: "log retention keeps\nunread records" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
slow -> poll
poll -> leave
slow -> fetch
fetch -> log
```

**Fig. 1.** A consumer that keeps polling just lags (the good case); one whose loop stalls past the poll interval is evicted by its own client and its partitions move on.

If the consumer still calls `poll()` but processes slowly, nothing evicts it — fetches continue, lag accumulates, and the fixes are capacity and batching: more members up to the partition count (the sizing trade-off in [[How do you choose the number of partitions for a Kafka topic]]), or tuning the fetch caps (`fetch.min.bytes`, `max.partition.fetch.bytes`, `fetch.max.bytes`) so each round trip carries more data. If the loop itself stalls longer than `max.poll.interval.ms` (5 minutes by default), the client proactively leaves the group — the timeout pair is dissected in [[What is the difference between session.timeout.ms and max.poll.interval.ms]]. For records that *never* process — corrupt payloads that fail on every attempt — lag grows without hope; that failure mode is the poison-pill problem in [[How do you handle a poison pill message in Kafka]].

The standard pattern for unpredictable processing time: move processing to another thread, keep the consumer polling, and `pause()` the partitions so poll stops returning new records until the worker drains the old ones — with manual commits so offsets never race ahead of actual processing.

> [!warning] A slow consumer does not slow the cluster — until you misread the fix
> Producers, brokers and other groups keep full speed while one group lags; there is no broker-side throttling to loosen. But two popular "fixes" are traps: raising `max.poll.interval.ms` hides the stall while delaying every future rebalance, and disabling the poll-gap eviction outright lets a hung member hold partitions forever. If processing is genuinely slower than production long-term, the only real cures are more parallelism or more partitions — lag will otherwise exceed even the retention window, and then the data is gone (records past retention are deleted and the consumer resets per `auto.offset.reset`).

> [!tip] Interview answer
> Kafka's pull design means a slow consumer just falls behind and catches up later — the broker stores everything and never throttles or drops for a lagging group. You watch consumer lag per partition; if the loop stalls past max.poll.interval.ms the consumer leaves the group, otherwise it keeps fetching while behind. Fixes are parallelism, fetch tuning, the pause-and-worker-thread pattern, and handling poison records — not broker settings.

