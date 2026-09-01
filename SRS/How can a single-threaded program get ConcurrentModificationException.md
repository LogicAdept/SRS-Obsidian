<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Collections/Iteration/FailFast #SRS

# How can a single-threaded program get `ConcurrentModificationException`?

> [!abstract] Short answer
> **Modify a fail-fast collection with a collection mutator while that thread’s own iterator is still walking it.** Enhanced `for` plus `list.remove(...)` is the usual demo — one thread, no lock, still CME. The exception name does **not** mean “two threads.” `Iterator.remove()` (or `removeIf`) is the in-walk delete that fail-fast allows. Concurrent / snapshot collections do not throw CME for this.

## The contract, not a second thread

`ConcurrentModificationException` may be thrown when a method detects a modification that is not allowed during that operation. Fail-fast iterators (`ArrayList`, `HashMap` views, and the other general-purpose JRE collections) throw it if the collection is **structurally** modified after the iterator was created, except through **that** iterator’s `remove` (and list-iterator `add`). A **single thread** that does `next`, then `coll.remove` / `add` / `put` of a **new** key, then `next` again is enough [[What is ConcurrentModificationException]], [[What counts as a structural modification for fail-fast iterators]].

Enhanced `for` is a hidden iterator, so `list.remove` in the body is that illegal mutator [[Can you modify a collection while iterating with a for-each loop]]. Fail-fast is **best-effort** (`modCount`); do not catch CME for control flow. `ArrayList.hasNext` does not check `modCount`, so some one-thread `list.remove` calls skip the tail **without** throwing — still a bug [[What is fail-fast iterator behavior in Java collections]].

`List.set` and `HashMap.put` of an **existing** key are not structural. `Iterator.remove()` after `next()` is the specified exception [[How do you remove an element from a collection while iterating]].

`CopyOnWriteArrayList` iterators are a snapshot and never throw CME; iterator `remove` is unsupported. `ConcurrentHashMap` iterators are **weakly consistent**: they do not throw CME and reflect some state at or since creation (not a COW array copy). They are for **one thread** at a time. Dump “fail-safe = snapshot” mixes those two [[What is the difference between fail-fast and fail-safe iterators]], [[Are ConcurrentHashMap iterators fail-fast]].

```d2
direction: down
t: "one thread" {
  width: 200
  height: 45
}
fe: "for (E e : list)" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
rm: "list.remove(e)" {
  width: 200
  height: 50
  style.fill: "#ffebee"
}
cme: "next() → CME" {
  width: 200
  height: 50
  style.fill: "#ffebee"
}

t -> fe -> rm -> cme
```

**Fig. 1.** No second thread. The iterator sees a structural change it did not make.

```java
class SingleThreadCme {
    static void classic(java.util.List<String> list) {
        for (String s : list) {
            if (s.isEmpty()) {
                list.remove(s); // typically CME on the next iterator step
            }
        }
    }

    static void allowed(java.util.List<String> list) {
        java.util.Iterator<String> it = list.iterator();
        while (it.hasNext()) {
            if (it.next().isEmpty()) {
                it.remove();
            }
        }
    }
}
```

**Listing 1.** `classic` is the interview one-thread case. `allowed` uses the iterator’s own `remove`. `list.removeIf(String::isEmpty)` is the same idea.

> [!warning] The name is not a thread count
> One thread that breaks the iterator contract is enough. Two threads without a fail-fast iterator (or with a concurrent map) may **not** get CME. Do not diagnose “we must have a race” from this exception alone.

> [!warning] CHM / COW are not “fail-fast with a try/catch”
> They do not throw CME. Weakly consistent ≠ snapshot. Catching CME on `ArrayList` does not make the loop safe.

> [!tip] Interview answer
> **One thread: enhanced `for` (or any fail-fast iterator) plus `list.remove` / `add` — CME on a later `next()`.** The name does not require two threads. Use `Iterator.remove()` or `removeIf`. ConcurrentHashMap and CopyOnWriteArrayList iterators do not throw CME.
