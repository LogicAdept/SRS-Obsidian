<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# How does RabbitMQ preserve message order

> [!abstract] Short answer
> A queue is FIFO and preserves publication order per channel, but observed order breaks with multiple consumers, requeue/redelivery, priorities, or multi-channel publishing. Guarantees need either one active consumer (or one consumer) on the queue, or streams, or per-key sharding with single consumers.

## What the broker promises

Messages published on one channel through one exchange into one queue are enqueued in publish order, and the queue holds them in publication order even across requeues (since 2.7.0, requeues go back to their original position when possible). What can still reorder: redelivery after crashes or nacks, priority queues dispatching high-first, and interleaving when several channels publish concurrently — those sequences race through routing.

```d2
direction: down
fifo: "single consumer\nFIFO kept" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
multi: "multiple consumers\nrequeues reorder" {
  width: 220
  height: 80
  style.fill: "#ffebee"
}
sac: "single active consumer\norder kept, failover ready" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
stream: "stream\nper-consumer offsets" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
multi -> sac: "fix: SAC"
multi -> stream: "fix: streams"
```

**Fig. 1.** The reordering sources and the two documented repairs: single active consumer or streams.

## The documented fixes

Single Active Consumer keeps exactly one consumer active on the queue with automatic failover to a standby — order preserved, availability kept. Quorum queues add a delivery limit so requeues go to the front deterministically. For per-entity order at scale, shard by key (modulus-hash exchange) into queues with single active consumers. Streams give each consumer its own offset over an append-only log — order within the stream, replayable. The dispatch base is [[How do competing consumers work in RabbitMQ]]; the scaling story is [[How do you scale RabbitMQ consumers]].

```java
Map<String, Object> args = Map.of("x-single-active-consumer", true);
ch.queueDeclare("ledger.eu", true, false, false, args);
```

**Listing 1.** SAC declaration; standby consumers sit idle until the active one dies.

> [!warning] Priority queues and order are enemies
> Enabling priorities explicitly reorders dispatch — that is the feature. Teams combine "strict order" requirements with priority levels and then debug "random" reordering; the honest answer is per-entity sharding with ordered substreams, not a single ordered priority queue.

> [!tip] Interview answer
> Order is per channel-to-queue FIFO, held even across requeues, but observed order breaks with multiple consumers, redeliveries, and priorities. Guarantees come from single active consumer on one queue, per-key sharding, or streams with offsets. Global order and parallelism are fundamentally in tension.
