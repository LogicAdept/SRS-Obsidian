<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Channels #SRS

# What is the Channel Purger pattern?

> [!abstract] Short answer
> A **Channel Purger** removes unwanted **left-over messages** from a channel — all of them, or a selection by message ID or field values — so stale messages do not disturb tests or a running system after redeployments or format changes.

## Why stale messages linger at all

Persistent, asynchronous messaging keeps delivering what it kept: after a failed test run or a redeploy that changed a message format, a queue can still hold messages that nobody can meaningfully process — or worse, messages that process "successfully" and corrupt state, like the reply that answered a request that never happened. The purger drains a channel: a simple purge removes everything (usually enough to reset a test system into a consistent state), while a production-grade purge removes messages matching criteria such as a message ID or a header value. Purging is a management operation, so it is typically invoked through a [[What is the Control Bus pattern]] command rather than application code; on AMQP it maps to the `queue.purge` method, on SQS-hosted systems to a purge API, and on JMS — which has no standard purge — to admin tooling plus a [[What is the Test Message pattern]]-style rehearsal.

```d2
direction: left
q: "orders.work\nstale + valid mixed" {
  width: 210
  height: 70
  style.fill: "#ffebee"
}
purge: "Channel Purger\nall / by selector" {
  width: 210
  height: 70
  style.fill: "#fff3e0"
}
cb: "Control Bus\npurge command" {
  width: 190
  height: 65
  style.fill: "#e3f2fd"
}
cb -> purge -> q: "drain"
q -> dlq: "quarantine survivors\n(optional)" {
  width: 220
  height: 65
  style.fill: "#e8f5e9"
}```

**Fig. 1.** The purge is triggered out-of-band; a careful purge quarantines survivors instead of deleting them.

## Choosing what to remove

```text
Purge mode            Use when                          Risk
--------------------  --------------------------------  ----------------------
Drain all             test reset, format break          data loss if used in prod
By message ID         one poisoned entry                selection must be exact
By field/selector     batch of bad v1 payloads          selector drift drops good msgs
Move, then delete     production incidents              slower, needs quarantine
```

**Listing 1.** In production the safe sequence is select, move to quarantine, verify, then delete — the delete-then-regret order has no undo.

> [!warning] Purging a queue is destructive and order-sensitive
> A drained queue also throws away messages a slow-but-legitimate consumer has not reached yet, and purging does not retract copies already delivered or dead-lettered. Coordinate the purge with consumer downtime and treat "purge" plus "replay from source" as one procedure, not two independent ops.

> [!tip] Interview answer
> A Channel Purger drains unwanted messages from a channel — everything, or a filtered subset by ID or field — typically via a control-bus command. It exists because persistent channels keep stale messages alive across redeploys and tests, and those messages can later hit consumers unexpectedly. In production you purge by selection into quarantine rather than blind drain, and you coordinate with consumers.
