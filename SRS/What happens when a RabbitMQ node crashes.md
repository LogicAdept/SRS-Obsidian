<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What happens when a RabbitMQ node crashes

> [!abstract] Short answer
> Clients reconnect to surviving nodes (or a load balancer). Quorum queues elect a new leader if a majority remains and continue serving; a classic queue on the dead node is unavailable until that node returns. Metadata survives cluster-wide; transient queues vanish; resource alarms and replica catch-up need checking after restart.

## Immediate effects by queue type

A quorum queue with a surviving majority elects a leader within seconds and keeps publishing with confirms — availability holds. If the majority is gone, the queue stops accepting rather than risking data loss. A classic (non-replicated) queue hosted on the failed node is unreachable until the node is back, regardless of cluster health elsewhere. Streams keep serving if a replica majority remains. Connection-level: every client connected to the crashed node drops and must recover — connection recovery in client libraries rebuilds channels, consumers, and (server-named) queues.

```d2
direction: down
crash: "node dies" {
  width: 160
  height: 70
  style.fill: "#ffebee"
}
qq: "quorum queue\nmajority → new leader" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
cq: "classic queue\noffline until node returns" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
cli: "clients\nreconnect + recover" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
crash -> qq
crash -> cq
crash -> cli
```

**Fig. 1.** The blast radius depends on queue type and client recovery, not on the cluster itself.

## Recovery checklist

When the node returns: verify it rejoins the cluster and its replicas catch up, check memory and disk alarms before reopening traffic, confirm quorum leader placement rebalances, and watch for clients hammering re-declares — the reconnect race. The cluster context is [[What is RabbitMQ clustering]]; the data-safety prerequisites that make crash survival real are in [[How do you make a RabbitMQ message survive a broker restart]].

> [!warning] A recovered node does not automatically mean healthy
> A node that rejoins with stale disks may need to resync quorum replicas; serving traffic before alarms clear and replicas catch up turns a restart into an outage. Treat node return as a transition, not a completion.

> [!tip] Interview answer
> Clients recover to other nodes; quorum queues fail over on a majority and refuse writes without one; classic queues on the dead node simply disappear until it is back. After restart, rejoin, replica catch-up, alarms, and leader rebalancing decide when the node is actually safe again.
