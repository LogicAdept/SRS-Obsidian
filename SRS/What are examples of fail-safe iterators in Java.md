<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration/FailFast #Java/Collections/Concurrency #SRS

# What are examples of fail-safe iterators in Java?

> [!abstract] Short answer
> **Interview “fail-safe” examples: `CopyOnWriteArrayList.iterator()` and `ConcurrentHashMap` view iterators (`keySet()`, also `values()` / `entrySet()`).** The JRE does **not** use the word fail-safe. COW is a **snapshot** (never CME; iterator `remove` is UOE). CHM is **weakly consistent** (no CME; may see later writes; one thread per iterator). Neither is fail-fast `ArrayList`.

## Snapshot vs weakly consistent

Interview tables often call any iterator that does **not** throw `ConcurrentModificationException` “fail-safe.” Official text splits that bucket [[What is the difference between fail-fast and fail-safe iterators]], [[What is ConcurrentModificationException]].

**`CopyOnWriteArrayList`:** the iterator holds a reference to the array at creation. That array does not change for the iterator’s life, so interference is impossible and CME is **guaranteed** not to be thrown. Later `add`/`remove` on the list are invisible to this walk. Iterator `remove` / `set` / `add` throw `UnsupportedOperationException` [[How do you avoid ConcurrentModificationException while iterating a collection]].

**`ConcurrentHashMap`:** iterators, spliterators, and enumerations reflect the table at some point **at or since** creation. They **do not throw CME**. Views: `keySet()` / `values()` / `entrySet()` iterators are weakly consistent. Designed for **one thread** at a time. This is not a COW array copy [[Are ConcurrentHashMap iterators fail-fast]].

Same weakly consistent idea: `ConcurrentLinkedDeque.iterator()` / `descendingIterator()`. Not a snapshot.

**Not examples:** `ArrayList` / `HashMap` iterators (fail-fast). `Hashtable.keys()` / `Vector.elements()` (not fail-fast; results **undefined** — not a snapshot). `ListIterator` on `ArrayList` is still fail-fast.

```d2
direction: down
label: "no-CME iterators" {
  width: 220
  height: 50
}
cow: "CopyOnWriteArrayList\nsnapshot array\nno CME" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
chm: "ConcurrentHashMap views\nweakly consistent\nno CME" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}

label -> cow
label -> chm
```

**Fig. 1.** Two interview names, two contracts. Both skip CME; only COW freezes the element array.

```java
class FailSafeStyleIterators {
    static int cowSizeSeen() {
        java.util.concurrent.CopyOnWriteArrayList<Integer> list =
                new java.util.concurrent.CopyOnWriteArrayList<>();
        list.add(1);
        int n = 0;
        for (Integer ignored : list) {
            list.add(2);
            n++;
        }
        return n; // 1 — snapshot, not the live list
    }

    static void chmKeys() {
        java.util.concurrent.ConcurrentHashMap<String, Integer> map =
                new java.util.concurrent.ConcurrentHashMap<>();
        map.put("a", 1);
        for (String k : map.keySet()) {
            map.put("b", 2); // no CME; may or may not see "b" on this iterator
        }
    }
}
```

**Listing 1.** COW for-each plus `add` does not throw and does not see `2` on that pass (`n == 1`). CHM `keySet()` for-each plus `put` does not throw; `"b"` may appear on the same iterator. Do not call `iterator.remove()` on COW. Do not share one CHM iterator across threads.

> [!warning] “Fail-safe” is not a JRE interface
> You will not find `FailSafeIterator`. Say **snapshot** (COW) or **weakly consistent** (CHM). Treating them as the same “copy” is the usual mix-up.

> [!warning] Hashtable `keys()` is not a third example
> It also skips CME, but the spec says results are **undefined** after a structural change. That is not copy-on-write and not weakly consistent CHM. `hasNext` looking fine after a fail-fast write is a different story.

> [!tip] Interview answer
> **CopyOnWriteArrayList iterators and ConcurrentHashMap `keySet()` iterators — they do not throw `ConcurrentModificationException`.** COW walks a snapshot; CHM is weakly consistent and may see later puts. Official docs never call them fail-safe. ArrayList is the fail-fast contrast.
