<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Canonical Data Model pattern?

> [!abstract] Short answer
> A **Canonical Data Model** is a **single, application-independent message format** that every integrating application translates to and from, instead of translating pairwise between each other's proprietary formats — one shared contract instead of N times (N minus 1) dialects.

## Indirection that pays for itself at the fourth system

Each application has its own internal data format, and direct pairwise translation seems cheaper at first: two applications need two translators, the canonical approach needs four. The crossover comes fast — three applications need six translators either way, and six applications need **thirty** pairwise translators versus twelve canonical ones. The canonical model is an extra level of indirection: each application produces and consumes one agreed format, and a new system joining the integration only builds its own pair of translators, independent of how many systems already participate. The model is not free to design: it needs governance so it does not become either the union of every system's fields or the lowest common denominator; formats usually ride with a [[What is the Format Indicator pattern]] for evolution, and each boundary conversion is a [[What is the Message Translator pattern]]. When heterogeneous inputs must be funneled into the model at the edge, the [[What is the Normalizer pattern]] is the standard composition.

```d2
direction: down
a: "CRM" {
  width: 120
  height: 50
  style.fill: "#e3f2fd"
}
b: "Accounting" {
  width: 140
  height: 50
  style.fill: "#e3f2fd"
}
c: "Inventory" {
  width: 130
  height: 50
  style.fill: "#e3f2fd"
}
d: "Partner feed" {
  width: 150
  height: 50
  style.fill: "#e3f2fd"
}
canon: "Canonical Data Model\none shared format" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
a -> canon
b -> canon
c -> canon
d -> canon```

**Fig. 1.** Translators pair every system with the model, not with each other: N systems need 2N translators, not N(N-1).

## Translator arithmetic

```text
Systems   Pairwise translators   Canonical translators
-------   --------------------  ---------------------
2         2                     4
3         6                     6
4         12                    8
6         30 (!)                12
```

**Listing 1.** The indirection tax at two systems becomes the decisive saving from four systems upward.

> [!warning] The canonical model needs an owner, or it becomes a battlefield
> With no governance, every team adds "just one field" and the model bloats into the union of all schemas; with too much discipline it starves into a lowest-common-denominator blob of optional strings. Version it, assign ownership, and evolve it with the same rigor as a public API — it is one.

> [!tip] Interview answer
> A Canonical Data Model is one application-independent message format that all integrating systems translate to and from. Pairwise translation costs N times N minus one translators and explodes with scale, while the canonical model costs two per system and isolates each newcomer's integration effort. It wins from roughly four systems on, and it needs real governance and versioning to stay healthy.
