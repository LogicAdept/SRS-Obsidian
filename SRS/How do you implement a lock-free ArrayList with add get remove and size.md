<!--
reps: 0
priority: 0
-->
#OperatingSystems/Concurrency/LockFree #Java/Concurrency/Atomics #Java/Collections/Concurrency #Java/Collections/List/ArrayList #Career/Interview/Exercises #SRS

# How do you implement a lock-free `ArrayList` with `add`, `get`, `remove`, and `size`?

> [!abstract] Short answer
> You do **not** start from `java.util.ArrayList`. The JDK has no lock-free indexed list. Build on `java.util.concurrent.atomic` (`AtomicReferenceArray` + `AtomicInteger` / CAS), or **copy-on-write** the array and `compareAndSet` the reference. `get` and end-`add` can be lock-free; `remove` that **shifts** like `ArrayList` is not one CAS. For a real `List`, use `CopyOnWriteArrayList`; for a lock-free FIFO, `ConcurrentLinkedQueue`.

## Why `ArrayList` is the wrong base

`ArrayList` is unsynchronized: concurrent structural use needs an external lock or `Collections.synchronizedList`. Those are **locks**, not lock-free. `java.util.concurrent` says a `CopyOnWriteArrayList` is preferable to a synchronized `ArrayList` when reads/traversals vastly outnumber updates — writers still **copy the whole array** ([[What is the difference between CopyOnWriteArrayList and ArrayList]]).

Lock-free updates of **one** cell or counter live in `java.util.concurrent.atomic`: `compareAndSet`, `getAndUpdate`, `AtomicInteger.getAndIncrement`, and `AtomicReferenceArray` (volatile per slot). There is no `ConcurrentArrayList`.

```d2
direction: down
need: "List-like add / get / remove / size\nshared by threads, no monitors" {
  width: 340
  height: 70
  style.fill: "#e3f2fd"
}
atoms: "AtomicReferenceArray + AtomicInteger\nCAS loops, not synchronized ArrayList" {
  width: 340
  height: 80
  style.fill: "#fff3e0"
}
jdk: "JDK instead:\nCopyOnWriteArrayList or ConcurrentLinkedQueue" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}

need -> atoms
need -> jdk
```

**Fig. 1.** Interview design vs what the platform already ships.

## A minimal CAS sketch (not a `List`)

Treat the buffer as `AtomicReferenceArray<E>` and the logical length as `AtomicInteger`. `get(i)` is `array.get(i)` after a bounds check against `size` (volatile `get`). End `add` can `int i = size.getAndIncrement()` then `array.set(i, e)` **only if** `i < array.length()` — overflow needs a **new** array published with `AtomicReference.compareAndSet` of the buffer, or you reject the add.

Indexed `remove` in `ArrayList` shifts the tail with `System.arraycopy`. That is many slots; one `compareAndSet` cannot move them all. Official tools for **logical** delete: `AtomicMarkableReference` (mark bit = deleted) and `AtomicStampedReference` (stamp against ABA when a slot is reused). A lock-free “remove” is usually: CAS the slot to a tombstone, or pop the last index with `compareAndSet` on `size`. A true `ArrayList.remove(index)` clone is copy-on-write (CAS a copied array) or a linked structure.

```java
// Conceptual — not a complete List, not production
final class LockFreeBuffer<E> {
    private final AtomicReferenceArray<E> cells;
    private final AtomicInteger size = new AtomicInteger();

    LockFreeBuffer(int cap) {
        cells = new AtomicReferenceArray<>(cap);
    }

    E get(int i) {
        int n = size.get();
        if (i < 0 || i >= n) throw new IndexOutOfBoundsException();
        return cells.get(i); // VarHandle.getVolatile
    }

    void add(E e) {
        int i = size.getAndIncrement(); // may overshoot length()
        if (i >= cells.length()) throw new IllegalStateException("full");
        cells.set(i, e);
    }

    int size() {
        return size.get();
    }
}
```

**Listing 1.** Conceptual: lock-free **get** / **append** / **size** on a **fixed** buffer. `add` can race past `length()`; `remove` is omitted because a shifting remove is a different algorithm.

A second honest sketch is **copy-on-write**: snapshot the `Object[]`, copy, mutate, `AtomicReference.compareAndSet`. A plain `volatile` assign of the new array is **not** atomic read-copy-write — two writers can lose an append. OpenJDK `CopyOnWriteArrayList` copies under a **private monitor**, not CAS; iterators never `ConcurrentModificationException`. Tradeoffs: [[What are CopyOnWriteArrayList thread safety tradeoffs]]. Vs `ArrayList`: [[What is the difference between CopyOnWriteArrayList and ArrayList]]. Atomics: [[How would you explain Java atomic types in java.util.concurrent.atomic]]. JDK list: [[What are Java CopyOnWrite collections]].

```java
boolean add(E e) {
    for (;;) {
        Object[] prev = ref.get();
        Object[] next = Arrays.copyOf(prev, prev.length + 1);
        next[prev.length] = e;
        if (ref.compareAndSet(prev, next)) return true;
    }
}
```

**Listing 2.** Lock-free **append** by replacing the whole array. `remove(i)` is the same loop without slot `i`.

`ConcurrentLinkedQueue` is the JDK’s non-blocking unbounded queue (Michael–Scott). Its `size()` is **not** O(1) and may be wrong under concurrent mutation — a warning for any lock-free `size()`. Bulk ops are not atomic.

> [!warning] `synchronized` on `ArrayList` is not lock-free
> Wrapping `add`/`get`/`remove` in `synchronized` (or `Collections.synchronizedList`) gives mutual exclusion, fail-fast iterators, and still a shifting `remove`. The atomic package is for **single-variable** CAS, not a drop-in `ArrayList`.

> [!warning] `volatile Object[]` is not a concurrent list
> Visibility of the **reference** does not make **read-copy-write** atomic. Lost updates look like “sometimes size is short.” Tombstone `remove` (CAS-to-`null`) is not `ArrayList.remove`: holes disagree with compact `get(i)` / `size`.

> [!warning] Copy-on-write is for rare writes
> Every `add`/`remove` allocates and copies. High-mutation workloads want a real concurrent structure or a lock around an `ArrayList`. `AtomicMarkableReference` is the documented mark-for-delete pattern, not `System.arraycopy`.

> [!tip] Interview answer
> **Don’t lock `ArrayList`.** Use `AtomicReferenceArray` plus an atomic `size` for lock-free `get` and end-`add`, or CAS a copied array. Treat indexed `remove` as logical delete or copy-on-write. In production, pick `CopyOnWriteArrayList` for a `List`, or `ConcurrentLinkedQueue` if you need a non-blocking queue rather than random access.
