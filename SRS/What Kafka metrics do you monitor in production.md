<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What Kafka metrics do you monitor in production?

> [!abstract] Short answer
> Four broker red lines — `UnderReplicatedPartitions`, `UnderMinIsrPartitionCount`, `OfflinePartitionsCount`, and exactly one `ActiveControllerCount` per cluster — plus throughput and idle-percent for capacity, and the client sides: producer buffer and request latency, consumer lag and poll health.

## Broker red lines and capacity

```properties
# red lines — alert the moment they are nonzero (controller: exactly one)
kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions      # expect 0
kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount      # expect 0
kafka.controller:type=KafkaController,name=OfflinePartitionsCount    # expect 0
kafka.controller:type=KafkaController,name=ActiveControllerCount     # expect 1 cluster-wide
# capacity
kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent  # ideally > 0.3
kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec              # + BytesOutPerSec, MessagesInPerSec
```

**Listing 1.** The broker-side MBeans worth alerting on, with the healthy values.

The red lines catch replication damage before data loss: under-replicated partitions mean some replica fell behind or died ([[What are under-replicated partitions in Kafka]]), under-min-ISR partitions are the stricter state where producers with `acks=all` must already be failing ([[What is min.insync.replicas in Kafka]]), offline partitions mean reads and writes are actually blocked, and a controller count other than one is a cluster-level fault ([[What is the Kafka controller]]). Capacity shows in `RequestHandlerAvgIdlePercent` — sustained idling below 0.3 means request threads are saturated — and in the per-topic `BytesIn/BytesOut/MessagesIn` rates, including the replication traffic variants that reveal whether normal traffic or reassignment is eating bandwidth.

## Client sides

```properties
kafka.producer:type=producer-metrics,client-id={client-id}
    buffer-available-bytes             # headroom before send() blocks
    buffer-exhausted-rate              # nonzero means the accumulator ran dry
    request-latency-avg                # per node; localizes slow brokers
kafka.consumer:type=consumer-fetch-manager-metrics,client-id={client-id}
    records-lag-max                    # worst per-partition lag for this client
kafka.consumer:type=consumer-metrics,client-id={client-id}
    poll-idle-ratio-avg                # ~0: processing-bound, not data-starved
    last-poll-seconds-ago              # approaching max.poll.interval.ms / 1000 is a red flag
```

**Listing 2.** The client-side MBeans that complete the picture, with the reading that matters.

On producers, `buffer-available-bytes` and `buffer-exhausted-rate` surface backpressure before users feel `send()` blocking, and `request-latency-avg` per node localizes slow brokers. On consumers, `records-lag-max` tracks the worst per-partition lag ([[What is Kafka consumer lag and how do you debug it]]), while `poll-idle-ratio-avg` and `last-poll-seconds-ago` distinguish "no data" from "cannot keep up" and warn before a `max.poll.interval.ms` eviction. All of these arrive through JMX under the `kafka.server`, `kafka.controller`, `kafka.producer`, and `kafka.consumer` domains, which is why the MBean names themselves are the interview-relevant detail — any scraper (Prometheus JMX exporter, Datadog, whatever) just reads those coordinates.

> [!warning] "Broker is up" is not a health check
> A broker process can answer health probes all day while its partitions sit under-replicated, or while it holds a second controller. Process liveness and cluster health are different signals — alerts fire on the red lines and on lag trends, not on systemd state or TCP reachability. [[What happens when a Kafka broker fails]] is what these metrics are watching for.

> [!tip] Interview answer
> I watch four broker red lines — under-replicated, under-min-ISR, offline partitions, and exactly one active controller — plus request-handler idle percent and per-topic traffic for capacity; on clients, producer buffer exhaustion and request latency, consumer lag and poll behavior. The principle: alert on symptoms like replication damage and lag growth, not on process liveness, because a broker can be up and still broken.
