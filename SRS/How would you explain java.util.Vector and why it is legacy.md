<!--
reps: 0
priority: 0
-->
#Java/Collections/List/Vector #Java/Collections/Concurrency #Java/Legacy #SRS

# How would you explain java.util.Vector and why it is legacy?

> [!abstract] Short answer
> **`Vector`** is a **growable array** (`List`, `RandomAccess`) from **Java 1.0**, **retrofitted** onto the collections framework in **1.2**. **Unlike later lists, every mutating/query method is synchronized.** The platform still calls it a **legacy collection**. If you do **not** need a thread-safe list, use **`ArrayList`**. If you do, prefer **`Collections.synchronizedList(new ArrayList<>())`** (and lock when iterating) or a **`java.util.concurrent`** list — not `Vector` as the default. Why ArrayList exists: [[Why was ArrayList added when Vector already existed]]. ArrayList vs Vector: [[What is the difference between ArrayList and Vector]]. COW list: [[What is the difference between ArrayList Vector and CopyOnWriteArrayList]].

## Synchronized growable array, pre-framework API

It stores elements in an `Object[]` (`elementData`), with `elementCount` and optional `capacityIncrement`. Capacity is at least size; you can **`ensureCapacity`** before a bulk insert. `iterator` / `listIterator` are **fail-fast** (`ConcurrentModificationException` is **best-effort**, not a protocol). **`elements()`** returns an **`Enumeration` that is not fail-fast** — concurrent structural change makes enumeration **undefined**.

**Legacy** here means: it predates `List`, keeps old names (`elementAt`, `addElement`), and **`java.util` documents legacy collection classes**. `Stack` **extends** `Vector`. Method-level `synchronized` serializes **one** call. `if (v.size() > 0) v.get(0)` is still a race. `synchronizedList` states the iteration rule explicitly: traverse under **`synchronized (list)`**. Sharing lists: [[How do you share data between two threads in Java]].

```java
List<String> unsync = new ArrayList<>();           // no thread-safety
List<String> wrapped = Collections.synchronizedList(new ArrayList<>());
Vector<String> legacy = new Vector<>();            // synchronized methods; still 1.0 API
```

**Listing 1.** Same “growable array” job. The javadoc’s replacement for a non-concurrent case is `ArrayList`.

```d2
direction: down
v: "Vector (1.0)\nsynchronized methods" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
al: "ArrayList\nif no sharing" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
wrap: "synchronizedList / j.u.c" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
v -> al: "no thread-safety needed"
v -> wrap: "need a concurrent list"
```

**Fig. 1.** Legacy is the type and the coarse lock, not “it does not work.”

> [!warning] Synchronized methods ≠ a thread-safe algorithm
> Two calls can still interleave. Fail-fast iterators do not replace a lock around a whole loop. Do not depend on `ConcurrentModificationException` for correctness.

> [!warning] `Enumeration` is the old, racy cursor
> `elements()` is **not** fail-fast. Prefer `iterator()` and, for a wrapped list, the documented **synchronized** traversal.

> [!tip] Interview answer
> Vector is a synchronized growable array from before the collections framework, later made to implement List. It is legacy because new code should use ArrayList when unsynchronized, or a synchronized wrapper or concurrent list when shared. Per-method locks still do not make check-then-act atomic.
