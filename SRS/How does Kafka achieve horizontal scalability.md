<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How does Kafka achieve horizontal scalability?

> [!abstract] Short answer
> By making the partition the only unit of everything: data is sharded across partitions, partitions are spread across brokers, consumers scale by grabbing partitions, and metadata coordination is cheap because leaders — not clients — route everything. Add brokers to add disk and network capacity; add partitions to add read/write parallelism; add consumers up to the partition count ([[What is Apache Kafka]]).

## The four scaling axes

```d2
direction: right
data: "Data plane\npartition = shard unit" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
broker: "Broker plane\nleaders spread evenly\nacross brokers" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
consumer: "Consumer plane\npartition = assignment unit" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
control: "Control plane\ncontroller quorum\nbatches leadership moves" {
  width: 260
  height: 100
  style.fill: "#f3e5f5"
}
data -> broker
data -> consumer
control -> broker: reassigns\nleadership
```

**Fig. 1.** Every plane scales around the same unit, which is why throughput grows roughly linearly as you add brokers and partitions — nothing centralizes on the data path.

Data placement: a topic's partitions are independent logs assigned to brokers, with each partition's leader spread by the replica placement policy so produce traffic lands on many machines at once; rack awareness keeps replicas off one failure domain ([[What is rack awareness in Kafka]]). Writes and reads are per-partition: a producer's batches target one leader per partition batch, and no global lock or coordinator sits in the write path — throughput scales with partitions times brokers, bounded by replication traffic and per-broker partition counts ([[How does a Kafka producer send a record internally]]). Consumer side: a group splits the partitions among members, so consumption parallelism is the partition count — more members than partitions just idle ([[What happens if you have more Kafka consumers than partitions]]).

## Why the control plane stays out of the way

The partitioned design also makes failure handling scalable. When a broker dies, the controller elects new leaders from the ISR in batches — one leadership-change wave, not one election per partition — and the critical unavailability window stays short even for clusters hosting many partitions ([[What happens when a Kafka broker fails]]). Client-side, the metadata contract means producers and consumers learn leader locations from metadata and then talk directly to the right broker; there is no routing tier whose capacity you must scale ([[What are the main components of Apache Kafka]]). KRaft extends the same idea to metadata: a Raft quorum of controllers maintains the metadata log, moving cluster coordination cost off the data brokers and supporting large partition counts ([[What is the Kafka controller]]).

The price is explicit in the model: ordering exists only per partition, so scaling a keyed workload means accepting that global order is gone ([[What ordering guarantees does Kafka provide for messages]]); keys pin records to partitions via hash, so changing partition count reshuffles key mapping ([[What happens if you increase Kafka partition count later]]); and skew shows up as a hot partition that no amount of broker addition fixes ([[What is a hot partition in Kafka]]).

> [!warning] Partitions are not free parallelism
> Each partition means open file handles, replication traffic, more fetch sessions, and more work in leader elections; per-broker partition counts in the hundreds of thousands start hurting recovery time. Scaling by blindly raising partition counts trades today's throughput problem for tomorrow's rebalance and recovery problem — sizing is a decision, not a default ([[How do you choose the number of partitions for a Kafka topic]]).

> [!tip] Interview answer
> Kafka scales horizontally because the partition is the unit of storage, replication, and consumption: partitions spread across brokers for capacity, consumer groups spread partitions across members for read parallelism, and clients talk straight to leaders with no routing tier. Failure handling is controller-batched, and KRaft keeps the metadata plane cheap. The tradeoffs are per-partition ordering and hash-based key placement.

