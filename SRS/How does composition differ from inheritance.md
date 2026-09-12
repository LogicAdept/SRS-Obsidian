<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Inheritance #SRS

# How does composition differ from inheritance

> [!abstract] Short answer
> **Inheritance** builds a class *on top of* another: `Sedan extends Vehicle` — the subclass **is-a** Vehicle, inherits its members, and is substitutable wherever the supertype is expected. **Composition** builds a class *out of* others: `Car` holds an `Engine` **field** — the whole **has-a** part and reaches behavior by **delegation**, not by inheritance. Mechanically: inheritance copies the supertype's API into your type and wires in **dynamic dispatch**; composition gives you a private reference and nothing else — every exposed behavior is an explicit method call to the part ([[What do in OOP expressions is-a and has-a]]). The GoF rule — favor composition over class inheritance — lives in [[Why is composition often recommended over inheritance]]; the decision procedure in [[Where should you prefer inheritance versus aggregation]].

## What each one actually gives you

`extends` does three things at once. First, **API inheritance**: every accessible member of the superclass is now part of your class — `Sedan` answers `describe()` without writing it. Second, **substitutability**: a `Sedan` reference may be used where a `Vehicle` is declared, enabling subtype polymorphism ([[What is polymorphism]]). Third, **dispatch**: overridden methods are chosen by the run-time class ([[What is the difference between static and dynamic binding in Java]]). The price: Java allows **one** superclass, and your class is statically coupled to that parent's implementation — the fragile-base-class risk ([[How would you explain class inheritance in Java and tradeoffs]]). The fragility mechanics: [[What is the fragile base class problem]].

Composition does none of that automatically. `Car` declares `private final Engine engine` and forwards `start()` to it. There is **no API inheritance** — `Car` does not become an `Engine` and does not get its members. There is **no substitutability** through the field — substitutability only appears if you compose *behind an interface* ([[Why are interfaces important in object oriented design]]). What you buy in exchange: the part can be **swapped at run time**, the part can come from anywhere (injected, shared, pooled), and the whole's API is *chosen*, not inherited — no accidental exposure of 40 superclass methods ([[What are alternatives to class inheritance]]).

```java
class Vehicle {
    String describe() { return "vehicle with " + wheels() + " wheels"; }
    int wheels() { return 4; }
}

class Sedan extends Vehicle {              // is-a
    @Override int wheels() { return 4; }
}

class Engine {
    String start() { return "engine ignition sequence"; }
}

class Car {                                 // has-a
    private final Engine engine = new Engine();   // owned part, created inside

    String start() { return "Car -> " + engine.start(); }   // delegation
}
```

**Listing 1.** Both constructions in one program. `Sedan` inherits `describe()` and overrides `wheels()`; `Car` owns an `Engine` and exposes only `start()`.

```text
vehicle with 4 wheels
Car -> engine ignition sequence
v is a Sedan: true
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_1`): the inherited call works without `Sedan` implementing it, the delegation call carries behavior from the part, and a `Sedan` substitutes as `Vehicle` — that last line is what composition alone does not give.

## How to answer "which one here"

- **True invariants + same contract?** Inheritance is honest: the subclass *is* the supertype, with something added or varied ([[What is inheritance]]).
- **Reusing behavior?** Compose: hold a part and delegate. Inheritance-for-reuse couples you to implementation you did not design ([[Where should you prefer inheritance versus aggregation]]).
- **Need run-time flexibility?** Composition behind an interface — strategy, plugin, testing seam.
- **Both:** they are not enemies — a class can extend one type and compose many parts; Java's single-`extends` budget is exactly why delegation is everywhere in real APIs.

> [!warning] "Inheritance is reuse, composition is reuse — pick any" is the trap
> They reuse different things. Inheritance reuses *implementation and type identity* and locks both in at compile time; composition reuses *behavior through a contract* and stays swappable. Saying they are interchangeable fails the follow-up "then why does `private` matter?" — a subclass can depend on superclass internals a composite never sees ([[How would you explain the Liskov substitution principle in SOLID]]).

> [!warning] Delegation is not free
> Composition means writing forwarding methods for everything you expose. A class forwarding 30 methods to its part is a smell in the *other* direction — you may want inheritance, or a smaller API. Also: delegation through a field of a *mutable shared* part leaks state between wholes — ownership rules decide whether you are composing or aggregating ([[What is the difference between composition and aggregation]]).

```d2
direction: right
inh: {
  label: "inheritance"
  v: "Vehicle" { width: 130; height: 34 }
  s: "Sedan" { width: 130; height: 34; style.fill: "#e3f2fd" }
  v -> s: "extends\ninherits API + dispatch"
}
comp: {
  label: "composition"
  c: "Car" { width: 130; height: 34 }
  e: "Engine" { width: 130; height: 34; style.fill: "#fff8e1" }
  c -> e: "field + delegate"
}
inh -> comp: "is-a vs has-a"
```

**Fig. 1.** Inheritance makes the child a subtype wired into dispatch; composition makes the whole a client of the part.

> [!tip] Interview answer
> Inheritance means is-a: the subclass extends one superclass, inherits its members, and is substitutable through the supertype, with overridden methods chosen at run time. Composition means has-a: the whole keeps a reference to a part and delegates, so behavior comes from an object it owns rather than from code it inherits. Inheritance reuses implementation and type identity but couples you to one parent forever; composition reuses behavior behind a contract and stays swappable. I use inheritance for genuine stable is-a with substitutability, and composition for reuse and flexibility — the GoF rule favors composition over class inheritance.
