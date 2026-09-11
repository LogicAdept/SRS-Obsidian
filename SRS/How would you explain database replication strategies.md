<!--
reps: 0
priority: 0
-->
#Databases/Replication #SystemDesign/Reliability #SystemDesign/Availability #DistributedSystems #SRS

# How would you explain database replication strategies

> [!abstract] Short answer
> Replication keeps copies of data on multiple servers, and the strategies differ in when the copy is confirmed: synchronous waits for the replica before committing (no data loss, higher write latency), asynchronous returns immediately (fast writes, replication lag and possible loss on failure), semi-synchronous requires one confirmed replica as a middle ground. Topology adds single-leader (simple, writes funnel through one primary), multi-leader (multi-site writes, conflict resolution needed) and leaderless (quorums).

## Timing: sync, async, semi-sync

The core knob is what a commit waits for. Synchronous replication commits only after the replica has durably received the change — a primary failure loses nothing, but every write pays a network round trip and a downed replica can block writes. Asynchronous commits locally and ships changes in the background — write latency ignores replica speed, but a primary crash can lose the last unreplicated transactions (the replication lag is the inconsistency window). PostgreSQL implements the spectrum in one setting: synchronous_commit off, on (wait for standby flush of WAL), remote_write, or remote_apply (wait until the replica has applied and made rows visible — the strongest, slowest point). Semi-synchronous formalizes the middle: MySQL's plugin makes the primary wait for exactly one replica to acknowledge receipt (its wait point configurable at AFTER_SYNC or AFTER_COMMIT), degrading to asynchronous if no replica responds in time. [[How would you explain PostgreSQL replication strategies]] and [[How would you explain MySQL replication strategies]] show both engines concretely; [[What is eventual consistency]] names the read-side consequence of async lag.

## Topology: who accepts writes

Single-leader replication routes all writes through one primary with read-only replicas — no conflicts, but a failover moment and a write bottleneck. Multi-leader lets several nodes accept writes (geographically distributed clusters) and must resolve concurrent conflicting writes — last-write-wins, per-field merge or CRDTs. Leaderless systems (Dynamo-style) let clients write to any of N replicas with quorum overlap deciding visibility — tunable consistency per operation. These combine with the timing axis: a single-leader async setup and a leaderless quorum cluster can offer the same read-your-writes properties at very different operation counts. [[How would you explain consistency in distributed systems and data stores]] maps the topologies to consistency models, and [[What problem does database sharding solve]] is orthogonal — replication copies each shard, sharding splits rows across primaries.

```text
sync:     client -> primary -> [replica ack] -> commit returns   (loss=0)
async:    client -> primary -> commit returns; replica lags      (loss=lag)
semi:     client -> primary -> 1 replica ack -> commit returns
topology: 1 leader | N leaders | 0 leaders (quorum writes)
```

**Listing 1.** The two independent axes: when a copy is confirmed, and who may accept writes.

> [!warning] Async replication silently rereads the durability contract
> With async, "committed" no longer means "survives primary loss" — the last lagged transactions can vanish at failover. Applications must know which setting they run under, because the guarantee changed without any API change.

> [!tip] Interview answer
> Replication strategy has two axes. Timing: synchronous (no loss, slower writes), asynchronous (fast, can lose lagged writes), semi-sync (one confirmed replica). Topology: single-leader for simplicity, multi-leader for multi-site writes with conflict resolution, leaderless with quorums. The choice sets the durability-versus-latency and consistency-versus-availability trade the application lives with.
