<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How is a Kafka broker structured?

> [!abstract] Short answer
> A broker is one server process that hosts partition replicas: it accepts produce and fetch requests through a network and request-handler layer, appends and reads log segments on disk through the page cache, replicates with other brokers via its ReplicaManager, and coordinates through metadata — in KRaft mode by talking to the controller quorum, with no ZooKeeper anywhere.

## The layers, top to bottom

```d2
direction: down
net: "Acceptor + processor threads\nnetwork.client, plaintext/TLS" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
handlers: "Request handler pool\n(KafkaApis)" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
rm: "ReplicaManager\nappend / fetch / ISR tracking" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
log: "Log per partition\nsegments, indexes, page cache" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
meta: "Metadata client\nto controller quorum (KRaft)" {
  width: 320
  height: 90
  style.fill: "#f3e5f5"
}
net -> handlers -> rm -> log
handlers -> meta
```

**Fig. 1.** Requests land on network threads, are handed to the request-handler pool, and touch either replica data or the metadata path — never ZooKeeper in a modern cluster ([[What is the Kafka controller]]).

Data plane: broker sockets are served by acceptor and processor threads, then by a pool of request handlers that execute the actual API calls. The ReplicaManager decides where a produce request may append — a partition leader only accepts writes when enough replicas are in sync per `min.insync.replicas` — and serves fetches with bytes from the page cache; Kafka relies on sequential I/O and the OS cache rather than an application heap cache, which is why heap size is not the lever people expect ([[What is min.insync.replicas in Kafka]]). Each partition replica is a log: directories named `topic-partition`, holding size-rolled segments with offset and time indexes ([[How does Kafka store data on disk as a log]], [[What is a Kafka log segment]]).

## Control plane and lifecycle

In KRaft mode every server has a role — broker, controller, or both — and brokers discover the controller quorum through `controller.quorum.bootstrap.servers`; the controllers keep the metadata log and push metadata to brokers, so adding or failing a controller is quorum business, not ZooKeeper sessions ([[What is the Kafka controller]]). Brokers host internal topics too: `__consumer_offsets` for group positions and the transaction coordinator's state — a broker is chosen as coordinator for a group or transaction by hashing into these topics' partitions ([[What is the consumer_offsets topic for]]). Operationally a broker's failure mode is well-trodden: the controller notices, reassigns leadership for the partitions it led, and the cluster keeps serving ([[What happens when a Kafka broker fails]]); disk problems degrade to under-replicated partitions or a stopped log dir ([[What are under-replicated partitions in Kafka]], [[What happens when a Kafka broker disk fills up]]).

```properties
num.io.threads=8                  # request handlers doing disk work
num.network.threads=3             # processors moving bytes on sockets
num.partitions=1                  # default partitions for new topics
log.dirs=/kafka/data-1,/kafka/data-2   # replica logs live here
log.retention.hours=168           # segment deletion policy
broker.rack=rack-1                # rack for replica spreading
```

**Listing 1.** The broker-side settings that shape this structure: thread pools, log directories, defaults, and placement.

> [!warning] The broker is not a database with queries
> Everything a broker does with data is append, read-by-offset, and segment deletion — no secondary indexes, no update in place, no filtering server-side beyond offset ranges. Workloads that need per-record lookup or mutation belong in a store behind Kafka, not inside it; forcing that role shows up as compaction abuse and unbounded partition counts.

> [!tip] Interview answer
> A broker is a server process hosting partition replicas: network threads, a request-handler pool, and a ReplicaManager that appends to segment logs and serves fetches from the page cache, tracking ISR per partition. Metadata comes from the KRaft controller quorum — brokers just consume it. Internal topics for offsets and transactions also live on brokers, and failure handling is controller-driven leader reassignment.

