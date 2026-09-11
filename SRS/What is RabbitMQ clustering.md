<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is RabbitMQ clustering

> [!abstract] Short answer
> A cluster is several RabbitMQ nodes acting as one logical broker: users, vhosts, exchanges, bindings, and policies replicate to all nodes, queues live on specific nodes (quorum queues replicate their contents), and any node can serve any client. Nodes authenticate via the Erlang cookie and must run compatible versions.

## What replicates and what does not

Topology and identity state — users, permissions, vhosts, exchanges, bindings, policies — replicates cluster-wide automatically. Queue contents do not by default: a classic queue lives on one node (its contents are not replicated; mirroring was removed in 4.0), a quorum queue replicates via Raft across its members, and streams replicate their log. Clients connect to any node and reach any non-exclusive queue transparently, with the broker routing operations to the right node; streams are the exception, requiring direct connections to replica nodes.

```d2
direction: down
meta: "replicated to all\nusers, vhosts, exchanges, bindings" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
n1: "node A\nclassic q on A" {
  width: 180
  height: 90
  style.fill: "#fff3e0"
}
n2: "node B\nquorum members" {
  width: 180
  height: 90
  style.fill: "#fff3e0"
}
n3: "node C\nquorum members" {
  width: 180
  height: 90
  style.fill: "#fff3e0"
}
meta -> n1
meta -> n2
meta -> n3
```

**Fig. 1.** Metadata is everywhere; queue contents live with their type — classic single-node, quorum replicated.

## Requirements and boundaries

Nodes must run compatible RabbitMQ and Erlang versions, share the Erlang cookie, and reach the distribution ports; the docs recommend odd node counts and strongly discourage two-node clusters. Clustering assumes LAN-like reliability — cross-DC topologies use federation or shovel, per [[What is the difference between clustering federation and shovel in RabbitMQ]]. Clustering alone is not durability: an unreplicated queue still dies with its node, which is the failure mode behind [[What happens when a RabbitMQ node crashes]].

> [!warning] Clustering is not replication of queues
> The most common cluster misconception: joining nodes does not copy queue contents everywhere. Data safety comes from choosing quorum queues or streams; a classic queue in a cluster is exactly as node-bound as a standalone one.

> [!tip] Interview answer
> A RabbitMQ cluster is one logical broker over several nodes: metadata replicates everywhere, clients use any node, and queue contents follow the queue type — classic on one node, quorum Raft-replicated, streams logged across replicas. Odd node counts, shared cookie, compatible versions, LAN links; federation and shovel for WAN.
