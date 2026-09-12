<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceCollaboration #Patterns/DistributedSystems #SRS

# How would you explain the event sourcing pattern

> [!abstract] Short answer
> Event sourcing persists an aggregate as an append-only log of domain events — OrderCreated, OrderPaid, OrderShipped — instead of storing only current state. Current state is derived by replaying the events in order; new facts are appended, never updated or deleted. It is a core data pattern for microservices.

## The mechanism: log as truth, state as a fold

An event-sourced aggregate keeps three moving parts. The event store appends immutable events per aggregate, ordered, with a monotonic version — appends can require the expected current version, which gives aggregates optimistic concurrency over the log. State is a deterministic fold: replay the events and the aggregate reconstructs — the replay enforces the same invariants, so a rule violation surfaces on replay exactly where it happened ([[What is a command in CQRS]]'s commands trigger these events; [[What is the difference between a command and an event]] fixes the vocabulary). Snapshots store a folded state at a version so replays start near the tip ([[What is snapshotting in event sourcing]]). Projections fold the same events into query-shaped read models ([[What is a projection in CQRS and event sourcing]]) — in event sourcing this is the standard query path, not an optimization.

```d2
direction: right
cmd: "Command" {style.fill: "#fff3e0"}
agg: "Aggregate
load state = replay" {style.fill: "#e8f5e9"}
store: "Event store
append-only" {shape: cylinder; style.fill: "#fffde7"}
proj: "Projections" {style.fill: "#e3f2fd"}
qry: "Queries" {style.fill: "#eceff1"}
cmd -> agg
agg -> store: append events
store -> agg: replay to rebuild
store -> proj
proj -> qry
```

**Fig. 1.** The store is append-only truth; aggregate state and query views are folds over the same log.

```java
static Account replay(List<AccountEvent> events) {
    Account a = null;
    for (AccountEvent e : events) {
        if (e instanceof Opened o) a = new Account(o.id(), 0, 1);
        else if (e instanceof Deposited d) a = new Account(a.id(), a.balance() + d.amount(), a.version() + 1);
        else if (e instanceof Withdrawn w) {
            if (w.amount() > a.balance()) throw new IllegalStateException("insufficient funds at version " + a.version());
            a = new Account(a.id(), a.balance() - w.amount(), a.version() + 1);
        }
    }
    return a;
}
```

**Listing 1.** Verified on JDK 21 (G02_EventSourcingReplay in empirics): four events replay to `Account[id=acc-1, balance=120, version=4]`; after appending one more deposit, replay yields balance 125, version 5; a snapshot at version 4 plus the newer event reproduces the same state, and an over-withdrawal surfaces as `insufficient funds` during replay (out/G02_EventSourcingReplay.txt).

## Why teams adopt it — and pay for it

Benefits: complete audit history by construction; temporal queries (state as of any version); natural fit for event-driven integration — the log that rebuilds state also feeds consumers ([[How would you explain the polling publisher pattern]] and CDC are the bridge for stores that are not event stores). Costs: the query problem — the log answers nothing fast until projections exist; eventual consistency everywhere; versioned event schemas, since old events must replay forever (upcasters translate old formats); and a steep model shift — developers must think in facts, not rows. The convergent guidance: adopt event sourcing for aggregates where the audit trail or the event stream is itself a business requirement, not as a default persistence style ([[Which kinds of projects benefit most from CQRS]] applies to the pairing; [[What is BASE as a consistency model]] names the consistency contract). The same events, streamed to other services, are the payload of [[What is the domain event pattern in microservices]] - when the log is the source of truth, it doubles as the publication mechanism.

> [!tip] Interview answer
> Event sourcing stores an aggregate as an append-only sequence of domain events; current state is a deterministic replay of that log, snapshotted periodically to bound replay cost, and projections fold the same events into query views. I get a full audit trail, temporal queries and an integration-grade event stream, at the cost of eventual consistency, event schema versioning and a real modeling shift — so I reserve it for aggregates where history or the stream is a business requirement.
