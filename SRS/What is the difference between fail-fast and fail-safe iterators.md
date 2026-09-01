<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration/FailFast #Java/Collections/Concurrency #SRS

# What is the difference between fail-fast and fail-safe iterators?

> [!abstract] Short answer
> **Fail-fast (`ArrayList`, `HashMap` views): `ConcurrentModificationException` if the collection is structurally changed except via that iterator’s `remove`.** So-called **fail-safe** is interview slang, not a JRE type. The real split is **snapshot** (`CopyOnWriteArrayList`: frozen array, never CME) vs **weakly consistent** (`ConcurrentHashMap`: no CME, may see later writes). Neither is “a clone of the whole collection.” Fail-fast is best-effort, not a lock.

## CME vs snapshot vs weakly consistent

**Fail-fast.** After the iterator is created, a structural `add`/`remove` (or ArrayList array resize) that is not this iterator’s `remove` (list-iterator `add`) typically throws `ConcurrentModificationException` on `next()` / iterator `remove()`. One thread is enough. `modCount` vs `expectedModCount`. Best-effort; do not catch for control flow [[What is fail-fast iterator behavior in Java collections]], [[What is ConcurrentModificationException]].

**Snapshot (COW).** `CopyOnWriteArrayList` iterators use a reference to the array **at creation**. That array does not change for the iterator’s life, so CME is guaranteed not to be thrown. Later list `add`/`remove` are invisible. Iterator `remove`/`set`/`add` throw `UnsupportedOperationException`. This is a snapshot of the **array**, not `clone()` of the `List` [[What are examples of fail-safe iterators in Java]].

**Weakly consistent (CHM).** View iterators do not throw CME. They reflect some state **at or since** creation; later completed `put`s may appear. One thread per iterator. **Not** a copy [[Are ConcurrentHashMap iterators fail-fast]].

Interview “fail-safe = clone, no exceptions” mixes COW (frozen array) with CHM (live table) and wrongly includes Hashtable `keys()` (undefined, not a copy) [[How do you avoid ConcurrentModificationException while iterating a collection]].

```d2
direction: down
write: "structural write during walk" {
  width: 280
  height: 55
}
ff: "fail-fast\nCME on next()" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
snap: "COW snapshot\nno CME, old array" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
wk: "CHM weakly consistent\nno CME, may see write" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}

write -> ff
write -> snap
write -> wk
```

**Fig. 1.** Same mutation, three contracts. Only fail-fast uses CME. Only COW ignores later writes by design.

```java
class FastVsNot {
    static void failFast(java.util.List<String> list) {
        for (String s : list) {
            list.add("x"); // typically CME
        }
    }

    static void snapshot(java.util.concurrent.CopyOnWriteArrayList<String> list) {
        for (String s : list) {
            list.add("x"); // no CME; this pass does not see "x"
        }
    }
}
```

**Listing 1.** Fail-fast vs snapshot. A `ConcurrentHashMap.keySet()` loop with `put` is the weakly consistent third case: no CME, `"x"` may show up.

> [!warning] There is no `FailSafeIterator`
> Official words are fail-fast, snapshot, and weakly consistent. “Works on a clone” is true only as a loose description of COW’s array snapshot — not CHM, not `Object.clone()`.

> [!warning] No CME is not always a copy
> Hashtable enumerations also skip CME and are **undefined** if mutated. Weakly consistent iterators can still observe concurrent updates. Fail-fast CME is not a happens-before barrier.

> [!tip] Interview answer
> **Fail-fast throws `ConcurrentModificationException` on structural change except `iterator.remove` (`ArrayList`, `HashMap`).** “Fail-safe” is slang: CopyOnWriteArrayList is a snapshot (no CME, frozen array); ConcurrentHashMap is weakly consistent (no CME, later puts may appear). They are not the same clone.
