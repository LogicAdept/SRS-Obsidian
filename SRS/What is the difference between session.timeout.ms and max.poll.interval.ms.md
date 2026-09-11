<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the difference between session.timeout.ms and max.poll.interval.ms?

> [!abstract] Short answer
> `session.timeout.ms` is a liveness timer watched by the broker: if no heartbeat arrives within it, the coordinator declares the consumer dead and rebalances. `max.poll.interval.ms` is a progress timer watched by the client: if you do not call `poll()` within it, the consumer decides it is stuck and proactively leaves the group. One catches a crashed process; the other catches a livelocked one that keeps heartbeating.

## The two failure modes

| | `session.timeout.ms` | `max.poll.interval.ms` |
|---|---|---|
| Detects | crashed or partitioned process | hung or too-slow processing loop |
| Watched by | broker (coordinator) | consumer itself |
| Signal | heartbeats stop arriving | no `poll()` call in the window |
| Default | 45000 (45 s) | 300000 (5 min) |
| Reaction | broker removes the member, rebalance | client leaves the group proactively |
| Linked knob | `heartbeat.interval.ms` (3 s, ≤ 1/3 of session) | `max.poll.records` (500) |

The two timers split the failure space cleanly. If the consumer crashes or is unable to send heartbeats for `session.timeout.ms`, it is considered dead and its partitions are reassigned — the heartbeat machinery behind that signal is [[What is the Kafka consumer heartbeat thread for]]. The livelock case is separate — a consumer can keep sending heartbeats while making no progress (a handler blocked forever, an infinite loop after a poison record). To keep such a member from holding its partitions indefinitely, the client checks the gap between `poll()` calls against `max.poll.interval.ms` and leaves the group on its own; the next offset commit then fails with `CommitFailedException`, the manual-commit contract from [[What are Kafka commitSync and commitAsync for]].

## What happens next, member by member

For a dynamic member, leaving the group means the coordinator rebalances and the partitions move to someone else — the evicted member's seats are filled through the flow in [[What are Kafka subscribe and poll for]]. For a static member (non-empty `group.instance.id`) the timeout is deliberately softer: the consumer stops sending heartbeats, but its partitions are not immediately reassigned — they are reassigned only after the session timeout expires, mirroring a static consumer that shut down. That asymmetry is a documented property of [[What is Kafka static group membership]], not a bug.

Under the KIP-848 consumer protocol (`group.protocol=consumer`, GA in Kafka 4.0) the split becomes explicit: `session.timeout.ms` is not a supported client config — the session length is controlled by the broker via `group.consumer.session.timeout.ms` — while `max.poll.interval.ms` remains a client-side concern.

## Tuning both together

* Raise `max.poll.interval.ms` when a batch legitimately needs more time; the documented drawback is that the consumer joins a rebalance only inside `poll()`, so a large poll interval can delay group recovery.
* Lower `max.poll.records` to shrink each batch so the loop predictably fits the interval.
* Keep `heartbeat.interval.ms` at about a third of `session.timeout.ms` so crash detection is fast without timing races.
* For unpredictable processing time, move processing to another thread: keep polling (and pause partitions while the worker drains), which decouples progress from processing speed; auto-commit makes that race worse, as laid out in [[Why is Kafka enable.auto.commit dangerous]].

> [!warning] The popular lie: "heartbeats keep my partitions while I process"
> No — heartbeats only keep the session. A consumer that heartbeats steadily but stops polling is evicted by its own client through the poll-gap timeout, and the first visible symptom is a `CommitFailedException` on the next `commitSync()`. The inverse lie is that raising `session.timeout.ms` buys slow processors time; it only delays crash detection while the poll-gap timeout still evicts the stuck member.

> [!tip] Interview answer
> session.timeout.ms is broker-side crash detection: no heartbeat for 45 seconds by default and the coordinator evicts the member. max.poll.interval.ms is client-side progress detection: no poll call for 5 minutes by default and the consumer leaves the group itself, so the next commit throws CommitFailedException. One guards against dead processes, the other against livelocked ones — slow processing is fixed with max.poll.records and worker threads, not with heartbeats.

