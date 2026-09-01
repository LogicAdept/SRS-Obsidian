<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Concurrency #SRS

# What is the difference between `TreeMap` and `ConcurrentSkipListMap`?

> [!abstract] Short answer
> Both are **sorted `NavigableMap`s** (natural order or a constructor `Comparator`, expected log(n) `get`/`put`). `TreeMap` is a **red-black tree**, **not synchronized**, with **fail-fast** iterators. `ConcurrentSkipListMap` is a **concurrent skip list**: many threads may mutate it together, iterators are **weakly consistent**, and **null keys and null values are forbidden**. For shared sorted maps, prefer the skip list over `synchronizedSortedMap(new TreeMap<>())`.

## Same ordered API, different concurrency model

`TreeMap` (`java.util`, `Since: 1.2`) implements `NavigableMap`. `ConcurrentSkipListMap` (`java.util.concurrent`, `Since: 1.6`) implements `ConcurrentNavigableMap` (hence `ConcurrentMap` + `NavigableMap`). Order and neighbor/range methods are the same idea ([[How do you get a range or neighbor key from a TreeMap]], [[What interfaces does TreeMap implement]]).

`TreeMap` **guarantees** log(n) for `containsKey`/`get`/`put`/`remove`. The skip list documents **expected average** log(n); several threads may insert, remove, update, and read at once. That is **concurrent**, not a single monitor: “synchronized” wrappers exclude everyone else; concurrent maps do not ([[Why use concurrent collections instead of Collections synchronized wrappers]], [[How do you synchronize a TreeMap]]).

| | `TreeMap` | `ConcurrentSkipListMap` |
| --- | --- | --- |
| Structure | Red-black tree | Concurrent skip list |
| Threads | External lock or `Collections.synchronizedSortedMap` | Safe concurrent access |
| Iterators | Fail-fast; `ConcurrentModificationException` (best-effort) | Weakly consistent; no CME; may miss later writes |
| Null key | NPE unless a null-friendly comparator | Always forbidden |
| Null value | Allowed | Forbidden |
| Bulk `putAll` / `clear` / `equals` | Ordinary map ops under your lock | **Not** atomic vs concurrent readers |

Package `java.util.concurrent`: when many threads share a collection, prefer `ConcurrentSkipListMap` to a synchronized `TreeMap` (and `ConcurrentHashMap` to a synchronized `HashMap`). Unsynchronized `TreeMap` is the right default when the map is **not** shared.

```d2
direction: down
need: "shared sorted NavigableMap?" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
cslm: "ConcurrentSkipListMap\noverlapping ops" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
wrap: "synchronizedSortedMap\n(new TreeMap)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
solo: "plain TreeMap\none thread / outer lock" {
  width: 260
  height: 70
  style.fill: "#f3e5f5"
}
need -> cslm: "many threads"
need -> wrap: "need one lock for all access"
need -> solo: "unshared"
```

**Fig. 1.** Concurrent vs synchronized vs unshared. Weakly consistent iterators: traverse what existed at construction, never throw CME, may (not must) show later updates.

```java
import java.util.Collections;
import java.util.TreeMap;
import java.util.concurrent.ConcurrentSkipListMap;

class Demo {
    static void wrapperVsConcurrent() {
        var locked = Collections.synchronizedSortedMap(new TreeMap<Integer, String>());
        var concurrent = new ConcurrentSkipListMap<Integer, String>();
        concurrent.put(1, "a");
        // concurrent.put(2, null); // NullPointerException
        // locked may store null values; still wrap-and-lock for iteration
        synchronized (locked) {
            locked.put(1, "a");
        }
    }
}
```

**Listing 1.** Same sorted-map job. Skip list: no nulls, concurrent `put`. Wrapped `TreeMap`: one lock, null values OK ([[Can TreeMap have null keys or null values]]). Iterate the wrapper under that lock ([[Are TreeMap iterators fail-fast]]).

Skip-list `Map.Entry` objects from navigation methods are **snapshots** (`setValue` unsupported). Bulk methods (`putAll`, `clear`, `containsValue`, `equals`) can interleave with other threads. `compute*` on the skip list is **not** guaranteed once-only atomic.

> [!warning] Not “synchronized,” not “fail-safe”
> Dumps that say two threads cannot access a `ConcurrentSkipListMap` at the same time describe a **mutex**, which this class is not. Iterators are **weakly consistent**, not the magazine term “fail-safe.” They will not throw `ConcurrentModificationException`; they also will not freeze a transactional snapshot of the whole map.

> [!warning] Null values are not the same
> `TreeMap` may map keys to `null`. `ConcurrentSkipListMap` rejects **null keys and null values** so `get`’s null cannot mean “present.” Do not copy a “both allow many null values” table.

> [!tip] Interview answer
> **Both are sorted navigable maps with log(n) lookups. `TreeMap` is an unsynchronized red-black tree with fail-fast iterators; share it only behind a lock or `synchronizedSortedMap`. `ConcurrentSkipListMap` is a concurrent skip list from Java 6: overlapping reads and writes, weakly consistent iterators, no null keys or values. Prefer it over a synchronized `TreeMap` when many threads share the map — same idea as `ConcurrentHashMap` versus a synchronized `HashMap`.**
