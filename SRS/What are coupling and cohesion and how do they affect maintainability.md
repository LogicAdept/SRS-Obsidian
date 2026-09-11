<!--
reps: 0
priority: 0
-->
#Methodologies/Principles #SystemDesign/Architecture #SRS

# What are coupling and cohesion and how do they affect maintainability

> [!abstract] Short answer
> Coupling is the degree to which modules depend on each other's internals — how much a change in one forces changes in others. Cohesion is how strongly a module's internals belong together — one responsibility versus a grab-bag. The design target is the classic pairing: low coupling, high cohesion. Maintainability follows directly: with low coupling you change one module without dragging others; with high cohesion you find everything about one concern in one place.

## The two axes

Coupling measures the cost of change across boundaries. Its ladder runs from data coupling (modules share only well-defined parameters) through control coupling (one dictates another's flow) to the worst — content/common coupling (direct access to another's internals or shared global state). Concrete modern markers: imports reaching into another package's internals, shared mutable state, temporal coupling (call order assumptions), and the tell-tale change amplification — one requirement, five files. Cohesion measures alignment inside a boundary: a module where every member serves one reason to change (a pricing module owns pricing rules, rates, surcharges) is highly cohesive; a `Utils` class holding string, date and crypto helpers is its anti-type — members united only by file location. Conway's law gives the organizational mirror: coupling between modules tends to match coupling between the teams that own them, which is why service boundaries are also ownership boundaries.

```text
high coupling, low cohesion (the mud):
  change pricing rule -> touches Order, UI, Report, EmailService...
  "Utils" grows; logic for one concern is scattered everywhere
low coupling, high cohesion (the target):
  change pricing rule -> PricingModule only; its members all serve pricing
maintainability = cost of change = f(coupling) ; findability = f(cohesion)
```

```d2
direction: right
mud: "mudball" {
  style.stroke: "#c62828"
  P: "pricing logic" {
    width: 150
    height: 45
  }
  O: "Order" {
    width: 100
    height: 40
  }
  U: "UI" {
    width: 80
    height: 40
  }
  R: "Report" {
    width: 100
    height: 40
  }
  E: "Email" {
    width: 100
    height: 40
  }
  O -> P
  P -> U
  P -> R
  E -> P
  O -> R
  U -> E
}
bound: "bounded" {
  style.stroke: "#2e7d32"
  C: "clients" {
    width: 110
    height: 45
  }
  PM: "PricingModule\n(high cohesion)" {
    width: 190
    height: 60
  }
  C -> PM: "narrow interface"
}
```

**Fig. 1.** Left: one concern scattered with tangled edges - a pricing change hits five files. Right: the concern owns its boundary and meets clients through one narrow interface.

**Listing 1.** The same change in a mudball versus a well-bounded design.

## How they shape maintainability

The maintainability effect is measurable, not aesthetic. Low coupling limits blast radius: bugs, refactorings and rewrites stay contained; tests need fewer doubles and less setup (no transitive dependency walls); modules can be reused, replaced or migrated independently ([[What is the difference between a stateful service and a stateless service]]-style swapability, or the vendor-exchange seams of [[How do you design a system against vendor lock-in]]). High cohesion makes the system searchable and safe to change: a contributor finds the whole concern in one place, and contradictory logic (two places implementing "the rule") has nowhere to hide. The metrics family backs the intuition — dependency fan-in/fan-out ([[What are afferent coupling and efferent coupling]] covers the directed pair), instability metrics, and cohesion measures like LCOM. The two axes trade against naive designs: duplicating logic lowers coupling but kills cohesion (the same rule in three places); a god-module is perfectly cohesive by accident (everything in one place) with catastrophic internal coupling — the target is the pairing, per boundary: modules that own one concern completely and touch neighbors only through narrow, stable interfaces ([[What is layered architecture]] applies the pairing at the layer scale; microservices at the system scale).

> [!warning] Duplication is not decoupling
> Copying logic into two modules removes a dependency and creates a worse problem: two copies drifting apart — every future fix must find both. Decouple through a shared, well-owned abstraction or accept the dependency; do not launder coupling into duplication.

> [!tip] Interview answer
> Coupling is inter-module dependence — how far a change propagates; cohesion is intra-module alignment — whether one module owns one concern. Maintainability wants low coupling (contained blast radius, testable modules) and high cohesion (findable, non-contradictory logic). The trap is calling duplication decoupling — copies drift; the real answer is narrow stable interfaces and clear ownership.
