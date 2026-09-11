<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# How do you scale RabbitMQ consumers

> [!abstract] Short answer
> First add competing consumers and tune prefetch. When one queue saturates — it is effectively single-core — shard into multiple queues via routing keys or the modulus-hash exchange and balance consumers across them. More cluster nodes only help if the bottleneck is connections or CPU overall, not a single queue.

## The scaling ladder

Level one is horizontal consumers: more processes on the same queue, each with a sensible prefetch. Level two is consumer speed itself: the consumer capacity metric tells whether the queue could deliver faster than it does. Level three is sharding: publish with shard-aware routing keys, or use the `x-modulus-hash` exchange to partition messages across queues, each with its own consumer pool — parallelism with per-key ordering preserved, per [[How does RabbitMQ preserve message order]]. Level four is protocol-level throughput (streams) when the workload is fan-out rather than job processing.

```d2
direction: down
pub: "publish\nshard keys" {
  width: 170
  height: 70
  style.fill: "#e3f2fd"
}
hash: "x-modulus-hash\nexchange" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
q1: "shard queue 1\nconsumers" {
  width: 180
  height: 80
  style.fill: "#e8f5e9"
}
q2: "shard queue 2\nconsumers" {
  width: 180
  height: 80
  style.fill: "#e8f5e9"
}
q3: "shard queue 3\nconsumers" {
  width: 180
  height: 80
  style.fill: "#e8f5e9"
}
pub -> hash
hash -> q1
hash -> q2
hash -> q3
```

**Fig. 1.** Sharding multiplies the single-core queue limit by the shard count while keeping per-key order.

## What does not scale

Adding cluster nodes does not speed up one hot queue: a classic queue lives on one node and a quorum queue serializes through its leader — replicas are for availability, not read scaling. Prefetch inflation beyond unacked-seconds of work adds memory without throughput. And if consumers are slow because the handler is slow (IO, external calls), no broker knob helps; the fix is batching, async IO, or handler redesign — the broker-side counterpart is [[What causes a RabbitMQ queue to back up]].

```bash
rabbitmqctl list_queues name consumers messages_unacknowledged   messages_ready
```

**Listing 1.** The first scaling triage: consumers per queue, unacked pressure, ready backlog.

> [!warning] Quorum leader is not a load balancer
> All operations flow through a quorum queue's leader; followers are redundancy. "We replicated to five nodes so five consumers can read in parallel" misunderstands both quorum queues and streams — parallel reads across replicas are a stream feature, not a queue one.

> [!tip] Interview answer
> Scale in order: more competing consumers with tuned prefetch, verify via consumer capacity, then shard into multiple queues with modulus-hash or key routing to escape the single-queue core limit, and use streams when the need is throughput fan-out. Extra nodes improve availability, not one queue's speed.
