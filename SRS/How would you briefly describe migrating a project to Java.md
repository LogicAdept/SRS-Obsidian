<!--
reps: 0
priority: 0
-->
#SystemDesign/Architecture #Career/Java #SRS

# How would you briefly describe migrating a project to Java

> [!abstract] Short answer
> A migration to Java is run incrementally, not as a rewrite: carve the target system into modules by business capability, integrate the new Java services with the legacy core through an interposed facade (strangler-fig style — new growth replaces old around the edges while the old core keeps serving), keep data honest (owned per service, synchronized until cutover), and move traffic piece by piece with rollback at every step. The plan's deliverables are a capability map, an integration seam, a data strategy, and a per-module cutover order driven by risk and value.

## The strangler path, concretely

Fowler's strangler-fig application pattern is the standard shape: gradually build the new system around the edges of the old and let it grow until the old is enclosed — new capabilities are built as Java services, and an interposing facade (API gateway or reverse proxy) routes each request either to the legacy core or to its Java replacement, one route at a time. The sequence that works: first, stabilize the seam — define contracts for the pieces being extracted (REST/gRPC, events); second, extract low-risk, high-churn modules first (reporting, notifications, a CRUD slice) to prove the toolchain (build, CI/CD, observability, deployment) while blast radius is small; third, migrate the core transactional pieces last, only after the platform has production mileage. Each extracted service is stateless where possible ([[What is the difference between a stateful service and a stateless service]]), owns its data going forward, and integrates with legacy via the facade plus events ([[How does an aggregate persist and publish events without a distributed transaction]]'s outbox keeps the legacy database and new services synchronized without 2PC). The facade also carries traffic-splitting: percentage routing and shadow traffic give the per-module rollback lever — any regression reroutes to legacy instantly.

```d2
direction: right
facade: {
  label: "facade / gateway\nroute per capability\n+ shadow traffic"
  width: 220
  height: 80
}
legacy: {label: "legacy core\n(still serving migrated-away routes? no)" ; width: 190; height: 80}
j1: {label: "java: reporting\n(step 1, low risk)"; width: 180; height: 70}
j2: {label: "java: orders\n(step N, core)"; width: 150; height: 70}
bus: {label: "event bus / outbox sync"; width: 200; height: 60}
facade -> legacy: "not-yet-migrated"
facade -> j1: "route 1"
facade -> j2: "route N"
j2 -> bus: "events"
legacy -> bus: "CDC"
```

**Fig. 1.** Strangler migration: the facade routes per capability; events keep old and new stores coherent.

## The decisions that make or break it

Data is the hard third: each migrated capability needs a data strategy — coexistence (legacy DB remains source of truth, Java reads via the facade), synchronization (CDC/outbox to the new store, [[What is eventual consistency]]-bounded), or cutover (dual-write with backfill and verification, then flip) — chosen per module, not globally. Team and process shift too: the receiving organization needs Java platform maturity before core modules arrive — build tooling, JVM ops (memory, GC, profiling), Spring/Quarkus conventions ([[How do you implement caching in Spring]]-class standards), and hiring or training. Risk management runs the whole show: a capability map with per-module risk/value ranking sets the cutover order; every step has a defined rollback (route back, feature flags); and success metrics are declared up front (latency parity, error budgets, delivery speed). The anti-patterns to name: the big-bang rewrite with a moving legacy target (Fowler's cited caution — the old system keeps changing while you copy it), migrating because "Java is modern" rather than for named business outcomes, and letting the facade ossify into a second monolith. [[How do you design a system against vendor lock-in]]'s exit-plan discipline applies to the legacy side symmetrically.

> [!warning] The big-bang rewrite loses to a moving target
> While the rewrite chases the current feature set, the legacy system keeps changing — the gap grows, momentum dies, and the migration becomes the project that never shipped. Incremental strangling with per-module rollback is slower per step and faster in total, because every step ships.

> [!tip] Interview answer
> I migrate to Java strangler-style: an interposing facade routes per business capability, low-risk high-churn modules move first to prove the platform, core transactions last. Data strategy per module (facade reads, CDC sync, then cutover), outbox events keep stores coherent, and every route has instant rollback. No big-bang rewrite — the legacy target keeps moving, the incremental path keeps shipping.
