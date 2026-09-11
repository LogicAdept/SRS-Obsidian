<!--
reps: 0
priority: 0
-->
#Methodologies/Principles #SystemDesign/Architecture #SRS

# What are afferent coupling and efferent coupling

> [!abstract] Short answer
> Afferent coupling (Ca) is the number of components that depend ON a given component — incoming dependencies, its fan-in. Efferent coupling (Ce) is the number of components a given component depends on — outgoing dependencies, its fan-out. They are the directed pair behind stability analysis: a component with high afferent coupling is stable (many depend on it — change it carefully), one with high efferent coupling is sensitive (it breaks when many others change).

## The definitions and what each implies

Afferent: how many clients call this module? High Ca means many consumers — the module is a hub. Implication: it is stable by necessity (changing its interface breaks many) and therefore must change slowly, version deliberately, and be tested exhaustively; it is also a reuse asset — the shared library everyone wants. Efferent: how many modules does this one call? High Ce means the module aggregates many concerns or sits at an integration point. Implication: it is sensitive (any upstream change can break it), hard to test in isolation (many doubles needed), and a candidate for decomposition. The classic pathology pair: a god-module with high Ce and high Ca (depends on everything, everything depends on it — change amplification in both directions), and utility-library churn with high Ca but changing internals (every release ripples). Dependency cycles are the structural bug this pair exposes: in a cycle, every component's Ca and Ce inflate together and no component can change in isolation.

```text
Ca = # of components depending on ME    (fan-in)  -> stability
Ce = # of components I depend on        (fan-out) -> sensitivity
hub:      high Ca, low Ce  (core domain lib)     -> change slowly
wrapper:  low Ca, high Ce  (integration facade)  -> isolate, absorb churn
mudball:  high Ca AND high Ce                    -> decompose
instability I = Ce / (Ca + Ce)  (0 = maximally stable, 1 = maximally unstable)
```

```d2
direction: right
core: "Domain core\nCa = 4, Ce = 0\nstability hub" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
c1: "API layer" {
  width: 130
  height: 45
}
c2: "Batch jobs" {
  width: 140
  height: 45
}
c3: "Web app" {
  width: 120
  height: 45
}
c4: "CLI tools" {
  width: 120
  height: 45
}
c1 -> core: "depends on"
c2 -> core: "depends on"
c3 -> core: "depends on"
c4 -> core: "depends on"
wrap: "Vendor wrapper\nCa = 0, Ce = 3\nchurn absorber" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
v1: "Vendor SDK" {
  width: 140
  height: 45
}
v2: "Vendor API" {
  width: 140
  height: 45
}
v3: "Legacy SOAP" {
  width: 150
  height: 45
}
wrap -> v1: "calls"
wrap -> v2: "calls"
wrap -> v3: "calls"
```

**Fig. 1.** The two healthy profiles: many-in/none-out (stable hub) and none-in/many-out (integration wrapper). A module with both counts high is the decomposition target.

**Listing 1.** The pair, its meanings, and the derived instability metric.

## Using them in design

The pair drives three practices. Layering enforcement: dependencies should point one way — high-level policy toward low-level detail — so Ca/Ce profiles per layer are checkable ([[What is layered architecture]]'s downward-only rule is exactly a Ce constraint per tier). Stability assignments: put the most stable (high-Ca) logic at the center — domain rules — and let volatile integration (external APIs, vendor SDKs — the seams of [[How do you design a system against vendor lock-in]]) live in low-Ca, high-Ce wrappers whose churn is absorbed in one place; the instability metric I = Ce/(Ca+Ce) makes the assignment measurable. Decomposition targeting: fan-out explosions after a feature (one class now importing fifteen services) mark the module to split, and the cohesion lens ([[What are coupling and cohesion and how do they affect maintainability]]) says along which lines. Tools expose both per package/type (dependency-matrix and cycle reports), so the review question "did this change raise Ce on a hub?" is answerable mechanically — and in microservice landscapes the same analysis maps to service-to-service call graphs, where hub services need the protection patterns ([[How do you protect a slower downstream service from overload]]) precisely because their Ca is the whole system.

> [!warning] Fan-in makes a module load-bearing, not disposable
> The module everyone depends on cannot be casually refactored, renamed or deleted — its high afferent coupling is a contract. Treat hubs as versioned products: deprecate, dual-publish, migrate consumers — or the next "simple change" becomes an ecosystem-wide incident.

> [!tip] Interview answer
> Afferent coupling counts incoming dependencies — how many depend on me — and marks stability; efferent counts outgoing — how much I depend on — and marks sensitivity. Design puts stable domain logic at high-Ca hubs, isolates volatile integrations in high-Ce wrappers, checks I = Ce/(Ca+Ce), and hunts cycles. A hub with both high is the decomposition target.
