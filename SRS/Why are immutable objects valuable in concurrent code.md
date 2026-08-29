<!--
reps: 0
priority: 0
-->
#Java/Immutability #Java/Concurrency #Java/JMM #SRS

# Why are immutable objects valuable in concurrent code?

> [!abstract] Short answer
> A **correctly built immutable object** (typically **`final` fields**, no leaked `this`, no mutable internals) can be **shared by many threads without `synchronized` or `volatile` on that object**. Other threads see the **frozen** `final` values **even if the reference is published in a data race**. That is why **`String`** can skip locks and still be safe. There is **no** `java.lang` `@Immutable`. Mutable shared state still needs a lock, `volatile`, or a concurrent structure: [[How would you explain thread safety for shared mutable state]]. Sharing protocol: [[How do you share data between two threads in Java]]. Data race vs race condition: [[What is the difference between a race condition and a data race]]. How to write one: [[How do you implement an immutable class in Java]]. Broader value: [[Why is immutability valuable in Java programs]]. `String`: [[Why is java.lang.String immutable and final]].

## Freeze, then share

When the constructor **finishes**, `final` fields **freeze**. A thread that **first sees** the object **after** that is guaranteed those `final` values (and the objects/arrays they refer to, **as of that freeze**). Compilers may **cache** `final` reads. **Do not** store `this` where another thread can read it **before** the constructor ends.

A **non-`final`** field on the same object is **not** covered: a racy reader can still see the **default**. A **`final` reference to a mutable array or list** is not an immutable object.

```d2
direction: down
ctor: "constructor finishes (final freeze)" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
share: "share the reference freely" {
  width: 240
  height: 36
  style.fill: "#e3f2fd"
}
mut: "mutable fields: lock or volatile" {
  width: 260
  height: 36
  style.fill: "#ffebee"
}
ctor -> share
ctor -> mut
```

**Fig. 1.** Immutability buys **publication of that object**. It does **not** freeze other shared mutables.

```java
final class Point {
    private final int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }
    int x() { return x; }
    int y() { return y; }
}
```

**Listing 1.** After construction, threads may read `x()`/`y()` with **no** lock on `Point`.

> [!warning] `final` is not a magic “immutable” stamp
> Leak `this` from the constructor, keep a **mutable** field, or mutate via **reflection**, and the freeze story **does not** hold. `Collections.unmodifiableList` is a **view**, not a new immutable type.

> [!warning] Non-`final` still races
> Publish `new Holder()` through a plain static and a reader may see **`final x == 3`** and **`y == 0`**. Use `final` (or a safe publish) for every field that must be visible.

> [!tip] Interview answer
> Immutable objects are valuable in concurrent code because their state never changes, so you can share them without locking that object. Final fields freeze at the end of the constructor, so other threads see the initialized values even if the reference is passed in a data race. You still must not leak this during construction, and a final pointer to a mutable array is not immutable.
