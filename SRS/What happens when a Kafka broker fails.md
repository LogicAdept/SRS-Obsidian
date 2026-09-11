<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What happens when a Kafka broker fails?

> [!abstract] Short answer
> The controller notices that the broker's session is gone, removes it from the in-sync replica set of every partition it replicated, and elects new leaders for those partitions from the remaining in-sync replicas — batching the leadership-change notifications so recovery is one cheap wave, not one election per partition. Committed records survive as long as one in-sync replica of a partition remains, and the restarted broker rejoins only after fully re-syncing its log.

## The failure detection and recovery sequence

A broker is considered failed when it stops maintaining its session with the controller — in KRaft mode brokers send periodic heartbeats, and if the controller receives none before `broker.session.timeout.ms` expires the node is treated as offline. The controller then reassigns leadership for every partition the broker led, choosing among the remaining in-sync replicas, and pushes the changes out as a batched set of notifications; this batching is what makes the critical window of unavailability short even on clusters with thousands of partitions. Monitoring sees it directly: `LeaderElectionRateAndTimeMs` is expected to be non-zero exactly when there are broker failures, and the ISR shrink rate spikes for the affected partitions.

```d2
direction: down
fail: "broker crashes\nsession with controller lost" {
  width: 320
  height: 80
  style.fill: "#ffebee"
}
ctl: "controller times out the session\nremoves broker from all its ISRs" {
  width: 360
  height: 90
  style.fill: "#fff3e0"
}
elect: "new leaders elected from remaining ISR\nnotifications batched" {
  width: 360
  height: 90
  style.fill: "#e3f2fd"
}
serve: "clients follow the leader\ncommitted records preserved" {
  width: 340
  height: 90
  style.fill: "#e8f5e9"
}
fail -> ctl
ctl -> elect
elect -> serve
```

**Fig. 1.** Failure handling is controller-driven and set-at-a-time: detection, ISR surgery, batched re-election, then ordinary serving.

Clients ride it out rather than reconfiguring. Consumers only ever receive committed messages, so a leadership change does not expose them to records that might vanish. Producers discover the new leader through their refreshed metadata and keep retrying the in-flight sends — with `retries` effectively unbounded by default, the client resends any record whose send failed with a transient error, bounded in wall-clock time by `delivery.timeout.ms`. After a planned stop the picture is gentler: the broker default `controlled.shutdown.enable=true` lets the server hand its leadership over as part of shutting down instead of making every partition wait out the session timeout.

## What the surviving guarantees rest on

For each partition, committed records are safe while at least one in-sync replica lives — that is the promise `acks=all` leans on, and `min.insync.replicas` is the floor that stops the ISR from silently shrinking below a safe size. Records acknowledged under weaker settings (`acks=1`) live in the unreplicated tail above the high watermark and are lost if the leader dies before a follower replicates them. When the failed broker returns, it does not pretend its log is intact: it must fully re-sync with the leader before being readmitted to the ISR, even if it lost unflushed data in the crash, and Kafka deliberately requires no fsync-on-every-write or stable-storage guarantee for this to work.

> [!warning] The recovery is only as good as the ISR was before the failure
> If the ISR had already shrunk to just the leader, the controller has nobody to elect: the partition sits unavailable until that broker returns, or — with unclean leader election enabled — comes back on a possibly stale log. A single broker failure cascading into real loss is almost always preceded by an ignored `UnderReplicatedPartitions` alert. The election eligibility rules behind this are the ISR's, in [[What is the Kafka in-sync replica set]].

```properties
# broker-side recovery knobs (defaults shown)
controlled.shutdown.enable=true      # hand off leadership on planned stop
broker.session.timeout.ms=9000       # how long the controller waits for heartbeats
auto.leader.rebalance.enable=true    # move leadership back to preferred leaders later
```

**Listing 1.** After the wave of re-elections, automatic leader rebalance walks leadership back toward each partition's preferred leader so the load spreads evenly again — see [[What are under-replicated partitions in Kafka]].

> [!tip] Interview answer
> The controller detects the dead broker through its lost session, strips it from every ISR it belongs to, and elects surviving in-sync replicas as leaders in one batched notification set, so serving continues for every partition that had at least one other in-sync replica. Consumers are insulated because they only see committed records, and producers retry onto the new leader. The restarted broker must fully re-sync before rejoining any ISR, and a shrunken-ISR-beforehand situation is what turns this into data loss.

