<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Java/Collections/Concurrency #SRS

# Is `LinkedHashMap` synchronized?

> [!abstract] Short answer
> **No.** The implementation is not synchronized. Concurrent access plus a structural modify needs an external lock or `Collections.synchronizedMap` wrapped at creation. Insertion-order `get` is not structural. **Access-order `get` is** — it moves the entry, so “we only read” is still a race.

## Structural modify is wider than `HashMap`

`LinkedHashMap` extends `HashMap` and keeps a doubly-linked list for encounter order (insertion-order by default; access-order via the three-arg constructor). Since 1.4. It is **not** synchronized. If several threads use the map and at least one modifies it structurally, synchronize externally — typically on an encapsulating object, or wrap at creation so nothing else keeps a raw reference. [[Does LinkedHashMap extend HashMap]] [[Is java.util.HashMap thread safe]]

A structural modification is any add or delete of mappings, **or**, on an access-ordered map, anything that **affects iteration order**. Insertion-order: replacing the value of a key already in the map is not structural. Access-order: **querying with `get` is structural.** `put`, `putIfAbsent`, `getOrDefault`, `compute*`, and `merge` also count as accesses when the entry exists. That is why an LRU `LinkedHashMap` cannot be shared with unsynchronized `get`. [[What are LinkedHashMap ordering guarantees]] [[How do you build a cache with invalidation using LinkedHashMap]]

```java
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;

class Demo {
    static void wrap() {
        Map<String, Integer> insertion =
                Collections.synchronizedMap(new LinkedHashMap<>());
        insertion.put("a", 1);

        Map<String, Integer> access =
                Collections.synchronizedMap(new LinkedHashMap<>(16, 0.75f, true));
        access.put("a", 1);
        access.get("a"); // structural: moves the node; must go through the wrapper

        synchronized (access) {
            Iterator<String> i = access.keySet().iterator();
            while (i.hasNext()) {
                i.next();
            }
        }
    }
}
```

**Listing 1.** Official wrap, at creation. The `true` flag is access-order. Wrapper methods lock the returned map. **Iteration does not** — `synchronized (access)` is required for `Iterator` / `Spliterator` / `Stream`.

```d2
direction: down
q: "Shared LinkedHashMap?" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
ins: "insertion-order\nget is not structural" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
acc: "access-order / LRU\nget IS structural" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
wrap: "Collections.synchronizedMap\nor encapsulating lock" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

q -> ins
q -> acc
ins -> wrap: still lock writers
acc -> wrap: lock get too
```

**Fig. 1.** “Non-synchronized” is the class. Access-order additionally treats `get` as a write to the list.

Fail-fast view iterators throw `ConcurrentModificationException` after a structural change, except via that iterator’s `remove`. Best-effort only; not a lock. `ConcurrentHashMap` is a concurrent hash table (no linked encounter order, no LRU `removeEldestEntry`, no nulls). Wrapping keeps `LinkedHashMap` order and one mutex. It does not become CHM.

> [!warning] “I only `get`” is false on an LRU map
> Default `new LinkedHashMap<>()` is insertion-order: concurrent `get` with no structural writer is the same story as `HashMap` (still undefined if anyone `put`s). `new LinkedHashMap<>(n, f, true)` makes `get` reorder the list. Two threads calling `get` without a lock race on the links. `Collections.synchronizedMap` does not lock a `for-each` unless you wrap the loop in `synchronized (m)`.

> [!tip] Interview answer
> **No — `LinkedHashMap` is not synchronized; wrap with `Collections.synchronizedMap` at creation or lock externally.** Insertion-order `get` is not a structural modify; access-order `get` is, so an LRU cache cannot be “read-only shared.” Fail-fast iterators are a bug detector, not a memory model. There is no concurrent `LinkedHashMap` in the JDK.
