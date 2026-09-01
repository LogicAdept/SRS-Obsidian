<!--
reps: 0
priority: 0
-->
#Java/Immutability #Java/Language/Modifiers/Final #SRS

# What language and class design features enforce immutability?

> [!abstract] Short answer
> The language does not have an `immutable` keyword. You combine **`final` fields** (no reassignment, freeze at the end of the constructor), **`private` fields** (no assignment from outside), and a **`final` class** — or a **private constructor** plus factories — so subclasses cannot add mutation or override methods. **Records** bake in a `final` class and `private final` component fields. Design still has to **omit setters**, **copy mutable inputs and outputs**, and **not publish `this` before the constructor finishes**. `final` itself: [[What does the final keyword mean in Java]]. Why you write it: [[What are use cases for the final keyword in Java]]. Hiding fields: [[How would you explain private]].

## Language knobs

- **`final` instance fields** — assigned once; after the constructor completes, other threads that only then see the object are guaranteed to see those field values (do not leak `this` earlier).
- **`private` fields** — another class cannot assign them. Accessors, if any, must not hand out a live mutable object.
- **`final` class** — no subclass that adds setters or mutable state. Alternative: **private constructor** and static factories so there is no accessible constructor to extend.
- **Record classes** — implicitly `final`; each component is a `private final` non-`static` field plus an accessor. That is **shallow**: a component of type `List` can still be mutated through the list.

`final` on a **method** stops override of that method. It does not freeze fields. `static final` constants are inlined compile-time values; they are not the same as an immutable *object*.

## Class design (the rest of the recipe)

1. No mutator methods. Operations that would change state **return a new instance**.
2. Every field `private` and `final`.
3. Block subclassing (`final` class or private constructor).
4. If a field refers to a **mutable** object: do not store the caller’s object; **copy in**. Do not return the internal object; **copy out**. Do not expose methods that mutate it in place.

```java
final class Path {
    private final int[] pts;

    Path(int[] pts) {
        this.pts = pts.clone();
    }

    int[] points() {
        return pts.clone();
    }
}

record Box(List<String> items) {} // items list is still mutable
```

**Listing 1.** `Path` copies the array both ways. `Box` is a `final` record with `private final` fields and is **not** deep-immutable if callers keep the list.

```d2
direction: down
goal: "immutable instance" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
lang: "final class + private final fields\n(record does this)" {
  width: 260
  height: 48
  style.fill: "#e3f2fd"
}
des: "no setters, copy mutable\nstate, do not leak this" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
goal -> lang
goal -> des
```

**Fig. 1.** Keywords lock identity and subclassing. Design locks the objects those fields refer to.

> [!warning] `final` on a field is not immutability
> `final List<String> xs` forbids `xs = ...`. Callers can still `xs.add(...)`. A `final` class with a public mutable field is not an immutable type.

> [!warning] Records do not deep-copy
> `record Box(List<String> items)` still shares the list. Treat records as immutable only when every component type is immutable (or you copy before construction and never expose the original).

> [!tip] Interview answer
> Make the class `final` (or hide the constructor), make every field `private final`, provide no setters, and copy any mutable objects you store or return. Records give you the `final` class and `private final` fields automatically, but not deep immutability. `final` also freezes those fields for other threads once the constructor finishes — if you do not publish `this` early.
