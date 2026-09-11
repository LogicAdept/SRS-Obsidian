<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What triggers a Kafka consumer group rebalance?

> [!abstract] Short answer
> Anything that changes group membership or the subscription: a member joins, leaves, crashes or is evicted for a missed timeout, plus topic-side changes — new partitions on a subscribed topic or a new topic matching a subscribed pattern. What the rebalance costs depends on the protocol: the classic protocol pays a stop-the-world revoke of all partitions, while the new consumer protocol (KIP-848, GA since Kafka 4.0) moves partitions incrementally and leaves unaffected members untouched.

## The trigger list

The concrete events. Membership triggers:

* a new consumer joins the group (first `poll()` after `subscribe`);
* an existing consumer closes cleanly or unsubscribes;
* a consumer crashes — heartbeats stop, the broker drops it after `session.timeout.ms` (45 s by default);
* the consumer stops calling `poll()` long enough to exceed `max.poll.interval.ms` — the client then proactively leaves the group;
* a static member restarts and comes back after its session expired — it re-joins as a "new" member.

Topic-side triggers:

* partitions are added to a subscribed topic (`alter` the topic, then producers start writing to the new partitions);
* a topic matching a subscribed regular expression is created — periodic metadata refreshes notice it.

All of these funnel into one place: the group coordinator decides the current assignment is stale and starts a rebalance. The mechanics of that role are in [[What is a Kafka consumer group coordinator for]].

## Why the cost depends on the protocol

```d2
direction: right
trigger: "Member join / leave\npartition count change" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
classic: "Classic protocol\nJoinGroup + SyncGroup barrier" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
eager: "Eager assignor (Range):\nrevoke ALL partitions" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
coop: "CooperativeSticky:\nrevoke only moved partitions" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
consumerp: "group.protocol=consumer\nKIP-848, GA in 4.0:\nno global barrier" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
trigger -> classic
trigger -> consumerp
classic -> eager
classic -> coop
```

**Fig. 1.** The same trigger is cheap or expensive depending on which protocol and assignor the group runs. The eager path stops the whole group; the other paths keep consumers working on partitions they keep.

In the classic protocol the coordinator picks a group leader among the members, the leader computes the assignment, and every member collects its share through a `SyncGroup` barrier. With an eager assignor such as `RangeAssignor` (still first in the default `[RangeAssignor, CooperativeStickyAssignor]` list), members revoke all their partitions before rejoining — that is the stop-the-world pause the incremental cooperative protocol (KIP-429, Kafka 2.4) was built to remove. `CooperativeStickyAssignor` revokes only the partitions that actually move, so consumers keep fetching from the rest.

Since Kafka 4.0 the next-generation rebalance protocol (KIP-848) is generally available: set `group.protocol=consumer` and the coordinator itself computes a target assignment server-side and hands out changes piggybacked on heartbeats. There is no global synchronization barrier anymore — a member whose partitions do not change is not disturbed at all.

> [!warning] Rebalance is not only "a consumer joined"
> Interviewers often reduce rebalances to member churn. Metadata changes trigger them too: raising a topic's partition count while a group is subscribed, or creating a topic that matches a subscribed regex, restarts the whole procedure. The other common lie is that cooperative rebalancing removes the pause entirely — in the classic protocol cooperative members still wait behind a group-wide barrier during the handoff, and offsets cannot be committed while a member waits for the rebalance to finish. Only the KIP-848 protocol removes the barrier itself.

## How you reduce the impact

* Prefer `CooperativeStickyAssignor` (or move to `group.protocol=consumer` on Kafka 4.0+) so unaffected members keep working.
* Give restartable processes a `group.instance.id` — a rolling restart then reclaims the same partitions without a rebalance, see [[What is Kafka static group membership]].
* Keep heartbeats at about a third of the session timeout (`heartbeat.interval.ms` 3 s vs `session.timeout.ms` 45 s by default) so slow detection does not add spurious rebalances; the timeout pair is dissected in [[What is the difference between session.timeout.ms and max.poll.interval.ms]].
* Do not block the poll loop — the batch you return from `poll()` is bounded by `max.poll.records` (500 by default), which keeps the gap between polls predictable.

> [!tip] Interview answer
> A rebalance fires whenever membership changes — join, clean leave, crash detected via missed heartbeats, or a poll-gap timeout — and also when the subscription surface changes: new partitions on a subscribed topic or a new topic matching a subscribed pattern. The classic protocol runs it as a stop-the-world JoinGroup/SyncGroup barrier, cooperative sticky limits revocation to moved partitions, and the KIP-848 consumer protocol since 4.0 is fully incremental with the coordinator driving an incremental target assignment.
