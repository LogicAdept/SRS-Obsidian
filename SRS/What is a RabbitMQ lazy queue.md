<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is a RabbitMQ lazy queue

> [!abstract] Short answer
> Lazy mode was a classic queue option (`x-queue-mode: lazy`) that pushed all messages to disk as early as possible, keeping memory flat for huge backlogs. It is gone: since 3.12 classic queues behave like lazy queues by default, the setting is ignored, and the current docs keep the page for historical reference only.

## What it used to be

A lazy queue avoided the old default-vs-lazy trade-off: non-lazy classic queues kept as much as possible in memory for low latency and swapped to disk under pressure, causing memory spikes and alarms on big backlogs. Lazy mode reversed the priority — write-through to disk, minimal memory, higher latency for the first delivery of each message. Teams used it for nightly bulk queues, work queues with millions of pending jobs, and anything where RAM stability mattered more than milliseconds — the same scenarios that today point at [[What are RabbitMQ streams]] or a quorum queue.

```d2
direction: down
pre: "pre-3.12 choice" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
normal: "normal mode\nfast, RAM-hungry" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
lazy: "lazy mode\nslow first delivery, flat RAM" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
now: "3.12+\none hybrid behaviour" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
pre -> normal
pre -> lazy
normal -> now
lazy -> now
```

**Fig. 1.** The old two-mode split collapsed into one hybrid: disk-backed with a small dynamic in-memory window.

## What to say today

Current classic queues buffer briefly in memory, flush to disk with a small delay, and keep only a fast-delivery window of messages in RAM — roughly the lazy contract without the flag, and quorum queues store on the Raft log similarly. Declaring `x-queue-mode: lazy` today is silently ignored, and interview answers claiming lazy is a current knob are dated. See [[What RabbitMQ queue types exist]] for where backlogs really belong now.

```java
// Historical: Map.of("x-queue-mode", "lazy") — ignored since 3.12
Map<String, Object> args = Map.of("x-queue-type", "quorum");
ch.queueDeclare("bulk.jobs", true, false, false, args);
```

**Listing 1.** For large backlogs today the honest answer is a quorum queue or a stream, not a lazy flag.

> [!warning] Interview cheat sheets still sell lazy as current
> "Enable lazy mode for big queues" is a 3.x-era answer. In 4.x the flag does nothing, and describing it as active behaviour signals stale knowledge — the modern equivalents are the unified classic queue implementation and streams for very large retained backlogs, both part of [[What RabbitMQ queue types exist]].

> [!tip] Interview answer
> Lazy mode was a classic-queue flag that traded latency for flat memory by writing everything to disk early. Since 3.12 it is removed as a knob: classic queues now behave that way by default, and large-backlog work lands on quorum queues or streams rather than the lazy flag.
