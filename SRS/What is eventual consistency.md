<!--
reps: 0
priority: 0
-->
#SystemDesign/Consistency #SRS

# What is eventual consistency

> [!abstract] Short answer
> Eventual consistency is the guarantee that if writes stop, all replicas will eventually converge to the same value — but reads during the window between write and convergence may return stale data. It is the consistency posture of asynchronously replicated and partitioned stores: writes stay available and fast, correctness is delayed rather than absolute, and the "inconsistency window" is bounded by network delays, load and replica count.

## The guarantee and its window

Under eventual consistency a write is acknowledged once the local copy (or a single replica) accepts it; other replicas reconcile in the background. Werner Vogels' canonical description — shaped by AWS's S3 and Dynamo experience — defines the observable consequence: an inconsistency window during which reads can return older data, its length determined by communication delays, system load and the number of replicas involved. The guarantee is convergence, not immediacy — which is why an integration test that asserts a read immediately after a send can fail: the message or update is accepted, but the read model or replica has not caught up. DNS is the classic convergent system (records propagate on their own schedule); async read replicas ([[How would you explain database replication strategies]]) are the database version; feed and cache updates are the application version. [[What is BASE as a consistency model]] names the posture this belongs to.

```text
t0  write x=1 accepted by replica R1       (client gets ack)
t1  read from replica R2 -> x=0            (stale, window open)
t2  R1 ships change; R2 applies            (converged)
t3  read from R2 -> x=1                    (window closed)
```

**Listing 1.** The window: acknowledged before converged, consistent after.

## Living with it: session guarantees and tests

Applications survive the window with targeted stronger guarantees rather than global strictness. Read-your-own-writes (a user sees their just-saved profile) is served by session consistency: sticky routing to the replica that took the write, monotonic read tokens, or quorum reads (R+W>N) per operation. Causal consistency preserves ordering within a conversation thread. The testing discipline changes too: assertions after async operations must await convergence explicitly (polling with a timeout — Awaitility-style), not sleep-and-hope, because fixed sleeps are flaky under load. The costs to state out loud: conflict handling when two replicas accept divergent writes (last-write-wins, CRDTs, application merge), and the discipline of deciding which reads truly need read-your-writes. [[How would you explain consistency in distributed systems and data stores]] places eventual consistency among its stronger siblings, and [[Why do some people say the CAP theorem is obsolete]] explains why this posture is the AP corner's everyday face.

> [!warning] "Eventually" does not answer "in what order"
> Plain eventual consistency says replicas converge, not that they converge in the same order or to the same winner without a conflict rule. Without deterministic resolution (timestamps, version vectors, CRDTs), two replicas can disagree forever — eventual needs a convergence mechanism, not just patience.

> [!tip] Interview answer
> Eventual consistency promises replica convergence after writes stop — reads during the window may be stale, with the window sized by network delay, load and replica count. It keeps writes fast and available; applications add read-your-writes routing, quorum reads and explicit await-based tests to cover the gap, plus deterministic conflict resolution.
