<!--
reps: 0
priority: 0
-->
#DistributedSystems #SystemDesign/Consistency #Databases #SRS

# How would you explain consistency in distributed systems and data stores

> [!abstract] Short answer
> Consistency in distributed systems is a ladder of guarantees about what reads see, not one property. From strongest: linearizability (every operation appears instantly atomic globally), sequential, causal, read-your-writes/session, monotonic reads, down to eventual (replicas converge when writes stop). Stronger costs more — extra round trips, waiting on replicas, unavailability during partitions — so real systems choose per operation.

## The ladder, concretely

Linearizability: after a write completes, any read from any node returns it or something newer — the system behaves like one atomic register; this is CAP's C and what consensus (Raft, Paxos) backs. Sequential: every node sees operations in the same total order, but that need not match real time. Causal: operations related by cause-and-effect (post then comment) are seen in order by everyone; unrelated ones may be seen in any order — cheap and sufficient for threads and feeds. Read-your-writes and session consistency: a client always sees its own writes, others may lag — the standard guarantee for user-facing profiles and settings. Monotonic reads: once a client has seen a value, it never sees an older one (prevents a replica failover from rewinding what a user read). Eventual: convergence only ([[What is eventual consistency]]) — the floor, not a model on its own. The database transaction level usually called "consistency" (ACID's C — [[What is the difference between atomicity and consistency]]) is about invariants on one node's committed state; the distributed ladder is about what replicas expose, and both matter.

## What each rung costs

The price is round trips and availability. Linearizability needs a quorum or leader round trip per read (or write) and blocks during partitions — the CP corner of [[How would you explain the CAP theorem]]; PACELC's point ([[Why do some people say the CAP theorem is obsolete]]) is that even without partitions, strong consistency pays latency. Quorum arithmetic (R+W>N) makes a store tunable per operation: N=3 with R=W=2 gives linearizable reads at two round trips; R=1, W=1 gives speed and a staleness window. Session and causal guarantees ride on metadata (session tokens, version vectors) and cost almost nothing — which is why the mature design keeps one linearizable path for money and invariants, and serves feeds, profiles and counters causally or eventually. Replication topology sets the reachable rungs: single-leader async caps at read-your-writes with sticky reads ([[How would you explain database replication strategies]]), while leaderless stores expose quorum knobs.

```text
linearizable   : read == latest write, globally      (quorum/leader RTT)
causal         : cause-before-effect, everywhere     (version vectors)
read-your-writes: my writes visible to me            (sticky/session token)
monotonic      : no rewinds after failover           (read tokens)
eventual       : converges when writes stop          (async lag window)
```

**Listing 1.** The ladder in one line each, with its typical mechanism.

> [!warning] Choosing "strong consistency" globally when only one path needs it
> Making every read linearizable to protect one financial invariant taxes the entire workload with quorum round trips and partition-blocking. The right design pins strong consistency to the invariant-touching operations and relaxes the rest deliberately.

> [!tip] Interview answer
> Consistency is a ladder: linearizable, sequential, causal, read-your-writes/session, monotonic, eventual — each defined by what reads may see, each bought with round trips or availability. I choose per operation: quorums or consensus where invariants live, session and causal guarantees for user-facing reads, eventual only where staleness is tolerable and conflicts are resolved.
