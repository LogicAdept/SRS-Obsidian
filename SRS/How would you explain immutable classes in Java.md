<!--
reps: 0
priority: 0
-->
#Java/Immutability #Java/OOP #Java/JMM #SRS

# How would you explain immutable classes in Java?

> [!abstract] Short answer
> An **immutable class** is one whose instances, once constructed, never change **observable state**. Typical recipe: **`final` class** (no subclass adding setters), **`private final` fields** assigned in the constructor, **no mutators**, **defensive copies** of any mutable parts, and **do not publish `this`** before the constructor finishes. `final` fields **freeze** when the constructor exits, so other threads that only see the object afterward see those fields correctly **without locking**. Platform examples: `String`, wrappers, `java.time`. Why it matters: [[How would you explain immutability and its benefits in Java]]. `String`: [[Why is java.lang.String immutable and final]]. APIs: [[How are immutable objects used in Java APIs]].

## State frozen at the end of `new`

**Language pieces.** A `final` instance field must be definitely assigned by every constructor. A `final` class cannot be subclassed. A **record** is implicitly `final` and holds `private` component fields ([[What is a Java record]]). `sealed` can close the set of subtypes if you need a small hierarchy instead of `final` ([[How would you explain Sealed classes]]).

**Memory.** Completely initialized means the constructor has finished. A thread that only sees the reference **after** that is guaranteed to see the `final` fields. Set those fields in the constructor; do not store `this` where another thread can read it first. Then you can share the object with a data race and it still looks immutable. Compilers may cache `final` reads; that is the point.

**Mutable guts.** `final int[] data` is a **fixed reference**, not a frozen array. Store `data.clone()` and return `data.clone()` ([[How would you explain copy constructors or defensive copying in Java]]). `List.copyOf` snapshots slots; mutable **elements** still move. `Collections.unmodifiableList` is a **view**, not an immutable class.

**Operations return new instances** (`plus`, `with`, `concat`), they do not assign to fields. That is how `String` and `LocalDate` stay shareable map keys and messages.

```d2
direction: down
new: "constructor assigns final fields" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
fr: "constructor exits → freeze" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
share: "other threads see those fields\nno lock required" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
new -> fr
fr -> share
```

**Fig. 1.** Immutability is “no writes after freeze,” plus not leaking `this` early.

```java
final class Box {
    private final int[] data;

    Box(int[] data) {
        this.data = data.clone();
    }

    int[] snapshot() {
        return data.clone();
    }

    Box plus(int x) {
        int[] n = java.util.Arrays.copyOf(data, data.length + 1);
        n[data.length] = x;
        return new Box(n);
    }
}

record Point(int x, int y) {}
```

**Listing 1.** `Box` copies the array in and out and mutates by returning a new `Box`. `Point` is an immutable aggregate by record rules.

> [!warning] `final` on a field does not freeze the object it points to
> `private final List<String> names = names;` still aliases a mutable list. Copy, or use an unmodifiable **copy** of immutable elements. A setter on a **subclass** also breaks immutability — keep the class `final` (or sealed and honest).

> [!warning] Publishing `this` from the constructor voids the `final` guarantee
> A listener list, a static `INSTANCES.add(this)`, or starting a thread with `this` before the constructor returns lets another thread read default zeros for `final` fields. Assign, finish the constructor, then publish.

> [!warning] Unmodifiable ≠ immutable class
> `List.of` forbids `add`, but a mutable element still changes what `get` shows. `Integer` and `LocalDate` are value-based: do not synchronize on them.

> [!tip] Interview answer
> An immutable class never changes state after construction: final type, private final fields, no setters, copy mutable arguments, do not leak this. Final fields freeze when the constructor ends, so the object can be shared across threads without locks. String, java.time, and records follow that model; operations return new instances instead of mutating.
