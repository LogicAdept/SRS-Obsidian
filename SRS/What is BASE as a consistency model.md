<!--
reps: 0
priority: 0
-->
#SystemDesign/Consistency #Databases/NoSQL #SRS

# What is BASE as a consistency model

> [!abstract] Short answer
> BASE — Basically Available, Soft state, Eventually consistent — is the consistency posture opposite to ACID: the system stays available for reads and writes during failures and partitions, tolerates temporary divergence (soft state), and guarantees only that replicas converge if writes stop. It is the model that large, partitioned, always-on stores adopted when strict ACID across nodes made them unavailable — and it is a spectrum of guarantees, not a single behavior.

## The three words, concretely

Basically available: the service answers requests even when parts of the system are down or disconnected — capacity and functionality may degrade, but the store does not turn unavailability into client errors ([[How would you explain the CAP theorem]] frames the availability goal it serves). Soft state: the stored state is allowed to change without new writes — replicas hold copies that reconcile in the background, so "the" value is provisional until convergence. Eventually consistent: if no new updates arrive, all reads eventually return the last written value; during the window between write and convergence, reads may return stale data — the inconsistency window Werner Vogels describes as bounded by communication delays, load and replica count. That guarantee is deliberately weaker than ACID's single-version truth ([[What are the ACID properties of database transactions]] for the contrast), and [[How would you explain consistency in distributed systems and data stores]] places BASE among the concrete consistency models.

## Why it exists and what it costs

BASE is the design answer to the CAP tradeoff under partition: for a partitioned, multi-master store, choosing availability over strict consistency yields a system where replicas diverge and heal — DNS, shopping carts, and most NoSQL stores live here. The cost shifts correctness work to the application: read-after-write may need read-your-own-writes support (sticky reads, quorum reads), conflicts need resolution (last-write-wins, CRDTs, application merge), and money-critical invariants usually cannot rely on eventual convergence alone. That is why BASE pairs naturally with compensating patterns: idempotent writes ([[What is idempotency in HTTP and in messaging]]), conflict resolution rules, and outbox/sagas for cross-entity workflows. Many engines make consistency tunable — quorum reads/writes let one cluster offer BASE at the default level and stronger guarantees per operation, which is the modern synthesis rather than a religion.

```text
ACID:   all copies agree before the write returns   (may be unavailable)
BASE:   write returns when one copy accepts it
        replicas reconcile in background (soft state)
        reads during window -> possibly stale; converges after
```

**Listing 1.** The same write under ACID and BASE postures.

> [!warning] "Eventually" is not "immediately"
> The inconsistency window can span a partition, a retry storm or a backlog — seconds to hours. Designing on BASE without deciding read-your-writes needs and conflict rules produces bugs that appear only under latency or partition, never in the test environment.

> [!tip] Interview answer
> BASE means basically available, soft state, eventually consistent: stay up during partitions, let replicas diverge temporarily, guarantee only convergence after writes stop. It buys availability and latency at the cost of stale reads and app-level conflict handling — the standard posture for large partitioned stores, ideally with tunable consistency per operation.
