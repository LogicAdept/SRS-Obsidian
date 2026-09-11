<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What RabbitMQ metrics do you monitor

> [!abstract] Short answer
> The core set: queue depth split into ready and unacked, publish versus ack rates, consumer count and consumer capacity, memory and disk alarms, connection and channel counts for leaks, quorum replica health, DLQ growth, and redelivery rates. Prometheus plus Grafana is the recommended stack; the management UI is the interactive fallback.

## Queue-level metrics

Ready and unacked counts with their rates tell the queue's story: publish rate above ack rate means backlog, unacked pinned at prefetch means stuck handlers, consumer capacity under 100 percent means deliveries could go faster with more or faster consumers. Redelivery-heavy traffic signals requeue storms or poisoning. DLQ depth growth is the explicit failure alarm — it should be zero in healthy systems, with alerts on any sustained rise.

## Node and cluster metrics

Memory and free-disk watermarks drive resource alarms that block publishers broker-wide, so alarm state is a first-class metric. Connections and channels per node catch leaks (churn graphs in the UI); Erlang-process counts and scheduler usage come from the rabbitmq-top plugin for deep dives. For quorum queues, replica membership and leader locations matter: missing followers or a leaderless queue is an availability emergency regardless of traffic — the cluster mechanics are in [[What is RabbitMQ clustering]] and the crash playbook in [[What happens when a RabbitMQ node crashes]].

```d2
direction: down
q: "queue\nready, unacked, rates" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
cons: "consumers\ncount, capacity" {
  width: 190
  height: 80
  style.fill: "#fff3e0"
}
node: "node\nmem/disk alarms, conns, channels" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
qq: "quorum\nreplicas, leaders" {
  width: 200
  height: 80
  style.fill: "#ffebee"
}
dlq: "DLQ depth\nredeliveries" {
  width: 190
  height: 80
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Monitoring spans four layers: queue flow, consumers, node resources, replication health.

```bash
rabbitmqctl list_queues name messages_ready messages_unacknowledged consumers
rabbitmq-diagnostics alarms
```

**Listing 1.** CLI quick checks; Prometheus scraping covers the same plus history and alerting, as in [[What is the RabbitMQ management plugin]].

> [!warning] Queue depth alone lies
> A shallow ready count can hide thousands of unacked messages; a green queue can sit in a cluster with a missing quorum. Monitoring only depth misses the two most common outages — stuck consumers and replication loss — which is why the unacked, capacity, and replica metrics exist.

> [!tip] Interview answer
> I watch ready versus unacked and their rates, consumer count and capacity, DLQ growth and redeliveries per queue; memory and disk alarms, connection and channel leaks per node; and quorum membership and leadership per queue. Prometheus with Grafana for history, rabbitmqctl and the UI for live triage.
