<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka AdminClient API for?

> [!abstract] Short answer
> Cluster administration from code: creating and deleting topics, growing partition counts, reading and altering configs, managing ACLs, quotas, consumer groups and their offsets, plus operational controls such as leader election, partition reassignment, and fencing transactional producers. Every bundled CLI — `kafka-topics.sh`, `kafka-configs.sh`, `kafka-consumer-groups.sh` — is a thin wrapper over this API, the `Admin` interface from kafka-clients ([[What core Kafka APIs exist]]).

## One pattern for every operation

```java
Properties props = new Properties();
props.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
try (Admin admin = Admin.create(props)) {
    CreateTopicsResult result = admin.createTopics(Collections.singleton(
        new NewTopic("orders", 12, (short) 3)
            .configs(Map.of(TopicConfig.CLEANUP_POLICY_CONFIG,
                            TopicConfig.CLEANUP_POLICY_COMPACT))));
    result.values().get("orders").get(); // blocks until created or fails
}
```

**Listing 1.** Creating a compacted topic: `Admin.create` builds the client, and `KafkaFuture.get()` turns the asynchronous call into a blocking one.

The API is uniform, and that pattern is the interview point. An `Admin` instance comes from `Admin.create(Map)` and is thread-safe, so one instance serves the whole application. Each operation takes a `Collection` of items — batching topics or group ids into one call is cheaper than looping — and each operation is asynchronous: it returns an `XxxResult` object exposing `KafkaFuture`s, typically `all()` for the batch outcome and `values()` for per-item results. Two overloads exist for every method: one with default options and one whose last parameter is an options object. `bootstrap.servers` is used only to discover brokers, so two or three addresses are enough to survive an outage.

## Where requests actually go

```d2
direction: right
admin: "Admin client" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
controller: "Controller" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
any: "Any broker\n(least outstanding\nrequests)" {
  width: 220
  height: 100
  style.fill: "#e8f5e9"
}
create: "createTopics\ndeleteTopics" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
describe: "describeTopics\ndescribeConfigs\nlistConsumerGroups" {
  width: 250
  height: 100
  style.fill: "#e8f5e9"
}
admin -> create: sends
create -> controller
admin -> describe: sends
describe -> any
```

**Fig. 1.** Different operations necessitate requests to different nodes: topic creation talks to the controller, while describes can hit any broker — the client picks the one with the fewest outstanding requests.

If a request like `createTopics` lands on a node that is not the controller, the client refreshes metadata and re-sends it transparently — callers do not pick targets. The minimum broker version is 0.10.0.0, and methods that need more say so in their contracts; calling a newer operation against an older broker fails with `UnsupportedVersionException`.

## What the surface covers

Topic lifecycle is `createTopics`, `deleteTopics`, and `createPartitions` — growing a topic later is exactly [[What happens if you increase Kafka partition count later]]. Configuration and governance come through `describeConfigs` and `incrementalAlterConfigs`, `describeAcls` for ACLs, and `describeClientQuotas`/`alterClientQuotas` for quota management — the programmatic path behind [[What is the Kafka Quota API for]]. Consumer groups are inspectable with `listConsumerGroups`, `listConsumerGroupOffsets` — the engine of lag tools ([[What is Kafka consumer lag and how do you debug it]]) — and `deleteConsumerGroups` for empty groups. Diagnostics and repair round it out: `listOffsets` and `describeProducers` for per-partition state, `describeTransactions` and `fenceProducers` for transaction coordinators ([[What is producer fencing in Kafka transactions]]), `electLeaders` for preferred-leader work, `alterPartitionReassignments` with `describeLogDirs` for moving replicas, and `unregisterBroker` for KRaft-era removal.

> [!warning] The futures execute on a single client thread
> `KafkaFuture` completion callbacks such as `thenApply` run on one thread inside the Admin client. Blocking inside such a callback — a `.get()` chained onto a result — stalls every pending result of that instance. Move heavy follow-up work onto your own executor, and use `.get()` only from caller code.

> [!tip] Interview answer
> AdminClient is the management API the CLIs are built on: topics, configs, ACLs, quotas, consumer groups, plus repair operations like leader election and reassignment. Every call is batched and asynchronous — it returns futures you can block on. Topic creation goes to the controller, describes go to any broker, and the client retries controller redirects by itself, so application code only declares what it wants done.

