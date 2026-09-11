<!--
reps: 0
priority: 0
-->
#Methodologies/Principles #SRS

# Which principles help you write clean maintainable code?

> [!abstract] Short answer
> A working core set: single responsibility - one actor, one reason to change per module; DRY - every fact has one authoritative representation; KISS and YAGNI - simplest thing that works, nothing speculative; encapsulation - invariants enforced behind small contracts; loose coupling with high cohesion - modules relate through interfaces and change together only when the business does; composition over inheritance; command-query separation for readable state handling; and the Law of Demeter for local knowledge. None of them is a law - the craft is applying the one that answers the pain in front of you.

## The core set and what each one buys

Maintenance is the cost of change, so the principles that pay are the ones that localize change. SRP keeps a module's changes driven by one stakeholder; DRY keeps a fact from disagreeing with itself across the codebase; KISS and YAGNI keep the surface small enough that fewer things can break ([[What is DRY, KISS, YAGNI]]). Encapsulation plus command-query separation make state reasoning cheap: legal states enforced at one door, queries repeatable without side effects ([[What is encapsulation]], [[What is CQS and how does it relate to CQRS]]). Composition over inheritance keeps reuse flexible and avoids fragile base classes; loose coupling keeps a change from rippling across modules ([[How would you explain tight versus loose coupling between software modules]], [[What are coupling and cohesion and how do they affect maintainability]]). The Law of Demeter adds the local rule: talk to collaborators, not to collaborators' collaborators - so chains like `a.getB().getC().doX()` stop hiding the real dependency structure.

```d2
direction: right
local: "Local clarity\nKISS, YAGNI, DRY, CQS" {
  width: 270
  height: 85
  style.fill: "#e3f2fd"
}
struct: "Structure\nSRP, encapsulation,\nlow coupling" {
  width: 270
  height: 85
  style.fill: "#fff3e0"
}
evo: "Evolution\ncomposition over inheritance,\nLaw of Demeter" {
  width: 280
  height: 85
  style.fill: "#e8f5e9"
}
local -> struct -> evo: "code stays changeable"
```

**Fig. 1.** The set at three altitudes: how one piece reads, how pieces connect, and how the whole thing is allowed to evolve.

## Judgment over catalog

Two meta-rules make the set work in practice. First, principles are diagnostics for pain, not pre-commitment: extract the abstraction when the duplication hurts, add the interface when the second implementation arrives - and refuse speculative ceremony ([[What is overengineering and how does it affect enterprise software]]). Second, they trade off against each other, and saying WHICH trade you chose is the senior move: DRY against KISS when a "shared" abstraction needs six flags; strict CQS against a natural `pop()`-style API; decoupling against indirection cost. Refactoring is the mechanism that keeps applying them incrementally as evidence accumulates ([[What is refactoring]]).

> [!warning] "Clean code = followed all the principles" is how systems get polite and unmaintainable
> A codebase can satisfy every named rule and still resist every change - if the abstractions cut across the domain, if the layers are ceremony, if names lie. The principles are descriptive tools distilled from designs that survived change; they cannot substitute for knowing the domain and reading the actual change history. And their set is not closed: testability, observability, and API stability are maintenance principles too, with equal standing ([[What can violating SOLID principles lead to]]).

> [!tip] Interview answer
> My working set: SRP, DRY, KISS, YAGNI, encapsulation with command-query separation, low coupling and high cohesion, composition over inheritance, and the Law of Demeter. I apply them as responses to real pain rather than as pre-armed ceremony, because dogma produces its own rot. The through-line is one idea: localize change - a principle that does not make the next change cheaper is decoration.
