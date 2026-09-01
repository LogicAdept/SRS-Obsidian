<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Concurrency #SRS

# How do you synchronize a `TreeMap`?

> [!abstract] Short answer
> `TreeMap` is **not synchronized**. If several threads share it and at least one **structurally** mutates it, lock an encapsulating object or wrap at creation with `Collections.synchronizedSortedMap` (or `synchronizedNavigableMap` when you still need `floorKey` / inclusive `subMap`). Do not treat `ConcurrentHashMap` as a sorted stand-in; the concurrent `NavigableMap` is `ConcurrentSkipListMap`.

## Not thread-safe; wrap or encapsulate

The class specification: concurrent access plus a structural modification (any add or delete of a mapping; replacing the value for an **existing** key is not structural) requires **external** synchronization. Typical pattern: synchronize on an object that already owns the map. If there is none, wrap **at creation** so no other reference sees the raw tree:

```java
import java.util.Collections;
import java.util.NavigableMap;
import java.util.SortedMap;
import java.util.TreeMap;
import java.util.concurrent.ConcurrentSkipListMap;

class Demo {
    static SortedMap<Integer, String> sortedWrapper() {
        return Collections.synchronizedSortedMap(new TreeMap<>());
    }

    static NavigableMap<Integer, String> navigableWrapper() {
        return Collections.synchronizedNavigableMap(new TreeMap<>());
    }

    static void iterate(SortedMap<Integer, String> m) {
        // lock the wrapper, not keySet() or a subMap view
        synchronized (m) {
            for (Integer k : m.keySet()) {
                m.get(k);
            }
        }
    }

    static NavigableMap<Integer, String> concurrentSorted() {
        return new ConcurrentSkipListMap<>();
    }
}
```

**Listing 1.** `synchronizedSortedMap` is the recipe in `TreeMap`'s class comment. `synchronizedNavigableMap` (Java 8) keeps neighbor and inclusive-range methods. `ConcurrentSkipListMap` (Java 6) is a concurrent sorted map, not a wrapper around `TreeMap`.

`Collections.synchronizedMap` is the same idea for a plain `Map` (`HashMap`, `LinkedHashMap`). For `TreeMap` the documented wrappers are the **sorted** / **navigable** ones so `subMap` / `headMap` / `tailMap` stay in the synchronized surface. `synchronizedNavigableMap` is the one to use if you still call `floorKey` / `ceilingKey` ([[How do you get a range or neighbor key from a TreeMap]]).

The wrapper is one mutex around every method. Concurrent maps allow overlapping operations; see [[Why use concurrent collections instead of Collections synchronized wrappers]] and [[What is the difference between TreeMap and ConcurrentSkipListMap]].

```d2
direction: down
raw: "new TreeMap<>()\nnot synchronized" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
wrap: "synchronizedSortedMap\nor synchronizedNavigableMap" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
iter: "synchronized (wrapper)\nthen iterate views" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
cslm: "or ConcurrentSkipListMap\nno TreeMap wrapper" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
raw -> wrap
wrap -> iter
raw -> cslm
```

**Fig. 1.** Either wrap the tree and iterate under that lock, or use a concurrent `NavigableMap`. Wrapping is [[How do you obtain synchronized wrappers for standard Java collections]].

> [!warning] Iterate under the wrapper lock
> The wrapper serializes `get`/`put`. **Iterators, spliterators, and streams on any view still need an explicit `synchronized (m)`** on the map the factory returned — not on `keySet()`, and not on `m.subMap(...)`. Skipping that is undefined. Fail-fast `ConcurrentModificationException` from a raw `TreeMap` is **best-effort** and is not a lock ([[Are TreeMap iterators fail-fast]]).

> [!warning] Wrap at creation; `ConcurrentHashMap` is not a sorted `TreeMap`
> Hold only the wrapped reference. A leftover unsynchronized `TreeMap` field defeats the wrapper. `ConcurrentHashMap` is a concurrent **hash** map: no key order, no `subMap`. For concurrent sorted keys use `ConcurrentSkipListMap` (no `null` keys or values).

> [!tip] Interview answer
> **`TreeMap` is not thread-safe. Wrap at construction with `Collections.synchronizedSortedMap` — or `synchronizedNavigableMap` if you need NavigableMap methods — and synchronize on that wrapper when iterating views. `ConcurrentHashMap` is not a drop-in; the concurrent sorted map is `ConcurrentSkipListMap`. Fail-fast CME is not your lock.**
