<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #Java/Collections/Map/ConcurrentHashMap #Java/Versions/5 #Java/Collections/Concurrency #SRS

# Why is `ConcurrentHashMap` faster than `Hashtable`?

> [!abstract] Short answer
> **Because `Hashtable` takes one monitor on the whole table for almost every public call, including `get`, while `ConcurrentHashMap` does not.** Retrievals overlap with updates; writers contend per bin (Java 8) or per stripe (Java 7), not on `this`. The `Hashtable` page itself sends highly concurrent code to `ConcurrentHashMap`. That is a contention story, not a “always fewer CPU cycles on one thread” guarantee.

## One lock versus concurrent retrievals

`Hashtable` is **synchronized** (since 1.0). `get`, `put`, `remove`, `size`, even `equals` / `hashCode` are `synchronized` methods — they lock the **same** object. Two threads looking up different keys still queue. The class has buckets for collisions like any hash table; “multiple buckets” is not the CHM advantage.

`ConcurrentHashMap` (1.5) is thread-safe **without** that protocol: retrievals do not entail locking, and there is no way to lock the entire table ([[Does ConcurrentHashMap get lock the whole table]]). `get` is volatile/acquire reads. Java 8 `put` CASes an empty bin or `synchronized`s the bin head ([[How does ConcurrentHashMap use CAS and synchronized in Java 8]]). Independent keys proceed together; readers do not wait for a table-wide `put`.

The JDK recommendation is explicit: not thread-safe → `HashMap`; thread-safe and **highly concurrent** → `ConcurrentHashMap` instead of `Hashtable` ([[How would you explain drawbacks of the legacy Hashtable class]]). Versus `HashMap` (nulls, fail-fast, unsynchronized): [[What is the difference between HashMap and ConcurrentHashMap]]. Pairwise Hashtable/CHM: [[How does Hashtable differ from ConcurrentHashMap]].

```d2
direction: right
ht: "Hashtable.get / put\nsynchronized(this)\nall keys, even reads" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
chm: "ConcurrentHashMap\nget: no lock\nput: bin or old Segment" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
ht -> chm: "less exclusion"
```

**Fig. 1.** Speed under sharing is who you exclude. Both types already use a bucket array.

```java
import java.util.Hashtable;
import java.util.concurrent.ConcurrentHashMap;

class Demo {
    static void contrast() {
        Hashtable<String, Integer> ht = new Hashtable<>();
        ht.put("a", 1);
        ht.get("a"); // synchronized on ht

        ConcurrentHashMap<String, Integer> chm = new ConcurrentHashMap<>();
        chm.put("a", 1);
        chm.get("a"); // no table lock; overlaps other puts
    }
}
```

**Listing 1.** Same call shape. Only `Hashtable` serializes the lookup with every other method on that instance.

Neither map allows null keys or values ([[Does ConcurrentHashMap allow null keys or values]]). Versions: `Hashtable` 1.0, `ConcurrentHashMap` 1.5 ([[In which Java version was ConcurrentHashMap introduced]]).

> [!warning] “Faster” is not uncontended single-thread law
> Official text does not publish a benchmark. A lone thread on a small `Hashtable` can be fine. The win shows up when **many threads** read and write: CHM does not make independent `get`s wait for `put`. `Hashtable` is still thread-safe — that is not a reason to keep it for a hot concurrent map.

> [!warning] Buckets are not the CHM trick
> `Hashtable` javadoc already describes capacity as the number of **buckets**. CHM is not “the hash table that has more than one bucket.” The dump’s “avoids read locks” is the real difference. Java 8 writes still lock a **bin**, not nothing.

> [!tip] Interview answer
> **`Hashtable.get` is `synchronized` on the map, so even independent reads contend. `ConcurrentHashMap.get` does not lock; updates lock a bin (or, in Java 7, a segment), not the whole table.** Both are thread-safe. The JDK tells you to use `ConcurrentHashMap` when you actually need concurrent access. That is why people say it is faster under load — not because it has “more buckets.”
