<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency/CopyOnWrite #Java/Collections/Set #SRS

# What is `CopyOnWriteArraySet`?

> [!abstract] Short answer
> **A thread-safe `Set` that delegates every operation to an internal `CopyOnWriteArrayList` (Java 1.5).** Membership is `Objects.equals` on an array — there is **no hash table**. Writes copy the whole array. Iterators are snapshots: no extra locking to walk, no `ConcurrentModificationException`, and they do not support `remove`. Fit is a **small**, **read-mostly** set.

## Array set, copy on write

`public class CopyOnWriteArraySet<E> extends AbstractSet<E> implements Serializable`. The class javadoc: it uses an internal `CopyOnWriteArrayList` for **all** of its operations, so it inherits that list’s costs ([[What is the difference between CopyOnWriteArrayList and ArrayList]]).

Mutative operations (`add`, `remove`, …) are **expensive** because they usually **copy the entire underlying array**. `contains` / `add` uniqueness is `Objects.equals` — a scan, not `hashCode`. Treat it as linear membership, not as `HashSet` ([[What is a HashSet]]).

Iterators (and the `Spliterator`) snapshot the array at construction. Traversal is fast and cannot be interfered with by other threads; **no synchronization** is needed while walking. The iterator does **not** support `remove` (`UnsupportedOperationException`). Encounter order is **insertion order**. The spliterator reports `IMMUTABLE`, `DISTINCT`, `SIZED`, `SUBSIZED`.

```d2
direction: down
api: "Set — unique, equals membership" {
  width: 300
  height: 60
  style.fill: "#e3f2fd"
}
impl: "CopyOnWriteArrayList\narray; write → fresh copy" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
walk: "iterator / spliterator\nsnapshot of that array" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

api -> impl
impl -> walk
```

**Fig. 1.** Readers hold the array that was current when the iterator was created. Later `add` publishes a new array; old walks keep going.

```java
Set<String> handlers = new CopyOnWriteArraySet<>();
handlers.add("a"); // scan for equals, then copy the array if it is new
handlers.add("a"); // false; still one element

for (String h : handlers) {
    // snapshot — another thread's add is not visible here
}
```

**Listing 1.** Duplicate `add` is rejected by `equals`, then no copy is needed if the set did not change. The enhanced-for uses the snapshot iterator.

Official use: set sizes **generally stay small**, **read-only operations vastly outnumber** mutative ones, and you need to prevent interference during traversal. The javadoc sketch is a set of handlers invoked after a state change — iterate without locking writers out.

## What this is not

For a large or write-heavy concurrent set, `ConcurrentHashMap.newKeySet()` ([[How do you get a concurrent Set in Java]]). For sorted concurrent ranges, `ConcurrentSkipListSet` ([[What is ConcurrentSkipListSet]]). `Collections.synchronizedSet(new HashSet<>())` is one mutex, not copy-on-write.

The internal list **permits `null`**. `CopyOnWriteArraySet` uniqueness is still `equals`, so at most one `null` — unlike `ConcurrentHashMap.newKeySet()`, which forbids null.

> [!warning] `contains` is not hash `O(1)`
> Every `add` / `contains` walks the array with `equals`. A “handful of subscribers” is the documented shape. A large write-heavy `CopyOnWriteArraySet` copies the array on every successful mutation and still scans on every membership test.

> [!warning] Snapshot iterators do not throw `ConcurrentModificationException`
> They also **never see** later adds. `iterator.remove()` is unsupported — it throws `UnsupportedOperationException`, it does not mutate the set. “Never throws” is wrong; mutator methods on the iterator do throw.

> [!tip] Interview answer
> **`CopyOnWriteArraySet` is a `Set` on a `CopyOnWriteArrayList`: unique elements by `equals` in an array, copy the array on write, snapshot iterators (Java 5).** Use it only when the set stays small and reads dwarf writes. For a concurrent hash set use `newKeySet()`; for a concurrent sorted set use `ConcurrentSkipListSet`.
