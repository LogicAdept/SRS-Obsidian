<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/List/Vector #SRS

# What is the difference between `ArrayList` and `Vector`?

> [!abstract] Short answer
> Both are resizable-array `List`s. `ArrayList` is **unsynchronized** (Java 1.2). `Vector` is the **synchronized** 1.0 list; use `ArrayList` when you do not need thread safety. Iterators on both are fail-fast. `Vector` also exposes `elements()`, a non-fail-fast `Enumeration`. Growth: `Vector` documents doubling when `capacityIncrement` is ≤ 0; `ArrayList`’s factor is unspecified.

## Same array list, different locking

```d2
direction: right
al: "ArrayList\nunsynchronized\nfail-fast iterator" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
vec: "Vector\nsynchronized methods\nfail-fast iterator\nelements() Enumeration" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
```

**Fig. 1.** `ArrayList` is “roughly equivalent to `Vector`, except that it is unsynchronized” ([[What is an ArrayList]]).

`Vector` predates the Collections Framework (1.0) and was retrofitted as a `List` in 1.2. “Unlike the new collection implementations, `Vector` is synchronized.” If a thread-safe implementation is **not** needed, the API recommends `ArrayList` ([[Why was ArrayList added when Vector already existed]], [[How would you explain java.util.Vector and why it is legacy]]).

| | `ArrayList` | `Vector` |
| --- | --- | --- |
| Synchronization | none; concurrent structural use needs an external lock | every public mutator/accessor is synchronized |
| Iterators | fail-fast | `iterator`/`listIterator` fail-fast; `elements()` is **not** |
| Default empty capacity | “capacity of ten” | 10, `capacityIncrement` 0 |
| Growth | unspecified beyond amortized end `add` | increment > 0 → add that many slots; else **double** (or `minCapacity`) |
| `null` | allowed | allowed |

`ArrayList` growth in OpenJDK is about 1.5×; that is **not** the public contract ([[How does resize ArrayList]]). `Vector(int,int)` lets you pick `capacityIncrement`. Both still copy into a larger array on overflow.

A synchronized `Vector.add` does **not** make a multi-step loop atomic. Fail-fast iterators can still throw `ConcurrentModificationException` if another thread mutates. `Collections.synchronizedList(new ArrayList<>())` is the documented wrapper when you want an `ArrayList` plus a lock; traversal must still be in `synchronized (list) { … }`. Snapshot iteration is a different type ([[What is the difference between ArrayList Vector and CopyOnWriteArrayList]]).

```java
List<String> local = new ArrayList<>();
local.add("a"); // no lock

Vector<String> locked = new Vector<>();
locked.add("a"); // synchronized method

Enumeration<String> e = locked.elements(); // not fail-fast
```

**Listing 1.** Same `add`; only `Vector` locks the method. Prefer `ArrayList` on one thread.

> [!warning] Synchronized methods ≠ a safe `for` loop
> `Vector` locks each call, not a whole iteration. Another thread’s `add`/`remove` can still make `iterator()` fail-fast. `elements()` is explicitly **undefined** if the vector is structurally modified during enumeration.

> [!warning] Do not pick `Vector` for a documented 2× grow
> `ArrayList` does not promise doubling. If you need a known extra capacity, pass it to `ArrayList(int)` / `ensureCapacity`, or use `Vector`’s `capacityIncrement` only when you already depend on the `Vector` API.

> [!tip] Interview answer
> **`ArrayList` is the ordinary unsynchronized resizable array list. `Vector` is the old synchronized one — same `List` shape, method-level locks, and a documented grow (double when increment is 0). Use `ArrayList` unless you still need `Vector`; wrapping with `Collections.synchronizedList` is the Framework way to lock an `ArrayList`.**
