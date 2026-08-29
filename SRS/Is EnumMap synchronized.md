<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Collections/Concurrency #SRS

# Is `EnumMap` synchronized?

> [!abstract] Short answer
> **No.** Like most `java.util` collections, `EnumMap` is **not** synchronized. If several threads use one instance and **any** of them mutates it, you must synchronize externally — usually by wrapping at creation with `Collections.synchronizedMap`, or by locking an object that already owns the map.

## Unsynchronized array map

`EnumMap` (Java 5+) is a compact array-backed `Map` whose keys are all from one enum type. That layout is about density and constant-time ops, not concurrent writers. The class page states the same rule as `HashMap`: concurrent access plus a mutator requires external synchronization. Read-only sharing after the map is safely published is the case the “at least one thread modifies” clause leaves out. Why you pick this map at all: [[Why prefer EnumMap when the keys are enum constants]]. Contrast with a type that *is* synchronized: [[What is the difference between HashMap and Hashtable]].

```java
import java.util.Collections;
import java.util.EnumMap;
import java.util.Map;

public final class SyncedEnumMap {
    enum Color { RED, GREEN, BLUE }

    static Map<Color, Integer> create() {
        return Collections.synchronizedMap(new EnumMap<>(Color.class));
    }
}
```

**Listing 1.** Wrap **at construction** so no caller holds the raw `EnumMap`. All later access must go through `m`. This is one mutex on the wrapper, not `ConcurrentHashMap` concurrent writers.

```d2
direction: down
q: "Shared EnumMap?" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
single: "one thread\nor immutable after publish" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
wrap: "synchronizedMap\nor encapsulating lock" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
q -> single: "no mutator races"
q -> wrap: "any thread writes"
```

**Fig. 1.** The documented recipes are an encapsulating lock or `Collections.synchronizedMap`. `EnumMap` itself has no `synchronized` methods and is not a `java.util.concurrent` map.

View iterators are **weakly consistent**: they never throw `ConcurrentModificationException` and may or may not reflect updates that happen during iteration. That is not a substitute for a lock when a writer exists.

> [!warning] Wrap before anyone else sees the map
> `synchronizedMap` only serializes access **through the returned map**. A leftover reference to the inner `EnumMap` bypasses the lock. Create the wrapper immediately, as in Listing 1.

> [!warning] Iterate the wrapper under `synchronized (m)`
> `keySet` / `entrySet` / `values` traversal via `Iterator`, `Spliterator`, or `Stream` must lock on the **returned map**, not on the view. Skipping that lock is non-deterministic even after wrapping.

> [!tip] Interview answer
> No — `EnumMap` is not synchronized. For concurrent mutation, wrap it with `Collections.synchronizedMap` at creation, or lock the object that owns it. That is coarse external synchronization, not a concurrent map, and you must still synchronize on the wrapper when iterating its views.
