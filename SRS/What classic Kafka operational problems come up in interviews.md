<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What classic Kafka operational problems come up in interviews?

> [!abstract] Short answer
> A stable set of production incidents, each with a known mechanism: consumer lag growth, rebalance storms, under-replicated partitions and ISR shrinkage, leader elections after broker loss, disk exhaustion, hot partitions from key skew, quota throttling that looks like a client bug, and poison pills that wedge a group. Interviewers want diagnosis from symptoms, not definitions ([[What Kafka metrics do you monitor in production]]).

## The catalog, symptom first

```d2
direction: right
lag: "Lag climbing\ngroup behind, no errors" {
  width: 240
  height: 100
  style.fill: "#fff3e0"
}
isr: "Under-replicated\nISR shrinking" {
  width: 230
  height: 100
  style.fill: "#ffebee"
}
rb: "Rebalance loop\nmembers cycling" {
  width: 230
  height: 100
  style.fill: "#ffebee"
}
disk: "Broker disk\nfilling up" {
  width: 220
  height: 90
  style.fill: "#ffebee"
}
skew: "One partition hot\nothers idle" {
  width: 230
  height: 100
  style.fill: "#fff3e0"
}
dq: "Throttled\nempty fetches, delays" {
  width: 240
  height: 100
  style.fill: "#f3e5f5"
}
```

**Fig. 1.** Six incident shapes that cover most interview war stories: each has a mechanism, a metric, and a fix that the follow-up question is really asking for.

Lag without errors: consumers are the bottleneck — processing slower than arrival, or throughput capped by fetch settings; fix the consumer, size partitions for parallelism, and check whether a rebalance reset the offsets' pace ([[What is Kafka consumer lag and how do you debug it]], [[What happens if you have more Kafka consumers than partitions]]). Rebalance storms: members evicted for exceeding `max.poll.interval.ms` — usually a slow handler, not a network fault — rejoin, inherit partitions, and fail again; the fix is the poll interval and batch size, not session timeouts ([[What is the difference between session.timeout.ms and max.poll.interval.ms]], [[What triggers a Kafka consumer group rebalance]]). Under-replicated partitions: a broker is slow, dead, or its disk is degrading; sustained URPs mean replication cannot keep up and `min.insync.replicas` puts availability at risk next ([[What are under-replicated partitions in Kafka]], [[What is min.insync.replicas in Kafka]]). Broker loss and disk full: leadership reassignment floods partitions — the controller batches it — and a full log dir stops serving replicas outright ([[What happens when a Kafka broker fails]], [[What happens when a Kafka broker disk fills up]]).

## The two that look like bugs but are features

Hot partitions: a skewed key space concentrates traffic on one partition while scaling out does nothing — the fix is key design or salting, and no broker tuning helps ([[What is a hot partition in Kafka]], [[Why do Kafka producer keys matter]]). Quota throttling: a multi-tenant cluster answers throttled clients with delayed responses and empty fetches, which surfaces as mysterious lag and slowness on only some clients — check quotas before rewriting the consumer ([[What is the Kafka Quota API for]]). The meta-skill the interviews test: read the symptom as a question about mechanism — what advances lag, what shrinks an ISR, what triggers an eviction — and answer with the knob that changes the mechanism, not with a config name memorized out of context ([[What is unclean leader election in Kafka]], [[How do you handle a poison pill message in Kafka]]).

> [!warning] Most "Kafka reliability problems" are consumer problems
> The broker layer — replication, leader election, retention — is battle-tested and rarely the culprit; the incidents above mostly start in application code: blocking handlers, unkeyed events, auto-commit misuse, retry loops without bounds. Saying that with the mechanism behind it lands better than reciting broker internals ([[Why is Kafka enable.auto.commit dangerous]]).

> [!tip] Interview answer
> The classics: consumer lag from slow processing, rebalance storms from max.poll.interval exceeded, under-replicated partitions from a sick broker or disk, leadership floods after broker loss, hot partitions from key skew, quota throttling disguised as lag, and poison pills wedging a group. For each I'd name the mechanism and the metric — lag per group, URPs, request handler idle — and the fix at the right layer, which is usually the consumer, not the broker.

