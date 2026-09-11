<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the difference between a Kafka Consumer and Kafka Streams?

> [!abstract] Short answer
> A consumer gives you a partition-cursor to program with; Streams gives you a processing engine to configure. The consumer hands you batches and trusts you for positions, ordering, state, and failure handling. Streams runs a topology of processors with managed state stores, joins, windows, and exactly-once plumbing — at the price of adopting its runtime model ([[What is the Kafka Consumer API for]], [[What is the Kafka Streams API for]]).

## The same substrate, two altitudes

```d2
direction: down
raw: "KafkaConsumer\npoll loop, you own everything" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
you: "Your code\nposition, dedup, state, joins,\nrebalance hooks, delivery" {
  width: 300
  height: 100
  style.fill: "#ffebee"
}
top: "KafkaStreams\ntopology + runtime" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
ops: "DSL ops, state stores,\nchangelog restore, EOS" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
raw -> you
top -> ops
```

**Fig. 1.** The consumer is a thin client over fetch and group protocols; Streams is a layer that already made the decisions you would otherwise code by hand.

With a plain consumer you control the loop — subscribe or assign, poll, commit — and every stateful concern is yours: keeping running aggregates means your own store and your own restore story, correlating two topics means your own join buffer, and surviving rebalances means committing in `onPartitionsRevoked` at the right moment ([[What are Kafka subscribe and poll for]], [[What triggers a Kafka consumer group rebalance]]). Streams takes those concerns in: stateful operators write to local state stores restored from changelog topics, aggregations and joins come as typed operations with event-time windows, scaling follows input partitions through task assignment, and `processing.guarantee=exactly_once_v2` commits input offsets, state changes, and outputs atomically ([[What is Kafka log compaction]], [[How do you achieve exactly-once processing in Kafka]]). The consumer remains underneath — a Streams instance is a consumer group member — but your code stops touching positions and fetches.

## Choosing the altitude

Choose the consumer when processing is application logic: writes to your own database, calls to other services, business branching, anything needing custom delivery semantics — the consumer is also the substrate Spring Kafka wraps for listener containers ([[How would you explain Spring Kafka]]). Choose Streams when the work is stream transformations between topics: aggregations, enrichments, windowed analytics, pipelines that benefit from the state and EOS machinery rather than fighting for it ([[What is Kafka Streams DSL for]]). The cost asymmetry matters in both directions: Streams adds internal topics, state directories, and rebalance semantics to operate; the consumer adds every stateful bug class back to your backlog ([[What are the main components of Apache Kafka]]).

> [!warning] Streams is not "a consumer with helpers"
> Adopting Streams changes your operational surface: changelog and repartition topics appear, state must be restored on restart, partition counts cap parallelism, and delivery is managed for you. Teams that pick Streams for a plain forwarding loop inherit that surface for nothing — the same loop is ten lines of consumer code with no topology to babysit.

> [!tip] Interview answer
> A KafkaConsumer is a thin, single-threaded client: poll batches, commit positions, and you own state, joins, windowing, and rebalance handling. Kafka Streams is an engine on top: typed operators with state stores restored from changelog topics, event-time windows, and exactly-once via processing.guarantee, scaling by input partitions. Use the consumer for app-side logic; use Streams when stateful topic-to-topic processing is the workload.

