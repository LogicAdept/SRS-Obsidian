<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Methodologies/Principles #SRS

# What does behavioral subtyping require beyond matching signatures?

> [!abstract] Short answer
> Liskov and Wing's formal answer (TOPLAS 1994) has two rules. The **signature rule** — compatible signatures — and the **methods rule**: a subtype may **weaken preconditions** and **strengthen postconditions**, never the reverse; it must **preserve the base's invariants**; and it must satisfy the **history constraint**: no new observable way to change state that the base treated as immutable. The compiler checks only the signature rule — the rest is design discipline ([[How would you explain the Liskov substitution principle in SOLID]]).

## The signature rule, Java's slice

Java enforces a narrow version mechanically: an override needs a subsignature, a return type that is the same or **covariant** ([[Can you declare a narrower return type when overriding a method]]), cannot add checked exceptions, and cannot weaken access ([[Can you use a weaker access modifier when overriding a method]]). Note that Java is *stricter* than the theory here: Liskov–Wing ask for **contravariant** argument types (a subtype accepting a broader argument), while Java fixes parameter types exactly — the variance corner is covered in [[How would you explain covariance of generic and return types in Java]].

## The methods rule: weaken pre, strengthen post

The behavioral core is an ordering on contracts. Accepting a **superset** of the base's inputs is safe: every client that satisfied the base precondition still satisfies yours. Promising a **superset** of outputs is safe: no client depends on less than you now give. The other direction — demanding narrower inputs or delivering weaker guarantees — lets a base-contract client crash on a perfectly legal call. That boundary is mechanically visible in the sandbox run below ([[How would you explain programming by contract and preconditions]]).

## Invariants and the history constraint

Two further clauses protect state. The subtype must preserve every **invariant** the base established — a `Fraction` subtype cannot permit `den = 0` ([[What is a representation invariant and abstraction function]]). The **history constraint** is subtler: a subtype may not *introduce* mutability the base never had. If `Point` exposes only getters, a `MutablePoint extends Point` with `setX` violates subtyping even though every signature matches: through the base's eyes, the object changed by itself. This is the clause behind the immutable-first advice for value types and behind `List.of` returning a fixed-size list whose contract *declares* mutability unsupported rather than silently refusing it.

```d2
direction: down
base: "Base contract\npre: 0..100   post: stored" {
  width: 300
  height: 64
  style.fill: "#e3f2fd"
}
rules: "subtype allowed\npre weaker (accept more)\npost stronger (promise more)\ninvariants hold   history fixed" {
  width: 320
  height: 96
  style.fill: "#fff8e1"
}
sub: "Subtype\nbreaks client" {
  width: 220
  height: 52
  style.fill: "#ffebee"
}
base -> rules: "legal directions"
rules -> sub: "pre 0..10 = DEMANDS MORE"
```

**Fig. 1.** The methods rule as arrows: only the "accept more / promise more" directions keep base-contract clients alive.

```java
class Bounded {
    int last;
    void put(int v) {                          // base contract: accepts 0..100
        if (v < 0 || v > 100) throw new IllegalArgumentException("base pre: 0..100");
        this.last = v;
    }
}
class Tighter extends Bounded {
    @Override void put(int v) {                // strengthened precondition: 0..10 — ILLEGAL direction
        if (v < 0 || v > 10) throw new IllegalArgumentException("tighter pre: 0..10");
        super.put(v);
    }
}
```

**Listing 1.** The violating direction. `Tighter` demands more than `Bounded` promised.

```text
Tighter broke client: put(60) -> tighter pre: 0..10
Wider accepted -100: legal weakening, last=-100
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_16`): a base-typed client crashes on `put(60)`, which the base contract allows; the precondition-weakening subtype accepts `-100` legally.

> [!warning] "The compiler enforces LSP" is false
> The compiler checks the signature rule only. Preconditions, postconditions, invariants, and the history constraint are invisible to `javac` — `Tighter.put` compiles cleanly and detonates at run time. Contracts must be documented and reviewed ([[Why are clear behavioral contracts important in Java APIs]]), and a subclass needing *extra* input checks is a hierarchy smell, not a robustness win ([[What is defensive programming and how does it differ from design by contract]]).

> [!tip] Interview answer
> Beyond signatures, behavioral subtyping means: never demand more from callers than the base did, never promise less, preserve the base's invariants, and don't invent new ways to mutate state the base treated as fixed. The compiler can't see any of it — `Tighter.put` restricting 0..100 to 0..10 compiles fine and breaks base-contract clients. When I see a subclass adding extra input restrictions, I treat it as a substitution bug, not hardening.
