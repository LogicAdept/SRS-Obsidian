<!--
reps: 0
priority: 0
-->
#Methodologies/Principles #SRS

# Why is composition often recommended over inheritance?

> [!abstract] Short answer
> Because inheritance couples a class to its superclass's implementation details, while composition couples it only to a contract. GoF's Design Patterns states it as a principle - "favor object composition over class inheritance" - for two reasons: composition is black-box reuse (you delegate to an interface and cannot break internals), and it is dynamic (you can swap collaborators at runtime, per test, per configuration). Inheritance is white-box, static, and single-parent in Java; its famous costs - the fragile base class problem and forced knowledge of parent internals - are exactly the costs composition avoids.

## The two reuses, mechanically

Inheritance reuses by EXPANSION: the subclass compiles against the parent's protected fields, overridable methods, and undocumented call patterns between them. That knowledge is the coupling: when the superclass changes its internals in a later release, subclasses break without any signature changing - the fragile base class problem. It also hard-codes the choice at compile time: `class Report extends PdfExporter` cannot become an Excel exporter at runtime. Composition reuses by DELEGATION: hold a reference to an interface, forward calls, and the implementation - and the strategy - is a swappable detail. The composed object knows only the contract, so implementation churn behind it is invisible ([[How does composition differ from inheritance]]).

```d2
direction: right
inh: "Inheritance" {
  width: 220
  height: 75
  style.fill: "#fde8e8"
}
inh1: "static, one parent\nsees internals" {
  width: 230
  height: 70
}
comp: "Composition" {
  width: 220
  height: 75
  style.fill: "#e8f5e9"
}
comp1: "runtime-swappable\ncontract only" {
  width: 230
  height: 70
}
inh -> inh1
comp -> comp1
```

**Fig. 1.** The trade in one line each: inheritance buys convenience at compile time and charges coupling to internals; composition buys freedom at runtime for a little delegation boilerplate.

## The concrete failure modes composition avoids

Three keep recurring in real systems. Fragile base class: the parent's internal refactoring (reordering `this.update()` calls, caching a computed value) breaks subclass assumptions invisibly. Rigid taxonomies: `PdfReport extends Report`, `ExcelReport extends Report`, then "export both ways" or "report with charts" forces diamond-shaped hierarchies - while composition just takes two collaborators ([[Does Java support multiple inheritance for classes]]). Testing drag: an extending class cannot be tested without dragging the superclass along; a composed collaborator is a mock in one line ([[What are alternatives to class inheritance]]). This is why dependency injection and test-friendly design are, structurally, arguments FOR composition - the object under test takes its collaborators in ([[How would you explain dependency injection]]).

> [!warning] "Composition over inheritance" is a preference, not a ban
> The principle loses its edge where inheritance is the designed mechanism: abstract skeletons with documented extension hooks (`AbstractList`-style template methods), sealed hierarchies the author controls, genuine substitutable types consumed polymorphically - there, extends IS the contract and delegation would just re-type it. The other lie is composition maximalism: a class with fifteen injected strategy objects and one-line delegation everywhere has traded readable coupling for unreadable indirection. Both tools shape reuse; the choosing rule is coupling to internals (inherit) versus coupling to contract (compose) ([[How would you explain class inheritance in Java and tradeoffs]]).

> [!tip] Interview answer
> Composition wins because it reuses through a contract instead of through implementation: no fragile base class exposure, swappable behavior at runtime, trivial mocking, and no single-parent ceiling - which is why GoF framed it as the default. I still use inheritance where it was designed for - skeleton classes and sealed variants - but for plain behavior reuse I delegate. The honest summary: inherit for type, compose for capability.
