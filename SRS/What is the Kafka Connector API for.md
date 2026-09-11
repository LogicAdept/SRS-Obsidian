<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka Connector API for?

> [!abstract] Short answer
> It is the plugin API of Kafka Connect — the framework for system-to-system pipes. You implement one `SourceConnector` or `SinkConnector` plus its tasks, deploy the jar on Connect workers, and the framework supplies offset storage, scaling, fault tolerance, and REST management. Dumping a database into topics, or topics into S3, becomes configuration instead of a hand-written client — Connect is one of the components in [[What are the main components of Apache Kafka]], while this API is its extension point ([[What core Kafka APIs exist]]).

## Two roles: planner and mover

The split is the interview point. A *Connector* never touches records: its configuration describes the job, `config()` exposes the validated settings schema, and `taskClass()` with `taskConfigs(maxTasks)` decides how the work splits into tasks. *Tasks* do the copying, in two flavors that mirror the direction: a `SourceTask` uses a pull interface — `poll()` returns batches of `SourceRecord` read from the external system — while a `SinkTask` uses a push interface — `put()` receives `SinkRecord`s, which carry the Kafka topic, partition, offset, key, value, and headers. So a connector you write once runs as many parallel tasks as `maxTasks` allows, distributed across the worker cluster.

```java
public class InvoiceSourceConnector extends SourceConnector {
    private Map<String, String> props;

    @Override public void start(Map<String, String> props) { this.props = props; }

    @Override public Class<? extends Task> taskClass() { return InvoiceSourceTask.class; }

    @Override public List<Map<String, String>> taskConfigs(int maxTasks) {
        // split the input (one shard per task) — never read records here
        return List.of(props);
    }

    @Override public ConfigDef config() { return CONFIG_DEF; }
    @Override public void stop() { }
}
```

**Listing 1.** Simplified source-connector skeleton: the Connector plans and hands config maps to tasks; record I/O lives in `InvoiceSourceTask.poll()`.

## What the framework does for the task author

```d2
direction: right
source: "External source\n(database, files)" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
connector: "SourceConnector\nplans tasks" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
worker: "Connect workers\nrun SourceTask.poll()" {
  width: 260
  height: 100
  style.fill: "#e8f5e9"
}
topic: "Kafka topic" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
offsets: "Offset storage\n(internal topics,\nframework-managed)" {
  width: 240
  height: 100
  style.fill: "#f3e5f5"
}
connector -> worker: taskConfigs
source -> worker: poll()
worker -> topic: produce
worker -> offsets: commits per record
```

**Fig. 1.** The Connector plans, workers run tasks, and offset management is automated by the framework: each `SourceRecord` carries a source partition and offset, so a restarted task resumes where it stopped.

Offset committing is the part Connect removes from your code: the framework records offsets into internal topics automatically, and only the connector knows how to seek back to that position in the source system on resume. For sources with acknowledgements, `SourceTask.commit()` and `commitRecord()` acknowledge back in bulk or per record. Discovery is Java ServiceLoader: the jar ships a `META-INF/services/org.apache.kafka.connect.source.SourceConnector` file listing the implementation class. When the external world changes — a new table appears — the Connector calls `ConnectorContext.requestTaskReconfiguration()` and the framework regenerates task configs gracefully. Workers themselves form a group in distributed mode — the same group management protocol that consumer groups use, so a worker leaving means its connectors rebalance ([[What triggers a Kafka consumer group rebalance]]) — and expose a REST API for submitting connectors; task failures surface through the reporter machinery, and an `ErrantRecordReporter` can send bad records to a dead-letter queue without stopping the task.

> [!warning] The Connector must not do the data movement
> The classic design error is reading or writing records inside the Connector class. Connectors are planners that may run anywhere in the cluster; tasks are the only place record I/O belongs — a `SourceTask.poll()` even gets its own dedicated thread and may block indefinitely, while `stop()` is called from another worker thread. Mixing the roles breaks scaling and task distribution.

> [!tip] Interview answer
> The Connector API is how Kafka Connect stays extensible: implement a Source or Sink Connector that splits the job into tasks, implement the task's poll or put, and the worker cluster handles offsets, distribution, REST management, and resume. Connectors plan, tasks copy. It is for system-to-system integration — for in-application logic with branching you would still use a plain consumer or a processing library.

