<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is supple design in DDD?

> [!abstract] Short answer
> Supple design is the set of code-level traits that let a domain model absorb change: intention-revealing interfaces that state outcomes instead of mechanics, side-effect-free functions that answer without mutating, explicit assertions about preconditions and postconditions, a conceptual contour that follows the domain's joints, standalone classes, and closure of operations. It is the craft layer that makes the tactical patterns pleasant to work with after month six.

## The six elements

Intention-revealing interface: method names say what the outcome is - `order.cancel(now)` - not what steps they perform (`setStatus`, `recalc`). The caller reads the model like the business, and the ubiquitous language reaches the method signature. Side-effect-free functions: queries compute and return new values without touching state, so they can be called anywhere in any order - the `total()` of an order is provably non-mutating. Assertions: preconditions, postconditions, and invariants stated (and checked) on the object - "cancel is legal only while the window is open" lives in the cancel method, not in the caller's memory. Conceptual contour: modules and types split where the domain splits, so a pricing change touches pricing code only. Standalone classes: a class usable without dragging in half the graph, which keeps tests and reasoning cheap. Closure of operations: operations typed over their own domain - `Money.plus(Money): Money` - so arithmetic stays inside the concept instead of leaking primitives everywhere.

```java
record Money(long cents, String currency) {
    Money plus(Money other) {                       // closure of operations
        if (!currency.equals(other.currency)) throw new IllegalArgumentException("currency mismatch");
        return new Money(cents + other.cents, currency);   // side-effect-free
    }
}

void cancel(long nowMin) {                          // intention-revealing name
    if (nowMin - createdAtMin > CANCEL_DEADLINE_MIN)    // assertion: window
        throw new IllegalStateException("cancel window closed");
    if (!"OPEN".equals(status))                         // assertion: state
        throw new IllegalStateException("cannot cancel from " + status);
    status = "CANCELLED";
}
Money total() { return lines.stream().reduce(new Money(0, "EUR"), Money::plus); }
```

**Listing 1.** Verified on JDK 21.0.12.1: calling `total()` twice around an `add` shows the earlier snapshot unchanged (3500 stays 3500 while the live total becomes 3501) - the query is side-effect-free; cancel outside the window throws with the assertion message, not a corrupted state.

```d2
direction: right
iri: "Intention-revealing\ninterface" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
sef: "Side-effect-free\nfunctions" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
asserts: "Assertions\npre/post/invariant" {
  width: 210
  height: 70
  style.fill: "#fff3e0"
}
contour: "Conceptual contour\nmodules follow the domain" {
  width: 250
  height: 80
  style.fill: "#f3e5f5"
}
standalone: "Standalone\nclasses" {
  width: 190
  height: 70
  style.fill: "#ffebee"
}
closure: "Closure of\noperations" {
  width: 190
  height: 70
  style.fill: "#e1f5fe"
}
iri -> contour
sef -> contour
asserts -> contour
contour -> standalone
contour -> closure
```

**Fig. 1.** The six traits reinforce one another: names state intent, functions stay pure, assertions guard transitions, and the module contour keeps each change local.

## Why it matters

Supple design is what the model feels like in month six, not day one. A model that is "correct" but awkward - setters everywhere, queries with hidden mutations, rules spread across callers - gets worked around, and the workarounds fork the language. Each trait buys a specific freedom: pure functions make aggregation and parallelism safe; assertions turn late-night production bugs into early test failures; standalone classes keep the cost of the next change proportional to its size. The habits connect directly to older craft rules: telling over asking and limiting knowledge of neighbors ([[What is the Law of Demeter]]) are the behavioral face of the same discipline - and they are what keeps an entity rich instead of sliding into anemia ([[What is an anemic domain model and is it useful]]). The strategic side gets its own vocabulary in [[What is a domain model]]; supple design is the tactical promise that the model stays cheap to reshape.

> [!warning] Not a naming exercise
> Renaming `setStatus` to `cancel` without moving the window and state checks into the method is theater: the assertion still lives in the caller, so the next caller forgets it. Supple design is where the checks live, not what the words say. The corollary: it cannot be bolted on by a decorator layer - it is written into the objects themselves, or it is not there.

> [!tip] Interview answer
> Supple design is DDD's code-quality bar: intention-revealing interfaces, side-effect-free queries, assertions that guard state changes, modules contoured to the domain, standalone classes, and closure of operations. Together they keep a model cheap to change - behavior is discoverable from names, queries cannot corrupt state, and invalid transitions fail loudly at the object that owns them.

