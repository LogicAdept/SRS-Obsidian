<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What causes a RabbitMQ queue to back up

> [!abstract] Short answer
> The usual causes: consumers slower than publishers, dead or missing consumers, unacked deliveries piling up under stuck handlers or oversized prefetch, poison requeue loops, and traffic funneled into one hot queue. The fix targets the cause — scale consumers, bound the queue with max-length plus DLX, tune prefetch — not just deeper graphs.

## Diagnosis by state

Ready messages growing with zero consumers means missing subscriptions — often after a deploy or an exclusive/auto-delete lifecycle surprise. Ready growing while consumers exist means throughput shortfall: slow handlers, insufficient consumer count, or a saturated single-core queue. Unacked growing means consumers hold work without finishing: prefetch too high, handler blocked on a slow dependency, or a stuck loop — the poison scenario in [[What is a poison message in RabbitMQ]]. The consumer capacity metric (fraction of time the queue can deliver immediately) separates "needs more consumers" from "needs faster consumers".

```d2
direction: down
ready: "ready grows\nslow/few consumers" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
unack: "unacked grows\nstuck handlers, prefetch" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
fix1: "more consumers, sharding" {
  width: 230
  height: 80
  style.fill: "#e8f5e9"
}
fix2: "lower prefetch, fix handler" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
ready -> fix1
unack -> fix2
```

**Fig. 1.** Which state is growing tells you which lever to pull.

## Bound the failure

Queue limits are the blast-radius tool: max-length with reject-publish applies backpressure through publisher confirms instead of dropping history, and a DLX catches overflow and dead-lettered poisons for later triage. Monitoring the growth trends — publish rate versus ack rate — predicts the backup before it happens; the metric set is in [[What RabbitMQ metrics do you monitor]], and the scaling playbook in [[How do you scale RabbitMQ consumers]].

> [!warning] A bigger queue is not the fix
> Raising max-length or removing TTL to "absorb" a backup moves the failure later: memory and disk alarms will block publishers broker-wide, hitting every vhost. Backpressure (reject-publish) plus consumer scaling is the documented pattern; infinite buffering is an anti-pattern.

> [!tip] Interview answer
> Backups come from consumer shortfall, dead consumers, unacked pressure via stuck handlers or fat prefetch, poison loops, or single hot queues. Diagnose by ready-versus-unacked and consumer capacity, fix with consumers and prefetch, and bound the queue with max-length reject-publish plus a DLX instead of letting it eat the node.
