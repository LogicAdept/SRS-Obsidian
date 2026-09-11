<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How do you handle a poison pill message in Kafka?

> [!abstract] Short answer
> A poison pill is a record your consumer cannot process — undecodable bytes, a schema your code crashes on — and the danger is not the record but the loop: fail, restart, re-poll the same offset, fail again. The handling pattern is explicit: bound the failure, skip past it deliberately, and route the record to a dead-letter topic with context — or let Connect's error settings do the same for pipeline workloads ([[What is the Kafka Consumer API for]]).

## Why the naive loop dies

```d2
direction: down
poll: "poll() returns batch\nwith bad record" {
  width: 250
  height: 90
  style.fill: "#ffebee"
}
fail: "Handler throws\nno offset committed" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
rb: "Rebalance\nmax.poll.interval exceeded" {
  width: 260
  height: 100
  style.fill: "#ffebee"
}
again: "Partition reassigned\nsame offset re-polled" {
  width: 270
  height: 100
  style.fill: "#fff3e0"
}
dlq: "Skip + dead-letter\nwith error context" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
poll -> fail -> rb -> again
again -> fail: loops
again -> dlq: handled
```

**Fig. 1.** The poison-pill death spiral: the bad record blocks the loop, the group evicts the member, another member inherits the same offset — the pipeline wedges instead of failing.

Because commits are batch-level and a failed handler leaves the position uncommitted, a crashing record is retried forever: the consumer throws, restarts, re-polls the same offset, and — if retries burn past `max.poll.interval.ms` — the group rebalances and hands the poison to another member ([[What is the difference between session.timeout.ms and max.poll.interval.ms]], [[What triggers a Kafka consumer group rebalance]]). The fix is to convert an unbounded retry into a bounded decision: catch per-record failures, after N attempts produce the raw payload to a dead-letter topic — original bytes, plus headers or a wrapper carrying the topic, partition, offset, and the error — then commit past it. The dead-letter topic stays a real Kafka topic, so triage is itself a consumer, and reprocessing later is an ordinary replay ([[How do you replay Kafka messages from an older offset]]).

## Deserializers and Connect

Serialization failures deserve special handling because they fire inside the consumer before your code sees anything: a common pattern is a wrapping deserializer that returns a marker object or null with the failure recorded in headers, turning a crash into a routable record. In Connect the machinery is built in: `errors.tolerance` — `none` by default, so the first bad record fails the task — can be set to `all`, with `errors.deadletterqueue.topic.name` routing sink records that fail deserialization or conversion, and error logs or headers carrying the cause; an `ErrantRecordReporter` lets sink task code report bad records explicitly ([[What is the Kafka Connector API for]]). Monitoring closes the loop: dead-letter rates and skip counters are alerting signals, not noise — a silent skip path is how data loss hides ([[What Kafka metrics do you monitor in production]]).

> [!warning] Skipping is a product decision, not an engineering one
> "Skip after three tries and dead-letter" means the good records behind the poison now flow — usually right — but the skipped event's business effect never happened. The correct retry count and the dead-letter SLA belong to the domain owner; engineers who choose unilaterally pick the poison of silent inconsistency over the pill's loud stall.

> [!tip] Interview answer
> A poison pill wedges a consumer because a failing record never commits, the loop stalls, and rebalancing just hands the same offset to the next member. Handle it by bounding retries per record, then producing the raw payload to a dead-letter topic with origin metadata and committing past it; wrap deserializers so decode failures become routable records, use errors.tolerance plus DLQ settings in Connect, and alert on dead-letter rates.

