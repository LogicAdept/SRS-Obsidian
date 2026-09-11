<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What are under-replicated partitions in Kafka?

> [!abstract] Short answer
> A partition is under-replicated when the number of in-sync replicas is smaller than the number of assigned replicas — some follower has died or fallen too far behind, so the partition is running with less redundancy than configured. The broker gauge `UnderReplicatedPartitions` counts them and its healthy value is 0. It is a durability warning, not data loss by itself: the data is still served, but the next failure has far less to fall back on.

## What the metric measures

The documented gauge is `kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions`, defined as |ISR| < |all replicas|, with 0 as the expected value. Every eviction from an ISR on that broker moves a partition into the count: a crashed follower loses its controller session and is dropped, a lagging follower is dropped by the leader once it cannot reach the leader's log end offset within `replica.lag.time.max.ms` (30 seconds by default). The companion rates tell you which shape you have — `IsrShrinksPerSec` and `IsrExpandsPerSec` are both expected to be 0 outside broker restarts, and when the failed broker returns, its partitions leave the count as the ISR expands once the replicas are fully caught up.

```d2
direction: right
healthy: "partition RF=3\nISR = {leader, A, B}" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
fail: "broker holding B dies\nor B lags past 30 s" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
shrunk: "ISR = {leader, A}\nURP count +1" {
  width: 250
  height: 80
  style.fill: "#ffebee"
}
heal: "B returns and catches up\nISR expands, URP -1" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
healthy -> fail
fail -> shrunk
shrunk -> heal
```

**Fig. 1.** Under-replication is a transient state on the healthy path — the metric only becomes an incident when it does not return to zero after the member recovers.

## Causes worth distinguishing

A broker that is down (crash, restart, network partition) explains a burst of under-replicated partitions on every partition it replicated — that is the benign case if it comes back. A *live* broker whose partitions stay under-replicated points at a lagging follower: overloaded disks, network saturation, or a broker hosting so many partitions or leaders that its fetchers cannot keep up. A failed log directory also takes its replicas out of service. The count to watch next to it is `UnderMinIsrPartitionCount`, defined as |ISR| < `min.insync.replicas`: that one marks partitions where `acks=all` writes are actually being rejected with `NotEnoughReplicas` rather than merely running degraded — see [[What is min.insync.replicas in Kafka]].

> [!warning] Under-replicated is not "replicas are copying data" noise
> The most expensive reading of this alert is to ignore it because consumers still see no errors. With the ISR shrunken, acknowledged records may be living on one broker; if that broker then fails, the partition is either unavailable or — with unclean leader election on — rewound to a stale log. Sustained URP means your durability cushion is gone; treat it as a capacity or health incident on the lagging broker, not as a cosmetic gauge. The eviction mechanics are the ISR's in [[What is the Kafka in-sync replica set]].

```bash
# the gauge and its rates, as documented for production monitoring
kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions   # expect 0
kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount   # expect 0
kafka.server:type=ReplicaManager,name=IsrShrinksPerSec            # 0 outside restarts
kafka.server:type=ReplicaManager,name=IsrExpandsPerSec            # 0 outside restarts
```

**Listing 1.** The four-gauge picture: how many partitions lost redundancy, how many also lost write availability, and whether the ISR is churning.

> [!tip] Interview answer
> Under-replicated partitions are partitions whose ISR shrank below the assigned replication factor — the gauge `UnderReplicatedPartitions` counts them and should be 0. They appear when a broker dies or a follower lags past `replica.lag.time.max.ms`, and they clear when the member catches up. They are not data loss and not yet unavailability, but they mean the next failure is much closer to actual loss, which is why the sister metric `UnderMinIsrPartitions` — partitions below `min.insync.replicas` — is the one that blocks `acks=all` writes.

