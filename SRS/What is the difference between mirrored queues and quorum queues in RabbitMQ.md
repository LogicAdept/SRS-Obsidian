<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is the difference between mirrored queues and quorum queues in RabbitMQ

> [!abstract] Short answer
> Classic queue mirroring (policies `ha-mode`, `ha-params`) was a leader-plus-mirror replication with best-effort, split-brain-prone behaviour; quorum queues replace it with Raft majority replication. Mirroring was deprecated in 3.9 and removed in 4.0 — quorum queues are the only replicated queue today.

## How mirroring worked and why it lost

Mirroring copied the classic queue's messages to mirror nodes according to a policy (`exactly`, `all`, `nodes`). A publish was confirmed after the master processed it — mirrors replicated asynchronously, so confirmations could outlive data. Failover promoted the oldest mirror, and when a mirror was out of sync it either rejoined by discarding its messages or the queue halted — a documented split-brain and sync-storm class of problems. There was no majority notion: two nodes could each believe they led.

```d2
direction: down
m: "classic master" {
  width: 190
  height: 70
  style.fill: "#fff3e0"
}
mi1: "mirror (async)" {
  width: 190
  height: 70
  style.fill: "#ffebee"
}
mi2: "mirror (async)" {
  width: 190
  height: 70
  style.fill: "#ffebee"
}
conf: "confirm possible before\nmirrors caught up" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
m -> mi1
m -> mi2
m -> conf
```

**Fig. 1.** Async mirroring let confirms run ahead of replica durability — the core data-safety flaw quorum queues fix.

## What quorum changes

Quorum queues confirm only after a Raft majority persists, elections are fast and predictable, and a lost minority simply cannot commit — CAP-wise a CP structure, versus mirroring's looser AP behaviour. Trade-offs: higher disk and memory use, member management via policies, and no support for transient declarations. New durable replicated queues should always be quorum; mirroring knowledge matters only for legacy migrations, per [[What is a RabbitMQ quorum queue]] and [[What RabbitMQ queue types exist]].

> [!warning] "Mirrored classic queues are deprecated" is outdated wording
> Since 4.0 the correct statement is *removed*: `ha-mode` policies are ignored and mirrored clusters must migrate. Answering "mirroring is deprecated, use quorum" dates the knowledge to the 3.x era; current guidance is quorum queues or streams, full stop.

> [!tip] Interview answer
> Mirroring was policy-driven leader-plus-mirrors replication: asynchronous, confirm-unsafe, split-brain prone; deprecated in 3.9 and removed in 4.0. Quorum queues replicate through Raft, confirm on majority persistence, elect leaders predictably, and are the documented replacement for replicated queues.
