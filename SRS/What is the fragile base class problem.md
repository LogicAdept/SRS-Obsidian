<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Inheritance #SRS

# What is the fragile base class problem?

> [!abstract] Short answer
> Inheritance couples subclasses to the base's **implementation**, not just its contract: which methods call which, in what order, on what state. Two directions break. **Base evolves**: a release that reshuffles internal call paths or adds methods silently changes or clashes with subclasses. **Subclass is written**: a base constructor that calls an overridable runs subclass code on a half-built object ([[What is inheritance]]). The sandbox shows the constructor case: the override reads a subclass field still holding its default value.

## Why it exists: white-box reuse

When `Sub extends Base`, `Sub` may rely on *how* `Base` works — that `putAll` loops over `put`, that the constructor initializes fields in some order, that a helper is not overridden anywhere. That knowledge is nowhere in the type system; it lives in base internals. Any base release that reorganizes internals can break untouched subclasses — the code never changed, its meaning did ([[What is the difference between subtyping and inheritance]]). This is why the problem is called *fragile base class*: the base is the load-bearing wall nobody may touch.

## The constructor trap, mechanically

Java builds objects from the root up: `super()` runs before subclass field initializers. If the base constructor calls an overridable method, the **override** runs — with subclass fields still at defaults. The sandbox run prints `count = 0` although the initializer says `50`: dynamic dispatch reached into a not-yet-built object. The same pattern — base code invoking overridables — bites in any base method, not just constructors.

## Both directions, real cases

Base-side evolution: `java.util.Properties extends Hashtable` bakes in table mechanics; adding a default method or reshaping an internal loop ripples into it. Subclass-side: `Stack extends Vector` depends on Vector's storage decisions forever. JDK folklore (Effective Java item 19) turns this into design guidance: **design for extension or prohibit it** — document which methods are overridable and how they self-call, keep constructors calling only `private`, `final`, or `static` methods, and otherwise prefer composition ([[How does composition differ from inheritance]]; [[What are alternatives to class inheritance]]).

```d2
direction: down
sup: "Sub() {\n  1. super() runs FIRST\n  2. field initializers" {
  width: 260
  height: 80
  style.fill: "#fff8e1"
}
base: "Base() {\n  init();   <- overridable call" {
  width: 260
  height: 64
  style.fill: "#ffebee"
}
sub: "Sub.init()\ncount == 0 (default)" {
  width: 240
  height: 60
  style.fill: "#ffebee"
}
sup -> base
base -> sub: "dynamic dispatch on half-built object"
```

**Fig. 1.** Construction order plus dynamic dispatch equals an override running before the subclass fields exist.

```java
class Base {
    Base() { init(); }                       // FRAGILE: constructor calls an overridable
    void init() { System.out.println("Base.init"); }
}
class Sub extends Base {
    private int count = 50;                  // initialized AFTER super()
    @Override void init() { System.out.println("Sub.init sees count = " + count); }
}
```

**Listing 1.** The minimal trap: base constructor dispatches into subclass code.

```text
Sub.init sees count = 0
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_10`): the override observes `count = 0`, not `50` — the field initializer has not run when `super()` calls it.

> [!warning] "Fragile base class is about performance" is false
> It is **semantic coupling**, not memory or speed: correct-looking code breaks because the base's *implementation* contract shifted — a constructor self-call, a renamed internal helper, a reshaped loop — none of which any compiler can see. The defense is design discipline: freeze or document self-use, or drop inheritance for composition ([[How would you explain the Liskov substitution principle in SOLID]]).

> [!tip] Interview answer
> Inheritance makes subclasses depend on base internals: which method calls which and in what order. It bites in both directions — a base constructor calling an overridable runs subclass code before subclass fields exist, and a base release reshuffling its internal calls can break untouched subclasses. I design bases for extension explicitly — document self-use, keep constructors off overridables — or I compose instead.
