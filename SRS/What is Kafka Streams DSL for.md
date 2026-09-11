<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is Kafka Streams DSL for?

> [!abstract] Short answer
> It is the high-level layer of the Streams API: typed operations on KStream and KTable — map, filter, join, group, aggregate, window — that compile into a processor topology, so stateful stream processing is written as transformations instead of hand-wired processor nodes and manual state stores ([[What is the Kafka Streams API for]]).

## The vocabulary: streams, tables, operations

```d2
direction: right
in: "Input topic" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
ks: "KStream\nrecords, one event each" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
kt: "KTable\nper-key upserts" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
win: "Windowed aggregation\nstream time + grace" {
  width: 250
  height: 100
  style.fill: "#f3e5f5"
}
in -> ks
ks -> kt: groupBy + count
kt -> win: windowed ops
```

**Fig. 1.** The DSL's core move: an input stream grouped and aggregated becomes a KTable — a table of running values — which further operators and windows refine.

A `KStream` is an unbounded sequence of records where each is an event; a `KTable` is the changelog view of keyed data where each record is an upsert — and the DSL makes the duality workable in both directions: aggregating a stream yields a table, and `toStream()` turns a table back into its change stream ([[What is Kafka log compaction]]). Stateless operations — `map`, `filter`, `branch`-style splitting — transform records without history. Stateful operations build on the two abstractions: `groupBy` plus `count`/`aggregate` maintain per-key state in stores the framework manages; joins come in the combinations the semantics demand — KStream-KStream joins must be windowed because both sides are infinite, while KTable joins read current state per key. Windowing (`TimeWindows`, `SlidingWindows`, `SessionWindows`) groups records per key by event time with a grace period: a record arriving for a window after its end plus grace is discarded, which is the DSL's out-of-order contract ([[What ordering guarantees does Kafka provide for messages]]).

## What the DSL does not hide

The DSL sits on the same runtime as the Processor API: every operator becomes nodes in a topology, state lands in local stores backed by changelog topics, and scaling is still input partitions — grouping and aggregation shuffles by key through repartition topics when keys must be rehashed, which is a real data movement you pay for in latency and topics ([[How does Kafka achieve horizontal scalability]]). Aggregation output being a KTable is a semantic decision to make deliberately: downstream consumers of a count see updates per key, not appended events, and must call `toStream()` explicitly to publish them as a stream ([[What is the difference between a Kafka Consumer and Kafka Streams]]). For logic that does not fit the operators — custom scheduling, side effects per record, direct store access — the DSL drops down to the Processor API in the same application rather than forcing a rewrite.

> [!warning] Joins and aggregations are not SQL queries over the topic
> The DSL executes incrementally as records arrive; it is not a query engine that scans history on demand. A join only sees records present in its window or store while it runs — bootstrapping a KTable from a topic's past works because of changelog restoration, but a KStream-KStream join on "everything ever" is not a thing. Interviewers probe exactly this confusion.

> [!tip] Interview answer
> The DSL is the declarative layer of Kafka Streams: KStream for event sequences, KTable for per-key upserts, stateless ops like map and filter, stateful aggregations and joins with windowing on event time and grace periods for late data. It compiles to a processor topology with managed state stores and repartition topics, so you describe transformations while the runtime handles state, ordering, and scaling by partitions.

