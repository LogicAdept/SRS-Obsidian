<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka consumer heartbeat thread for?

> [!abstract] Short answer
> It is a background thread inside the consumer that periodically tells the group coordinator "this member is alive". In the classic protocol it proves liveness between polls so a busy processing loop does not get the member evicted; in the KIP-848 consumer protocol the heartbeat also carries assignment changes back and forth, making it the transport for rebalances.

## Classic protocol: liveness between polls

After `subscribe`, the consumer automatically joins the group when `poll()` is invoked, and a background thread sends periodic heartbeats to the coordinator. Heartbeats are used to ensure that the consumer's session stays active and to facilitate rebalancing when members join or leave. The pacing is set by `heartbeat.interval.ms` (3 s by default), and the contract is explicit: the value must be lower than `session.timeout.ms` (45 s by default) and should typically be no higher than a third of it, so the broker has at least a couple of heartbeat chances to detect a dead member before the session expires. If the broker receives no heartbeat before the session timeout, it considers the consumer dead, removes it from the group, and starts a rebalance.

The essential subtlety: the heartbeat thread keeps beating even while your processing loop is stuck. A consumer that hung in a long handler still looks alive to the broker. That is why the group needs a second, progress-oriented timer — the poll-gap check described in [[What is the difference between session.timeout.ms and max.poll.interval.ms]] — and why "heartbeats alone keep my partitions" is a false model, covered in [[What are Kafka subscribe and poll for]].

```d2
direction: down
loop: "poll loop\nprocess batch" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
hb: "heartbeat thread\nheartbeat.interval.ms = 3 s" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
coord: "coordinator\nsession.timeout.ms = 45 s" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
evict: "no heartbeat before timeout\n-> remove member\n-> rebalance" {
  width: 300
  height: 100
  style.fill: "#ffebee"
}
alive: "session kept alive\nmember stays" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
loop -> hb
hb -> coord
coord -> evict: silence
coord -> alive: heartbeats
```

**Fig. 1.** The heartbeat thread runs beside the poll loop; the coordinator evicts a member only when the heartbeat stream goes silent for a full session timeout.

## Consumer protocol: the heartbeat becomes the protocol itself

Kafka 4.0 made the next-generation rebalance protocol (KIP-848) generally available. When the consumer sets `group.protocol=consumer`, the client-side `heartbeat.interval.ms` and `session.timeout.ms` configs are not supported: the broker controls pacing with `group.consumer.heartbeat.interval.ms` (5 s default) and `group.consumer.session.timeout.ms` (45 s default). The new `ConsumerGroupHeartbeat` request is more than a ping — the coordinator piggybacks on it to assign or revoke partitions and each member reports its current state back, so the heartbeat stream is also the reconciliation loop that drives incremental rebalances.

> [!warning] Heartbeat frequency is not a tuning toy
> Setting `heartbeat.interval.ms` close to `session.timeout.ms` risks eviction from one lost heartbeat or a transient GC pause on the broker side of the timeout race. The documented rule keeps it under a third of the session timeout. Lowering it further does not make the group more correct — it only adds request traffic and marginally speeds up the expected time for normal rebalances.

> [!tip] Interview answer
> The heartbeat thread sends periodic liveness signals to the group coordinator — every 3 seconds by default, capped at a third of the 45-second session timeout — so the broker can detect crashed members and rebalance their partitions. Under the KIP-848 consumer protocol the same heartbeat is upgraded: the broker sets its interval and uses it to push incremental assignment changes during rebalances.

