<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Map/Hashtable #Java/Collections/Map/ConcurrentHashMap #SRS

# How does `Hashtable` differ from `ConcurrentHashMap`?

> [!abstract] Short answer
> **Both are thread-safe maps that reject `null` keys and values; `Hashtable` locks the whole table on every call, `ConcurrentHashMap` does not.** Retrievals on the concurrent map do not lock. There is no way to exclusive-lock that map. `Hashtable` itself recommends `ConcurrentHashMap` when you want a highly concurrent implementation.

## One monitor versus concurrent retrievals

`Hashtable` is a synchronized `Map` (and a legacy `Dictionary`). Each method acquires the table’s own lock, so readers block writers and each other. You can also `synchronized (theHashtable)` around several calls and know no other `Hashtable` method runs in between. Collection-view iterators are fail-fast; the old `keys()` / `elements()` enumerations are not. [[Can you unsynchronize a Hashtable]] [[Are Hashtable enumerations fail-fast]] [[Does Hashtable allow null keys or values]]

`ConcurrentHashMap` is written to the same functional `Map` spec as `Hashtable` — including **no `null` key or value**, unlike `HashMap`. It is the highly concurrent replacement: full concurrency of retrievals, overlapping updates, no lock that freezes the entire table. Iterators are weakly consistent and do not throw `ConcurrentModificationException`. Use `putIfAbsent` / `compute` for compound updates; do not try to lock the map. [[Does ConcurrentHashMap get lock the whole table]] [[Does ConcurrentHashMap allow null keys or values]] [[Are ConcurrentHashMap iterators fail-fast]] [[Why is ConcurrentHashMap faster than Hashtable]]

Programs that only needed “a thread-safe hash map” can switch. Programs that depended on **one lock for the whole table** cannot treat them as interchangeable. [[Why use concurrent collections instead of Collections synchronized wrappers]]

```java
Hashtable<String, Integer> table = new Hashtable<>();
table.put("a", 1);
// table.put(null, 1);              // NullPointerException

ConcurrentHashMap<String, Integer> chm = new ConcurrentHashMap<>();
chm.put("a", 1);
// chm.put("b", null);              // NullPointerException — same null rule
Integer v = chm.get("a");           // retrieval does not lock the table
```

**Listing 1.** Same null policy. Different locking.

```java
synchronized (table) {
    if (!table.containsKey("a")) {
        table.put("a", 1);          // exclusive on the whole Hashtable
    }
}

chm.putIfAbsent("a", 1);            // no equivalent of locking the entire CHM
```

**Listing 2.** `Hashtable` still has a single client-visible lock. `ConcurrentHashMap` does not.

```d2
direction: right
Hashtable: {
  lock: one monitor
  t1: get
  t2: put
  t1 -> lock
  t2 -> lock
}
CHM: {
  map: ConcurrentHashMap
  t3: get
  t4: put
  t3 -> map: no table lock
  t4 -> map
}
```

**Fig. 1.** `Hashtable`: every call takes the same lock. `ConcurrentHashMap`: retrievals do not lock the table; you cannot freeze it.

> [!warning] Neither is `HashMap`, and they are not drop-in for locking
> Both throw on `null` keys and values — that is not a `Hashtable`-only rule. `ConcurrentHashMap` is not a faster `Hashtable` with the same single lock: you cannot `synchronized (chm)` to make a multi-step update exclusive. If you needed that monitor, keep a wrapper or redesign around `putIfAbsent` / `compute`.

> [!tip] Interview answer
> **`Hashtable` synchronizes every method on the whole table; `ConcurrentHashMap` is the concurrent replacement for that thread-safe map spec.** Gets do not lock the concurrent map, and you cannot lock the entire table. Neither allows nulls. Reach for `ConcurrentHashMap` unless you depend on `Hashtable`’s single-lock behavior.
