<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Inheritance #SRS

# What is the difference between subtyping and inheritance?

> [!abstract] Short answer
> **Subtyping** is a **type relation**: `S` is a subtype of `T` when an `S` value may appear wherever a `T` is expected — the substitution license whose behavioral form the Liskov principle constrains ([[How would you explain the Liskov substitution principle in SOLID]]). **Inheritance** is a **code-reuse mechanism**: a class receives member implementations from a parent it can reuse or override ([[What is inheritance]]). Java fuses both in one keyword `extends`, which is why they get conflated — but they are orthogonal, and Cook's slogan **"inheritance is not subtyping"** marks exactly that.

## Two relations, one keyword

Subtyping lives in the **type lattice**: it decides which assignments and calls compile (`T t = s;`, passing `s` where `t` is expected) and which dispatch targets exist. Inheritance lives in the **class body**: it decides which members exist without being re-typed. A language can have either without the other: C++ **private inheritance** reuses code while producing *no* subtype relation usable by clients; Go's interfaces type **structurally** with zero inheritance at all. Java chose the fused design: `extends` draws the is-a edge *and* reuses the code; `implements` draws the type edge with no state reuse and only optional default-method reuse.

## Reuse without substitutability

A subclass can pass every compiler check and still be a **poor subtype**. `class Stack<E> extends ArrayList<E>` gets storage and machinery for free — and along with them `add(index, e)`, `insert`, and every other list affordance that lets a client corrupt the stack discipline. The compiler sees a perfect `Stack` *is-a* `ArrayList`; the design sees none. This is **white-box reuse**: the subclass silently depends on base internals ([[What is the fragile base class problem]]). The safe route when the goal is reuse is composition with delegation ([[How does composition differ from inheritance]]; [[What are alternatives to class inheritance]]).

## Substitutability without inheritance

Interfaces show the opposite direction: `Integer` and `BigInteger` are both `Comparable<Integer>` yet share no implementation at all. Subtyping organizes **clients** (what may be passed where); inheritance organizes **implementors** (who reuses whose code). Keeping the questions separate — *"may I pass X here?"* vs *"did X get code for free?"* — dissolves most inheritance debates, including the is-a vs has-a confusion ([[What do in OOP expressions is-a and has-a]]).

```d2
direction: down
lat: "Type lattice\nis-a edges: assignment, calls" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
kw: "extends / implements" {
  width: 220
  height: 44
  style.fill: "#fff8e1"
}
code: "Class body\nmember reuse: what code exists" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
kw -> lat: "subtype edge"
kw -> code: "reuse edge"
```

**Fig. 1.** One keyword, two independent edges. Interface methods make the split visible: a type edge with no inherited body.

```java
class Stack<E> extends ArrayList<E> {          // reuse: yes. Substitutability: no.
    public E push(E e) { add(e); return e; }   // clients can still call add(0, e) -> corrupted stack
}

record Max(int value) implements Comparable<Max> {   // subtype without any inherited code
    @Override public int compareTo(Max o) { return Integer.compare(value, o.value); }
}
```

**Listing 1.** Conceptual. `Stack extends ArrayList` proves subclassing, not subtyping discipline; `Max` is a subtype of `Comparable` with zero inheritance.

> [!warning] "It compiles, therefore it substitutes" is false
> The Java compiler enforces only the **signature** slice of subtyping: same or covariant return, matching parameters, no weaker access. The **behavioral** part — contracts, invariants, history ([[What does behavioral subtyping require beyond matching signatures]]) — lives entirely outside the type checker, which is why LSP violations compile cleanly ([[How would you explain the Liskov substitution principle in SOLID]]).

> [!tip] Interview answer
> Subtyping is the type-level is-a: it licenses substitution through a base reference. Inheritance is the code-level mechanism: members arrive for free. Java's `extends` bundles both, so a class can be a perfect subclass and a poor subtype — `Stack extends ArrayList` reuses code while exposing list operations that break the stack. When I need reuse without is-a, I compose; when I need is-a without shared code, I reach for interfaces.
