<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What Kafka consumer settings matter in practice?

> [!abstract] Short answer
> Three groups: correctness — `enable.auto.commit`, `max.poll.interval.ms`, `max.poll.records`; liveness — `session.timeout.ms` and `heartbeat.interval.ms`; throughput — `fetch.min.bytes` with `fetch.max.wait.ms` and the fetch size caps. Mode settings on top: `isolation.level`, `group.instance.id`, and `group.protocol`.

## The three groups

```properties
group.id=payments-consumers            # membership identity
enable.auto.commit=false               # default true; commit after processing for at-least-once
max.poll.records=500                   # records per poll() — default 500
max.poll.interval.ms=300000            # must exceed worst-case processing of one poll batch
session.timeout.ms=45000               # crash detection window; default 45 s
heartbeat.interval.ms=3000             # ideally no more than 1/3 of session timeout
fetch.min.bytes=1                      # broker waits for this much data per fetch
fetch.max.wait.ms=500                  # ... but at most this long
fetch.max.bytes=52428800               # 50 MiB per fetch, not an absolute cap
max.partition.fetch.bytes=1048576      # 1 MiB per partition inside a fetch
isolation.level=read_uncommitted       # read_committed for transactional sources
```

**Listing 1.** Consumer settings grouped by what they actually control; comments carry the shipped defaults.

The correctness group is where data is lost or duplicated. With `enable.auto.commit=true` offsets commit in the background whether or not processing finished — [[Why is Kafka enable.auto.commit dangerous]]; production consumers that need at-least-once turn it off and commit explicitly with `commitSync`/`commitAsync` ([[What are Kafka commitSync and commitAsync for]]). `max.poll.interval.ms` (5 minutes default) bounds the gap between `poll()` calls: if processing a `max.poll.records` batch takes longer, the consumer is considered failed and the group rebalances — the loop of [[What triggers a Kafka consumer group rebalance]]. `auto.offset.reset` (default `latest`) only answers where a group with no committed offset starts — a fresh group on `latest` silently skips everything already in the log, which is rarely what a first deploy wants ([[How do you replay Kafka messages from an older offset]]). Throughput tuning is symmetric: raise `fetch.min.bytes` and the broker answers only with meaningful data, at the cost of up to `fetch.max.wait.ms` of added latency; the fetch caps are not absolute — a first batch larger than the per-partition limit still ships so the consumer can make progress.

## Modes

`isolation.level=read_committed` hides aborted transaction records ([[What does isolation.level read_committed do in Kafka]]). `group.instance.id` turns a member static, which keeps partitions assigned across short restarts. `group.protocol` selects `classic` (default) or the new `consumer` protocol — under the latter the broker drives heartbeats, and `session.timeout.ms`/`heartbeat.interval.ms` are not supported on the client.

Static membership deserves a sentence of caution before it becomes the default choice: it trades fast failover for restart stability. With `group.instance.id` set, a member that goes away keeps its partitions idle until the session timeout expires instead of triggering an immediate rebalance — great for rolling restarts, worse for a genuinely crashed consumer. Choose per workload, not per fashion; the rebalance-triggering behavior itself is the same either way.

> [!note] The knobs move with the protocol
> Under `group.protocol=consumer` the liveness settings switch sides: session and heartbeat timeouts are broker-side configs (`group.consumer.session.timeout.ms`, `group.consumer.heartbeat.interval.ms`), and the client-side `session.timeout.ms`/`heartbeat.interval.ms` are not supported. During a rollout the two protocols coexist, so the same group can run different liveness regimes per member — check the protocol before debugging a "timeout that does nothing".

> [!warning] Slow processing is not a session-timeout problem
> Heartbeats flow on a background thread while your handler runs, so a consumer that takes 10 minutes per batch still shows a live session. Only `max.poll.interval.ms` governs processing time; raising `session.timeout.ms` to "fix" slow consumers just delays crash detection and rebalances — [[What is the difference between session.timeout.ms and max.poll.interval.ms]].

> [!tip] Interview answer
> I split consumer config by concern: auto-commit off with explicit commits for delivery control, `max.poll.interval.ms` above the worst batch so long processing does not evict the member, session and heartbeat timeouts for crash detection, fetch settings for throughput-latency, and mode flags — `read_committed`, static membership, and the group protocol. The classic mistake is tuning session timeout for slow processing; that is what `max.poll.interval.ms` is for.
