<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is min.insync.replicas in Kafka?

> [!abstract] Short answer
> `min.insync.replicas` is the minimum number of in-sync replicas — including the leader — required for a write to succeed when the producer uses `acks=all`. If the ISR drops below the floor, `acks=all` writes are rejected with `NotEnoughReplicas` (or `NotEnoughReplicasAfterAppend`) instead of being acknowledged by a lone replica. The default is 1; the classic durability recipe is replication factor 3, `min.insync.replicas=2`, `acks=all`.

## The floor under acks=all

By default, `acks=all` acknowledgment happens as soon as all the *current* in-sync replicas have received the record — and "current" may be one replica if the others just died. The min ISR setting closes that hole: the partition accepts `acks=all` writes only while the ISR is at or above the configured size, and producers get an explicit exception rather than a silent durability downgrade. It has no effect on `acks=0` or `acks=1` writes, which never wait for the full ISR in the first place. The property is set as a broker default (cluster-wide dynamically updatable) and overridden per topic; since the strict min ISR rule arrived with the Eligible Leader Replicas feature, the high watermark of a partition also stops advancing while the ISR is below this floor — see [[What is the Kafka high watermark]].

```d2
direction: down
rf3: "topic RF=3\nmin.insync.replicas=2" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
ok: "ISR = 3 or 2" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
write: "acks=all write succeeds\nmajority holds the record" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
low: "ISR = 1" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}
reject: "producer gets NotEnoughReplicas\nconsumer reads committed prefix" {
  width: 340
  height: 90
  style.fill: "#ffebee"
}
rf3 -> ok
ok -> write
rf3 -> low
low -> reject
```

**Fig. 1.** With RF 3 and min ISR 2 the write path either keeps a majority of copies or fails loudly; availability for writes is deliberately sacrificed before durability is.

Consumer visibility is tied to the same floor: regardless of the producer's acks setting, messages become visible to consumers only after they are replicated to all in-sync replicas *and* the number of in-sync replicas is no less than `min.insync.replicas`. That is what makes the pairing with `acks=all` enforce a majority-persisted-before-acknowledged guarantee end to end.

## Configuration mechanics and the ELR interaction

The broker-level default is 1 and updates cluster-wide dynamically; per-topic overrides are the normal practice since durability requirements differ per topic. Enabling Eligible Leader Replicas (Kafka 4.0; default on new clusters from 4.1) changes some of the bookkeeping: a cluster-level `min.insync.replicas` is added if missing, removing it at cluster level is not allowed, broker-level values are removed and altering them at broker level is disallowed, and updating the topic-level value clears the ELR state. The reason is that ELR's promotion logic — ISR first, then eligible replicas — depends on the strict min ISR rule being uniformly defined for the cluster.

> [!warning] min.insync.replicas=1 is not a durability feature
> With the default value, `acks=all` still succeeds on a single in-sync replica, so the guarantee degrades to exactly the `acks=1` single-copy risk the setting exists to prevent. The second popular lie is the inverse: that the floor guarantees *every assigned replica* got the write — it only blocks writes when the ISR falls below the floor, it does not expand the acknowledgement set beyond the current ISR. The semantics of the acknowledgement set itself are in [[What is the difference between Kafka acks 0 1 and all]].

```bash
# per-topic override at creation
kafka-topics.sh --create --topic orders \
  --replication-factor 3 \
  --config min.insync.replicas=2
```

**Listing 1.** The standard production shape: RF 3 tolerates one broker loss for *reads and serving*, while min ISR 2 keeps `acks=all` writes on a majority — the failure handling around it lives in [[What happens when a Kafka broker fails]].

> [!tip] Interview answer
> `min.insync.replicas` is the ISR floor checked when a producer writes with `acks=all`: below it the partition throws `NotEnoughReplicas` instead of acknowledging a one-replica write, and consumer visibility also waits for replication to the full ISR at or above the floor. Default 1 — which is effectively no protection — and the standard recipe is RF 3 with min ISR 2, buying majority durability at the cost of write availability in degraded states.

