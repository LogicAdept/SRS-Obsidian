<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Concurrency/Atomics #SRS

# How would you write a minimal non-blocking ArrayList (add, get, remove, size)?

> [!abstract] Short answer
> The exercise is a **tiny copy-on-write list**: **`add` / `get` / `remove` / `size`**, no mutex on **reads**. The inherited sketch (`volatile Object[]` + copy + assign) is **not** an `ArrayList` and **not** race-free: two writers copy the **same** snapshot and **one append is lost**. Production type: **`CopyOnWriteArrayList`** — mutative ops **copy** the array; **`get`/`size` read a snapshot**; iterators never `ConcurrentModificationException`. OpenJDK **serializes writers** with a **private monitor**; **lock-free** writers need **`AtomicReference.compareAndSet`** (retry). Vs `ArrayList`: [[What is the difference between CopyOnWriteArrayList and ArrayList]]. Tradeoffs: [[What are CopyOnWriteArrayList thread safety tradeoffs]]. Atomics: [[How would you explain Java atomic types in java.util.concurrent.atomic]].

## Snapshot, copy, publish

`get`/`size` load the current array (volatile / atomic) and **do not** lock. A writer allocates a **new** array, copies, then publishes. **`volatile` publish alone is not a CAS**: it does not detect that another thread already published. **`compareAndSet`** retries until **this** copy replaces the array we read. New arrays avoid ABA on the reference.

That is still **not** `java.util.ArrayList`: no spare capacity, **O(n)** writes, **`add(index)` must shift**, `remove(int)` returns the element and uses **`IndexOutOfBoundsException`**. The sketch’s `add(index)` was a **sparse set**, `equals` logic inverted, and `remove` **arraycopy** dropped the tail. JDK list: [[What are Java CopyOnWrite collections]]. Happens-before: placing an element **happens-before** a later `get`/`remove` of it in another thread.

```java
final class CowList<E> {
    private final AtomicReference<Object[]> ref =
            new AtomicReference<>(new Object[0]);

    boolean add(E e) {
        for (;;) {
            Object[] prev = ref.get();
            Object[] next = Arrays.copyOf(prev, prev.length + 1);
            next[prev.length] = e;
            if (ref.compareAndSet(prev, next)) return true;
        }
    }

    @SuppressWarnings("unchecked")
    E get(int i) {
        Object[] a = ref.get();
        if (i < 0 || i >= a.length) throw new IndexOutOfBoundsException();
        return (E) a[i];
    }

    int size() { return ref.get().length; }
}
```

**Listing 1.** Lock-free **append**. `remove(i)` is the same loop: copy **without** slot `i`, then CAS. OpenJDK `CopyOnWriteArrayList.add` copies under **`synchronized (lock)`** instead of CAS.

```d2
direction: down
r: "read array snapshot" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
c: "copy + mutate" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
cas: "CAS publish" {
  width: 140
  height: 36
  style.fill: "#e8f5e9"
}
r -> c -> cas
cas -> r: "lost race: retry"
```

**Fig. 1.** Readers never wait. Writers retry if someone else published first. A plain `content = renewed` skips the retry.

> [!warning] `volatile Object[]` is not a concurrent list
> Visibility of the **reference** does not make **read-copy-write** atomic. Lost updates look like “sometimes size is short.”

> [!warning] Copy-on-write is for rare writes
> Every `add`/`remove` allocates and copies. High-mutation workloads want a **real concurrent** structure or an exclusive lock around an `ArrayList`, not this pattern.

> [!tip] Interview answer
> I would copy-on-write the backing array so get and size only read a snapshot. A volatile assign is not enough; I CAS the new array or I use CopyOnWriteArrayList, which locks writers and copies. I would not ship the sparse set-style add from the sketch; add must append or insert and shift.
