<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration/FailFast #Java/Collections/Concurrency #SRS

# What happens to an iterator if the backing collection is modified externally?

> [!abstract] Short answer
> **Depends on the iterator contract.** Fail-fast (`ArrayList`, `HashMap` views): behavior is unspecified except this iterator’s `remove`; the JRE typically throws `ConcurrentModificationException` on a later `next()` / iterator `remove()`. Snapshot (`CopyOnWriteArrayList`): no CME; the walk still sees the array from creation. Weakly consistent (`ConcurrentHashMap`): no CME; may observe later completed writes. “External” means not through **this** iterator’s `remove`.

## Unspecified, CME, snapshot, or weakly consistent

`Iterator.remove` javadoc: behavior is unspecified if the underlying collection is modified while iteration is in progress **in any way other than this method**, unless the class documents a concurrent-modification policy [[How do you already iterator for collection if invoke collection.remove]].

**Fail-fast** (general-purpose JRE collections): if the collection is structurally modified after the iterator is created, except that iterator’s `remove` (list-iterator `add`), the iterator throws `ConcurrentModificationException`. One thread is enough (`coll.add` / `coll.remove` while `it` is live). Best-effort: `ArrayList.hasNext` does not check `modCount`, so CME usually appears on `next()`, and some writes skip the tail with no throw [[What is ConcurrentModificationException]], [[How can a single-threaded program get ConcurrentModificationException]], [[What counts as a structural modification for fail-fast iterators]].

Non-structural writes are not this story: `List.set`, `HashMap.put` of an **existing** key.

**Snapshot:** `CopyOnWriteArrayList` iterators never throw CME; they do not see later `add`/`remove` on the list. Iterator `remove` is UOE [[What are examples of fail-safe iterators in Java]].

**Weakly consistent:** `ConcurrentHashMap` view iterators do not throw CME and reflect some state at or since creation; later `put`s may appear. One thread per iterator [[Are ConcurrentHashMap iterators fail-fast]].

**Undefined, not CME:** `Hashtable.keys()` / `Vector.elements()` if structurally modified — not fail-fast, not a snapshot.

```d2
direction: down
ext: "coll.add / coll.remove\nwhile it is live" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
ff: "fail-fast\n→ CME on next()" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
snap: "COW snapshot\n→ no CME, old array" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
wk: "CHM weakly consistent\n→ no CME, may see writes" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}

ext -> ff
ext -> snap
ext -> wk
```

**Fig. 1.** Same external write, three documented outcomes. `it.remove()` is not external.

```java
class ExternalModify {
    static void failFast(java.util.List<String> list) {
        java.util.Iterator<String> it = list.iterator();
        list.add("x");
        it.next(); // typically ConcurrentModificationException
    }

    static void snapshot(java.util.concurrent.CopyOnWriteArrayList<String> list) {
        java.util.Iterator<String> it = list.iterator();
        list.add("x");
        it.next(); // no CME; "x" not in this iterator's array
    }
}
```

**Listing 1.** `failFast` is the `ArrayList` story. `snapshot` is COW. `list.add` is external; `it.remove()` after `it.next()` would not be.

> [!warning] External includes this thread
> “Concurrent” in CME is not a thread count. `list.remove` from the same thread that created `it` is still external to that iterator.

> [!warning] `hasNext` can lie after a fail-fast write
> On `ArrayList`, `hasNext` is `cursor != size` with no `modCount` check. A later `next()` throws — or the loop ends with a skipped tail and no CME. Do not treat “no exception yet” as “the iterator is still valid.”

> [!tip] Interview answer
> **Fail-fast iterators throw `ConcurrentModificationException` (usually on `next()`) if the collection is structurally changed except via that iterator’s `remove`.** CopyOnWriteArrayList keeps a snapshot and never throws CME. ConcurrentHashMap iterators are weakly consistent: no CME, later writes may show up. Same-thread `coll.remove` counts as external.
