<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is rack awareness in Kafka?

> [!abstract] Short answer
> Rack awareness means tagging every broker with its physical placement via `broker.rack` (a rack, an availability zone, a fault domain) so the replica assigner spreads each partition's replicas across different racks. The documented purpose is fault tolerance: a lost rack — one switch, one power feed, one zone — then removes at most one replica per partition instead of all of them. The config defaults to null, which makes placement topology-blind.

## Placement: replicas across fault domains

Hardware failures correlate: brokers behind one top-of-rack switch or on one power circuit fail together, and cloud availability zones have the same property. `broker.rack` feeds exactly this information into replica assignment — the broker config is documented as the input for rack-aware replication assignment for fault tolerance. With replication factor 3 and at least three racks, a partition's replicas land on three distinct racks, so losing a rack degrades those partitions to under-replicated rather than offline; when the cluster has fewer racks than the replication factor, some replicas must share a rack and the protection is correspondingly partial. The leadership side is separate: automatic leader balancing moves leadership back to each partition's preferred leader (`auto.leader.rebalance.enable`), a load optimization that does not consult racks.

```d2
direction: right
rack1: "RACK1\nbroker 1: leader" {
  width: 240
  height: 100
  style.fill: "#e8f5e9"
}
rack2: "RACK2\nbroker 2: follower" {
  width: 240
  height: 100
  style.fill: "#e3f2fd"
}
rack3: "RACK3\nbroker 3: follower" {
  width: 240
  height: 100
  style.fill: "#e3f2fd"
}
lost: "RACK2 switch dies\npartition still served" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
rack1 -> lost
rack2 -> lost
rack3 -> lost
```

**Fig. 1.** With replicas spread over three racks, one rack's failure costs the partition one follower; the ISR shrinks, the leader keeps serving, and the cluster re-replicates elsewhere.

The read side has a matching knob: consumers and other clients may set `client.rack`, any string saying where the client physically sits, corresponding to the broker's `broker.rack`. Rack-aware replica selection then lets a client in the same domain fetch from a co-located replica instead of always crossing the rack boundary — useful when the "racks" are zones and inter-zone traffic is billed and slow.

## What rack awareness is not

It is not a cross-datacenter replication scheme. The operations documentation is explicit that a single Kafka cluster stretched across datacenters over high-latency links is generally not advisable: writes pay the replication latency of the slow link on every commit, and a WAN outage makes the cluster unavailable or partitioned between locations. The recommended pattern is one local cluster per datacenter, applications talking only to their local cluster, and inter-cluster mirroring for the global view — see [[What is Kafka MirrorMaker for]]. Rack awareness is for tightening replica placement *inside* one cluster.

> [!warning] Naming a rack does not make the cluster survive a region
> `broker.rack` only influences where the assigner puts replicas; it does not add capacity, does not slow re-replication after a rack loss, and does nothing at all if you leave it unset while assuming the assigner is topology-aware. The common production trap is a cloud deployment where "zones" exist but `broker.rack` was never configured, so all replicas of a partition may land in one zone — the outage then takes out every copy at once. Check the resulting spread with the partition-state in [[What is the Kafka in-sync replica set]] and the alerts in [[What are under-replicated partitions in Kafka]].

```properties
# each broker names its fault domain
broker.rack=us-east-1d
# the read-side counterpart on clients
client.rack=us-east-1d
```

**Listing 1.** Both settings are strings — any consistent labeling works, as long as brokers in the same rack share the value and brokers in different racks do not.

> [!tip] Interview answer
> Rack awareness is `broker.rack`-driven replica placement: Kafka spreads each partition's replicas over distinct fault domains so a single rack or zone failure cannot kill all copies at once, and clients can set `client.rack` to fetch from a nearby replica. It is intra-cluster protection — for spanning datacenters the docs recommend separate clusters per site with mirroring, not one stretched cluster.

