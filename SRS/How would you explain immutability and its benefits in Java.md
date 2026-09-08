<!--
reps: 0
priority: 0
-->
#Java/Immutability #Java/OOP #Java/Concurrency #Java/String #SRS

# How would you explain immutability and its benefits in Java?

> [!abstract] Short answer
> An object is **immutable** when its observable state **cannot change** after the constructor finishes. Java has **no `immutable` keyword**; you get it with **`final` fields**, no mutators, and **no leaked mutable internals**. Benefits: **share without locks**, **stable `hashCode`** (map/set keys), cheaper sharing (`String` is constant and **can be shared**), and **`final`-field freeze** so another thread that only sees the object **after construction** reads the initialized finals — even if the reference was passed in a **data race**. How to build one: [[How would you explain immutable classes in Java]]. Concurrency value: [[Why are immutable objects valuable in concurrent code]]. Why `String`: [[Why is java.lang.String immutable and final]].

## Freeze the state, then share the reference

Set **`final` fields in the constructor**. Do **not** publish `this` (statics, other threads, inner-class leak) **before** the constructor returns. Then every later reader of those finals sees the values written in the constructor, and sees the objects/arrays those finals refer to **at least as up-to-date** as the freeze. That is how you get **thread-safe immutable objects without synchronization**.

`String` is the platform example: values do not change; implementations can share instances. Security-sensitive code treats a `String` as **one** sequence, not a sequence that morphs after a racy publish. Wrapper types and well-designed records follow the same idea. API use: [[How are immutable objects used in Java APIs]]. Sibling wording: [[How would you explain immutable objects and why they matter]].

A **`final` field that holds a mutable object** is not an immutable type. Callers who receive the raw `List` can still mutate it. Defensive copies or unmodifiable views belong in the constructor and getters. Language/class rules: [[What language and class design features enforce immutability]].

```java
final class Point {
    private final int x;
    private final int y;
    Point(int x, int y) { this.x = x; this.y = y; }
    int x() { return x; }
    int y() { return y; }
}
```

**Listing 1.** After construction, `x` and `y` cannot be assigned again. Threads may share one `Point` without locking those fields.

```d2
direction: down
ctor: "constructor writes finals\nthen returns" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
pub: "publish reference" {
  width: 180
  height: 40
  style.fill: "#fff8e1"
}
read: "other threads see frozen finals" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
ctor -> pub: "no early this leak"
pub -> read: "no lock required"
```

**Fig. 1.** Benefit is safe sharing **after** a completed constructor, not “`final` means skip the constructor protocol.”

> [!warning] `final` reference ≠ immutable object
> If the field is a `List` or array you still expose, callers can change elements. Freeze applies to the **reference**, not to the graph unless that graph is immutable too.

> [!warning] Do not publish `this` during construction
> A racy store of the object **before** the constructor finishes can let another thread see **default** `final` values. The freeze happens when the constructor **exits**.

> [!tip] Interview answer
> Immutability means state does not change after construction, usually via private final fields and no setters. You can share those objects across threads without locking, and they make safe map keys because hashCode stays stable. String works that way; a final field pointing at a mutable list does not.
