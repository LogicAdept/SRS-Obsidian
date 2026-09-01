<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers #Java/JMM #SRS

# What does volatile on a reference field guarantee for visibility?

> [!abstract] Short answer
> A **`volatile` write** of a **reference** **happens-before** every **later read** of **that same field**. Happens-before is **transitive**, so writes the publisher made **in program order before** that store (constructing the object, filling fields) are **visible** to a reader that has **observed** the new reference. It does **not** freeze the object forever: later unsynchronized writes to the **referent’s** fields are ordinary **data races**. It is **not** a lock and **not** atomicity of `holder.n++`. Field modifier: [[How would you explain the volatile field modifier in Java]]. HB: [[How would you explain the happens-before guarantee in the Java Memory Model]]. JMM: [[How would you explain memory Java]]. `final` freeze: [[How would you explain immutability and its benefits in Java]].

## Publish the graph, not every later mutation

The volatile variable is the **reference**, not the object’s internals. Safe-publication pattern: fully initialize a **new** object, then **assign** the `volatile` field. A reader that sees **non-null** may use those **pre-publication** writes. Sharing one mutable object and updating fields **after** both threads have the reference still needs **`synchronized`**, **`volatile` on those fields**, **atomics**, or **immutability**. Vs atomics: [[What is the difference between volatile fields and atomic variables]]. Compound updates: [[How does volatile visibility differ from atomicity for compound updates]].

A **`volatile` array reference** publishes that **array object**; slots are **not** automatically volatile. **`AtomicReference`** is a volatile-like **reference** plus CAS.

```java
final class Box {
    int n;
}
volatile Box published;

void publish() {
    Box b = new Box();
    b.n = 42;          // program order before the volatile write
    published = b;     // release
}

int consume() {
    Box b = published; // acquire
    return b == null ? -1 : b.n; // 42 if b is the published instance
}
```

**Listing 1.** After `consume` sees `b`, it sees `n == 42`. A later `published.n = 7` without extra ordering is **not** covered.

```d2
direction: down
init: "writes to object fields" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
vw: "volatile store of reference" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
vr: "later volatile load" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
use: "read those fields" {
  width: 170
  height: 36
  style.fill: "#f3e5f5"
}
init -> vw: "program order"
vw -> vr: "HB same field"
vr -> use: "transitive HB"
```

**Fig. 1.** Visibility of **pre-store** writes. Post-publication mutation is a different race.

> [!warning] Not a deep `volatile` of every field
> `volatile Box box` does not make `box.n` volatile. Two threads mutating `n` still race.

> [!warning] `null` means “not published yet,” not “object is gone”
> A reader that sees `null` must not assume a previous instance’s fields. Replacing the reference publishes a **different** object.

> [!tip] Interview answer
> Volatile on a reference makes the write of that pointer happen-before later reads of it, so a reader who sees the object also sees the writes that built it. It does not make later field updates on that object visible by themselves. For a mutable shared object I still need more synchronization or I make it immutable.
