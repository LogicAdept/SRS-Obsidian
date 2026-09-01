<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration/FailFast #Java/Collections/Concurrency #SRS

# How do you avoid `ConcurrentModificationException` while iterating a collection?

> [!abstract] Short answer
> **Mutate only through the iterator that is walking, or do not mutate that fail-fast collection during the walk.** Use `Iterator.remove()` after `next()`, or `Collection.removeIf` (default: same thing). Or iterate a **copy** and change the original (or the reverse). Or use a collection whose iterators are not fail-fast (`ConcurrentHashMap` weakly consistent; `CopyOnWriteArrayList` snapshot). Do not catch CME as the strategy.

## Change the mutator, the collection, or the timing

Fail-fast iterators (`ArrayList`, `HashMap` views, …) throw `ConcurrentModificationException` if the collection is structurally modified after the iterator is created, except through **that** iterator’s `remove` (and list-iterator `add`). Enhanced `for` hides the iterator, so `coll.remove` / `add` in the body is the usual one-thread CME [[What is ConcurrentModificationException]], [[Can you modify a collection while iterating with a for-each loop]].

**Allowed in-walk delete (fail-fast):** keep `Iterator` in source and call `remove()` once after `next()`. `removeIf(Predicate)` (Java 8) walks `iterator()` and uses `Iterator.remove()`. `ListIterator` may `add` / `set` / `remove` under its own rules [[How do you remove an element from a collection while iterating]].

**After the walk:** gather keys/elements to drop, then `remove` / `removeAll` when no fail-fast iterator is live. Or `new ArrayList<>(coll)` and iterate the copy while mutating `coll` (the copy’s iterator does not see original `modCount`).

**Different iterator contract:** `ConcurrentHashMap` iterators do **not** throw CME (weakly consistent; one thread per iterator). `CopyOnWriteArrayList` uses a snapshot and never throws CME; its iterator `remove` / `set` / `add` throw `UnsupportedOperationException` — mutate the **list**, not the iterator [[Are ConcurrentHashMap iterators fail-fast]], [[How can a single-threaded program get ConcurrentModificationException]].

Fail-fast is **best-effort**. Programs must not depend on catching CME for correctness.

```d2
direction: down
walk: "iterating a fail-fast collection" {
  width: 300
  height: 55
}
own: "iterator.remove / removeIf" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
copy: "iterate a copy\nor mutate after" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
conc: "CHM / COW iterators\nno CME" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}

walk -> own
walk -> copy
walk -> conc
```

**Fig. 1.** Avoidance is a legal mutator, a second collection, or a non-fail-fast iterator — not `try/catch`.

```java
class AvoidCme {
    static void removeInWalk(java.util.Collection<String> coll) {
        coll.removeIf(String::isEmpty);
    }

    static void iteratorRemove(java.util.Collection<String> coll) {
        java.util.Iterator<String> it = coll.iterator();
        while (it.hasNext()) {
            if (it.next().isEmpty()) {
                it.remove();
            }
        }
    }

    static void mutateOriginalWhileWalkingCopy(java.util.List<String> list) {
        for (String s : new java.util.ArrayList<>(list)) {
            if (s.isEmpty()) {
                list.remove(s);
            }
        }
    }
}
```

**Listing 1.** `removeIf` / `Iterator.remove` stay on the fail-fast list. The copy loop’s iterator belongs to the snapshot `ArrayList`, so `list.remove` does not invalidate it.

> [!warning] Catching CME is not avoidance
> Fail-fast is a bug detector. The collection may already be a bad state for this walk. Change how you mutate. Concurrent maps are not “ArrayList plus try/catch.”

> [!warning] COW `iterator.remove` is not the ArrayList pattern
> Snapshot iterators reject `remove` with `UnsupportedOperationException`. `list.remove` during for-each does not throw CME and does not change the remaining snapshot. Weakly consistent CHM iterators may see later puts; they are not a frozen copy.

> [!tip] Interview answer
> **Use `Iterator.remove()` or `removeIf`, or iterate a copy, or a concurrent/snapshot collection.** For-each plus `coll.remove` is the classic CME, even on one thread. Do not rely on catching the exception.
