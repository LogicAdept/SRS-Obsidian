<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Encapsulation #SRS

# How would you explain encapsulation in object oriented design

> [!abstract] Short answer
> At the design level, **encapsulation is a module boundary**: a class is a small unit that **owns its state and the rules over that state (invariants)**, and publishes a narrow API so that *every* change to the state goes through code that can enforce the rules. The point is not secrecy but **change locality and correctness** — the implementation can be rewritten, cached, synchronized, or persisted without any client noticing, because nothing outside can bypass the methods ([[What is encapsulation]]). It is the enforcing half of abstraction: abstraction decides *what* the boundary offers, encapsulation makes the boundary *impossible to bypass* ([[What is the difference between abstraction and encapsulation]]).

## Why designers care: invariants and local change

The design value rests on two arguments. **Invariants.** An object like a bank account or a connection pool is only correct while certain conditions hold (balance never negative, pool never exceeds its limit). If the state is private and every mutation goes through methods, the invariant is checked at a handful of well-known points — inside the class. If even one field is public, the invariant lives *everywhere in the program that touched the field*, and no class can guarantee it anymore ([[How would you explain problems with public mutable fields in Java]]). **Continuity under change.** The classic maintenance argument: a system stays maintainable when a change touches a *module boundary* instead of rippling across the code base. Encapsulated classes localize change — you can swap the storage of a cache from `HashMap` to something LRU-based while its public API stays untouched. That is exactly the modularity property Meyer's construction method optimizes for: designs where a change in one part does not force changes in others.

```java
interface Thermometer {                    // the published boundary
    double reading();
    void warmBy(double delta);
}

class CelsiusThermometer implements Thermometer {
    private double celsius;                        // no client can touch this
    CelsiusThermometer(double c) { setCelsius(c); }
    void setCelsius(double c) {
        if (c < -273.15) throw new IllegalArgumentException("below absolute zero");
        this.celsius = c;
    }
    public double reading() { return celsius; }
    public void warmBy(double delta) { setCelsius(this.celsius + delta); }
    public String toString() { return celsius + " C"; }
}
```

**Listing 1.** The invariant "temperature is above absolute zero" is enforced in exactly one place. Every mutation — constructor, `warmBy`, direct setter — funnels through the guard.

```text
25.0 C
invariant guarded: below absolute zero
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_7`): legitimate mutation works, the illegal one is rejected at the boundary instead of corrupting the object.

## The boundary is more than `private`

Treating encapsulation as "make fields private" understates the design content. The boundary also decides **what the class does not reveal**: implementation types (return `List`, not `ArrayList`), internal helper methods, mutable internal collections (hand out unmodifiable views or copies), and mutable references that would let callers escape the API entirely. It scales upward too: packages, modules, and services are encapsulation units with the same logic — an internal method of a service is "private" at system scale. And it has an honest limit: encapsulation guards *this* object's state; it does not make shared mutable state safe by itself, which is why concurrent designs still need synchronization or immutability on top ([[What are the advantages and disadvantages of object oriented programming]]).

> [!warning] Getters and setters are not encapsulation
> A class with private fields where every field has a `get`/`set` pair has a boundary in name only: the API still exposes raw state, so invariants cannot hold. Encapsulation asks the opposite question — *what operations does this object offer?* — and state access falls out of those operations. A data class legitimately reduced to getters/setters is a record or a DTO, and it should be honest about having no behavior ([[How would you explain problems with public mutable fields in Java]]).

> [!warning] Deep encapsulation leaks are real
> `this.field = other.mutableList` or returning the internal list hands the invariant to strangers. The classic bugs are aliasing leaks — a caller stores the returned collection and mutates it later. The design rule: anything crossing the boundary is either immutable, a copy, or an unmodifiable view ([[What is the difference between shallow and deep copying in Java]]).

```d2
direction: down
client: "clients" { width: 170; height: 34 }
api: "published API: reading(), warmBy()" { width: 300; height: 40; style.fill: "#e3f2fd" }
state: "private state + invariant guard" { width: 320; height: 40; style.fill: "#e8f5e9" }
client -> api: "only calls"
api -> state: "funnels through"
```

**Fig. 1.** Everything outside the class sees only the API line; all paths to state pass through the guard.

> [!tip] Interview answer
> Encapsulation at the design level means every object is a module that owns its state and enforces its own invariants: state is private, the API is the only way in, so the rules are checked in one place and the implementation can change without touching clients. The benefit is correctness — illegal states get rejected at the boundary — and change locality, because callers depend on operations, not on storage. It is more than private fields: exposing raw getters and setters or leaking internal collections breaks the boundary again. Abstraction decides what the boundary offers; encapsulation makes the boundary hold.
