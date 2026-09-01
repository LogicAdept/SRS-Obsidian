<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

# Can a Java enum implement an interface?

> [!abstract] Short answer
> **Yes.** An enum declaration may have an `implements` list, like a class: `enum Name implements I, J { … }`. That is the usual substitute for “extend a class,” which an enum cannot do. Interface methods still have to be implemented — in the enum body, by a default method you inherit, or by a class body on **every** constant.

## `implements` is in the declaration; `extends` is not

An enum class is a class. It already has superclass `Enum<E>`, so there is no `extends` clause ([[Can a Java enum extend a class]]). Superinterfaces are separate: the optional `implements` clause names any number of interfaces (no duplicates, no conflicting parameterizations of the same generic interface).

`java.lang.Enum` already implements `Comparable<E>`, `Serializable`, and `Constable`. Those come with every enum; you do not implement them to “turn on” ordering or serialization. `compareTo` is `final` on `Enum` ([[Can you override compareTo on a Java enum]]). Serialization of constants is special ([[How does Java serialization treat enum constants]]).

```d2
direction: down
op: "interface Op" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
math: "enum MathOp\nimplements Op" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
en: "Enum<MathOp>\nComparable, Serializable, Constable" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}

math -> op
math -> en
```

**Fig. 1.** `MathOp` may implement `Op`. It cannot also extend a user class; `Enum` is already the superclass and already brings `Comparable` / `Serializable` / `Constable`.

Because an enum is implicitly `final` or implicitly `sealed`, it can implement a `sealed` interface (it still has to be named in that interface’s `permits` list).

## How the methods get implemented

The enum is not an `abstract` class, so every abstract interface method must become concrete. Three legal ways:

1. One concrete method in the enum body — all constants share it.
2. A `default` method on the interface — inherited unless you override it.
3. A class body on **every** constant — per-constant behaviour, the usual replacement for a `switch` on the enum.

```java
interface Op {
    int apply(int a, int b);
}

enum MathOp implements Op {
    ADD {
        public int apply(int a, int b) { return a + b; }
    },
    MUL {
        public int apply(int a, int b) { return a * b; }
    };
}

// MathOp.ADD.apply(2, 3) -> 5
// Op asInterface = MathOp.MUL;  // assignable to the interface
```

**Listing 1.** Per-constant implementations. `apply` must be `public` (interface methods are public). It is a member of `MathOp`, so you can call it on the enum type or on `Op`.

```java
interface Named {
    String name();
    default String label() { return name(); }
}

enum Color implements Named { RED, GREEN }

interface IdOp {
    int apply(int a, int b);
}

enum Unit implements IdOp {
    ID;
    public int apply(int a, int b) { return a; }
}

// Color.RED.label() -> "RED"  (Enum.name() satisfies Named.name())
// Unit.ID.apply(1, 2) -> 1
```

**Listing 2.** No constant class bodies: inherit a `default` method, or implement the interface once in the enum body. `Enum.name()` can satisfy an interface method of the same signature.

If the method stays abstract as a member of the enum — inherited from the interface and not implemented in the enum body — every constant must have a class body that implements it. That is the same rule as declaring `abstract` methods on the enum ([[Can a Java enum have abstract methods]]).

```java
class Base {}
interface Marker {}

enum Status implements Marker { OK, FAIL }

// enum Status extends Base implements Marker { OK } // compile error: no extends clause
// enum Partial implements Op { ADD { public int apply(int a, int b) { return a + b; } }, MUL }
// compile error: MUL has no class body and Partial does not implement apply
```

**Listing 3.** Conceptual: `implements` does not unlock `extends`. A missing constant body leaves the interface method abstract.

> [!warning] `implements` does not lift the superclass rule
> `enum X extends Foo implements Bar` is still illegal. Put the shared contract on `Bar` (and default methods if you want shared code). Composition in the enum body is the other option.

> [!warning] Do not implement `Comparable` to “customize order”
> `Enum` already implements `Comparable<E>` and `compareTo` is `final` (declaration order / `ordinal`). `implements Comparable<String>` conflicts with `Comparable<E>`. Restating `implements Comparable<YourEnum>` is redundant, not a hook for a different ordering.

> [!tip] Interview answer
> **Yes — an enum can implement any number of interfaces, and that is the replacement for extending a class.** `Enum` already gives you `Comparable`, `Serializable`, and `Constable`. Abstract interface methods must be implemented in the enum, inherited as defaults, or implemented in every constant’s class body.
