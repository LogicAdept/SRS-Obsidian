<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #Java/Collections/Map/HashMap #Java/Collections/Concurrency #SRS

# Can you unsynchronize a `Hashtable`?

> [!abstract] Short answer
> **No.** `Hashtable` has no unsynchronized mode and no factory that strips its monitors. Public table methods are `synchronized` on the instance. For a map without that lock, use `HashMap`. For thread safety without a whole-table monitor, use `ConcurrentHashMap`. `Collections.synchronizedMap` wraps an unsynchronized map — the opposite direction.

## Synchronization is built into the type

As of Java 2, `Hashtable` implements `Map`. Unlike the collections added with that framework, it **is synchronized**. The class page’s replacements are explicit: no thread safety → `HashMap`; highly concurrent thread safety → `ConcurrentHashMap`. There is no constructor flag, no `setSynchronized(false)`, and no `Collections.unsynchronizedMap`. Synchronization is optional for `HashMap` (wrap only if you need a lock) and mandatory for `Hashtable`: a single-threaded caller still takes the monitor. [[What is the difference between HashMap and Hashtable]]

`get`, `put`, `remove`, `size`, `clear`, `containsKey`, and the Java 8 map defaults (`putIfAbsent`, `compute*`, `merge`, …) are `public synchronized` methods. The bucket array is a private field, so a subclass cannot reimplement those operations without calling the still-synchronized super methods.

```text
Hashtable          — synchronized methods on this; no off switch
HashMap            — not synchronized; null key/values allowed
Collections.synchronizedMap(new HashMap<>(...))
                   — add a wrapper lock (wrap at creation)
ConcurrentHashMap  — thread-safe; retrievals do not lock the table
```

**Listing 1.** Four answers to “I have a hash table and I care about monitors.” `Hashtable` is only the first row.

```d2
direction: down
ht: "Hashtable\nmonitors on the class" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
hm: "HashMap\nno lock" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
wrap: "Collections.synchronizedMap\nlock around HashMap" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
chm: "ConcurrentHashMap\nconcurrent; get does not lock the table" {
  width: 340
  height: 70
  style.fill: "#ffe0b2"
}

ht -> hm: "need no monitor"
ht -> wrap: "need one mutex, modern map"
ht -> chm: "need concurrent writers"
```

**Fig. 1.** You do not unsynchronize `Hashtable`. You pick a different map.

`HashMap` is “roughly equivalent to `Hashtable`, except that it is unsynchronized and permits nulls.” Its documented wrap is `Collections.synchronizedMap(new HashMap<>(...))`, done at creation so nothing else keeps a raw `HashMap` reference. Iteration on that wrapper still needs `synchronized (m)` around the iterator. [[Is java.util.HashMap thread safe]]

```java
import java.util.Collections;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Map;

class Demo {
    static void contrast() {
        Hashtable<String, Integer> ht = new Hashtable<>();
        ht.put("a", 1);
        ht.get("a"); // synchronized on ht; cannot turn that off

        Map<String, Integer> copy = new HashMap<>(ht); // new map, snapshot
        copy.get("a"); // not synchronized

        Map<String, Integer> locked =
                Collections.synchronizedMap(new HashMap<>(ht));
        locked.put("b", 2); // wrapper lock; backing HashMap has none
    }
}
```

**Listing 2.** A `HashMap` copy and a synchronized wrapper are different objects. The original `Hashtable` stays synchronized.

`ConcurrentHashMap` obeys the same functional spec as `Hashtable` (including no nulls) but retrievals do not entail locking the whole table, and you cannot freeze all access with one monitor. That is the concurrent replacement, not an unsync switch. [[Why is ConcurrentHashMap faster than Hashtable]] [[How would you explain drawbacks of the legacy Hashtable class]]

> [!warning] `synchronizedMap` does not unsynchronize `Hashtable`
> `Collections.synchronizedMap` adds a mutex around a backing map. Wrap a `Hashtable` and every `get`/`put` still takes `Hashtable`’s own monitor, then the wrapper’s. `Collections.unmodifiableMap` only rejects writes; read-through still locks. There is no `unsynchronizedMap`. `new HashMap<>(ht)` is a **copy**: later `ht.put` does not appear in the `HashMap`, and the live `Hashtable` is still fully synchronized.

> [!tip] Interview answer
> **No — `Hashtable` is synchronized in the class, and there is no unsynchronized mode.** If you do not need a monitor, use `HashMap`. If you need threads without locking the whole table, use `ConcurrentHashMap`. `Collections.synchronizedMap` is how you **add** a lock to `HashMap`, not how you strip one from `Hashtable`.
