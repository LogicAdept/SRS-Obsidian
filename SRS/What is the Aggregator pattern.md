<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messaging #SRS

# What is the Aggregator pattern?

> [!abstract] Short answer
> An **Aggregator** is a **stateful filter** that collects correlated messages until a **complete set** has arrived, then publishes **one distilled message**. Its design lives in three choices: how messages correlate, when a set is complete, and how results combine.

## Correlation, completeness, combination

The aggregator receives a stream and first identifies which messages belong together — correlation, usually a key such as an order id or a correlation identifier. Then comes the completeness condition: when is the set ready? If the count is known (from a copy of the original composite or a per-message total), it can wait for all; otherwise it can time out and act on what arrived, take the first-best response, time out with an override threshold, or conclude on an external business event such as end-of-trading. Finally the aggregation algorithm distills the collected messages into one output. Each choice trades latency against information: wait-for-all is slow and brittle (one missing piece stalls the aggregate), first-best is fast and wasteful. Typical fixtures: a stock aggregator recombining item reservations, a bidding flow taking the best quote — the sibling flow for broadcast-plus-collect is the [[What is the Scatter-Gather pattern]], the producer of its input is often a [[What is the Splitter pattern]], and correlation keys are the [[What is the Correlation Identifier pattern]].

```d2
direction: down
in: "Correlated stream\nkey: order O-9" {
  width: 230
  height: 65
  style.fill: "#e3f2fd"
}
ag: "Aggregator\nstate store + completeness" {
  width: 260
  height: 75
  style.fill: "#fff3e0"
}
set: "Set complete?\nall / timeout / first-best" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
out: "Single message\ndistilled result" {
  width: 230
  height: 65
  style.fill: "#e8f5e9"
}
in -> ag -> set -> out```

**Fig. 1.** State between messages is the essence: the aggregator is a filter with memory and a completion rule.

## The three decisions in code shape

```java
class OrderAggregationStrategy implements AggregationStrategy {
    public Exchange aggregate(Exchange old, Exchange next) {
        // correlation: header order-id (external to this method)
        // completeness: this strategy = wait-for-all via split size
        // algorithm: collect reservations into one order status
        return merge(old, next);
    }
}
// broker-side state store keyed by order-id, TTL for abandoned groups
```

**Listing 1.** Whatever the framework, the same triple appears: key, completeness rule, merge function — plus a TTL for groups that never complete.

> [!warning] Incomplete groups are the normal case, not the edge case
> At-least-once delivery produces duplicates inside a group; crashes produce groups that never finish; slow producers produce timeouts. An aggregator without a TTL on its state, a dedup on entry, and a designed timeout outcome leaks memory and deadlocks the business process waiting for a set that will never close.

> [!tip] Interview answer
> An Aggregator collects correlated messages in a stateful filter and emits one combined message when the set is complete. The three design decisions are correlation (what belongs together), completeness (wait-for-all, timeout, first-best, or an external event), and the aggregation algorithm. Its state needs TTL and dedup, because missing pieces and duplicates are routine, not anomalies.
