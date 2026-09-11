<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How does Kafka Connect differ from a custom consumer?

> [!abstract] Short answer
> Connect is a runtime you deploy; a custom consumer is code you own. Connect workers run connector plugins with framework-managed offsets, scaling, error handling, and REST operations — for moving data between systems. A custom consumer lives inside your application when the logic itself is the point: branching, business rules, writes that must join application transactions ([[What is the Kafka Connector API for]], [[What is the Kafka Consumer API for]]).

## The decision by responsibility

```d2
direction: right
kafka: "Kafka" {
  width: 160
  height: 80
  style.fill: "#e3f2fd"
}
conn: "Connect workers\nplugin does the mapping;\nframework does the rest" {
  width: 300
  height: 110
  style.fill: "#e8f5e9"
}
app: "Your app\nconsumer embedded\nin business logic" {
  width: 280
  height: 110
  style.fill: "#fff3e0"
}
sink: "Another system\nDB, S3, search" {
  width: 210
  height: 90
  style.fill: "#e3f2fd"
}
kafka -> conn -> sink
kafka -> app
```

**Fig. 1.** System-to-system pipes belong on workers; logic that shares a process and transaction boundary with your application stays a custom consumer.

What the framework takes over is the operational surface a hand-rolled consumer always underinvests in: offset storage and resume (per-record source offsets committed automatically for source connectors, consumer offsets for sink ones), task distribution across workers with rebalancing, REST APIs for submitting and inspecting connectors, per-record error handling with dead-letter queues, and single-message transforms for cheap reshaping. A custom consumer gives you all the control that Connect deliberately abstracts: transactional consistency between consuming and your database (offsets committed in the same transaction as side effects), arbitrary in-process logic, and no second distributed system to run. Connect also inverts the offset model for sources — the connector reports a source partition and offset per record, and the framework persists it — which is resume plumbing you would otherwise write yourself ([[What is Kafka Consumer position for]]).

## Where each choice actually hurts

Teams that hand-roll an ingest pipeline in a consumer end up re-implementing workers: deployment for parallelism, retry and dead-letter paths, offset bookkeeping, monitoring of progress — all of it with a homegrown shape nobody can operate but the authors. Teams that force Connect where logic belongs end up writing transformations in a DSL that cannot call your domain code, splitting one business operation across a worker process and an application with no shared transaction ([[What happens during a Kafka consume-transform-produce transaction]]). The interview-shaped answer: the differentiator is not features but ownership — Connect owns moving bytes between named systems; you own decisions, and decisions belong in your codebase ([[What are the main components of Apache Kafka]]).

> [!warning] Connect is not "an easier consumer" for application logic
> Sink connectors write to other systems; they do not hand records to your service's event handlers. If the requirement is "when an order event arrives, update the order service's state", a connector into a database is the wrong shape — that is a consumer in the service, where processing and state changes share one failure domain.

> [!tip] Interview answer
> Kafka Connect is a framework and runtime: connector plugins, managed offsets and resume, task distribution, REST ops, DLQs — the right tool when data just needs to move between systems. A custom consumer is your code inside your application, with full control and transactional coupling to your own state. If the pipeline is dumb plumbing, use Connect; if processing is the product, write the consumer.

