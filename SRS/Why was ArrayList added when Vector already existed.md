<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/List/Vector #SRS

# Why was `ArrayList` added when `Vector` already existed?

> [!abstract] Short answer
> **`ArrayList` is the unsynchronized resizable-array `List` in the Collections Framework (Java 1.2).** `Vector` (1.0) locks every method. The API: if you do not need a thread-safe list, **use `ArrayList`**. Growth (Vector double vs ~1.5×) is a side difference, not the reason it was added.

## Unsynchronized default `List`

```d2
direction: right
v: "Vector 1.0\nsynchronized methods" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
al: "ArrayList 1.2\nunsynchronized List" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}

v -> al: "Framework default"
```

**Fig. 1.** Same growable-array shape; the new type drops method-level locks ([[What is the difference between ArrayList and Vector]]).

`ArrayList` is “roughly equivalent to `Vector`, except that it is unsynchronized.” `Vector`: “Unlike the new collection implementations, `Vector` is synchronized. If a thread-safe implementation is not needed, it is recommended to use `ArrayList` in place of `Vector`.” That is the documented why ([[How would you explain java.util.Vector and why it is legacy]]).

`Vector` was retrofitted as a `List` in 1.2 and kept old names (`addElement`, `elementAt`) plus `elements()` (`Enumeration`, not fail-fast). `ArrayList` is the Framework `List`: fail-fast iterators, no per-call lock, `null` allowed. Concurrent structural use needs an external lock or `Collections.synchronizedList`. A synchronized `add` still does not make a `for` loop atomic.

Dump “Vector doubles, ArrayList grows by half” is **not** the design reason. `Vector` documents doubling when `capacityIncrement` is ≤ 0. `ArrayList`’s growth factor is **unspecified**; OpenJDK prefers `oldCapacity >> 1` (~1.5×) ([[How does resize ArrayList]]).

```java
List<String> local = new ArrayList<>(); // 1.2 default, no lock
local.add("a");

Vector<String> locked = new Vector<>();
locked.add("a"); // synchronized method, 1.0 API
```

**Listing 1.** Why interviews contrast them: locking, not the grow multiplier.

> [!warning] `Vector` is not forbidden; it is not the default
> It is still in `java.util`. Do not pick it for a documented 2× grow. Prefer `ArrayList` unless you still depend on `Vector`. For a concurrent `List` with snapshot iterators, that is `CopyOnWriteArrayList`, not “a faster Vector” ([[What is the difference between ArrayList Vector and CopyOnWriteArrayList]]).

> [!warning] Synchronized `Vector` is not a snapshot
> Method locks serialize one call. Fail-fast `iterator()` can still throw `ConcurrentModificationException` if another thread mutates.

> [!tip] Interview answer
> **`ArrayList` was added as the unsynchronized resizable-array `List` when collections arrived in 1.2.** `Vector` already existed with synchronized methods. Use `ArrayList` unless you need that old locking (or a real concurrent list). Grow 2× vs ~1.5× is an implementation detail, not why `ArrayList` exists.
