<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Map/HashMap #Java/Versions/8 #Java/Collections/Concurrency #SRS

# What is the difference between `HashMap` and `ConcurrentHashMap`?

> [!abstract] Short answer
> **`HashMap` is an unsynchronized map that allows a null key and null values and fail-fast iterators.** **`ConcurrentHashMap` is thread-safe, forbids nulls, and has weakly consistent iterators that do not throw `ConcurrentModificationException`.** It is not a `synchronized HashMap`: retrievals do not lock the table, and there is no whole-map lock.

## Contract, not a speed table

`HashMap` (since 1.2) permits the null key and null values, is **not synchronized**, and must be wrapped (`Collections.synchronizedMap`) or guarded by an external lock if one thread mutates while others access it. Its view iterators are **fail-fast** (best-effort `ConcurrentModificationException`). `get` returning null is ambiguous: absent vs mapped to null ([[Can HashMap store a null key]]).

`ConcurrentHashMap` (since 1.5) matches `Hashtable`’s functional spec, not `HashMap`’s: **no null key or value** (`put` / `get(null)` → `NullPointerException`), so a null `get` means absent ([[Does ConcurrentHashMap allow null keys or values]]). All operations are thread-safe, but retrievals **do not entail locking** and the class has **no whole-table lock** ([[Does ConcurrentHashMap get lock the whole table]]). Iterators / spliterators are **weakly consistent**: they do not throw `ConcurrentModificationException` ([[Are ConcurrentHashMap iterators fail-fast]]). Interview “fail-safe” is not the JDK term.

```d2
direction: right
hm: "HashMap\nunsynchronized\nnull key + null values\nfail-fast iterators" {
  width: 260
  height: 110
  style.fill: "#fff8e1"
}
chm: "ConcurrentHashMap\nthread-safe, no table lock\nno nulls\nweakly consistent iterators" {
  width: 280
  height: 110
  style.fill: "#e8f5e9"
}
hm -> chm: "not a synchronized wrapper"
```

**Fig. 1.** Calling `ConcurrentHashMap` “synchronized” is the dump trap: it is concurrent, not one monitor on `this`.

Java 8 internals (not the `HashMap` API): occupied bins `synchronized` on the head node; empty bins CAS ([[How does ConcurrentHashMap use CAS and synchronized in Java 8]]). Java 7 used segment locks. `computeIfAbsent` on this map is one atomic invocation — `containsKey` then `put` is still a race ([[How do you avoid a check-then-act race on ConcurrentHashMap]]). `HashMap.computeIfAbsent` is the single-thread Map default: not a concurrent protocol, and it may best-effort throw `ConcurrentModificationException` if the function mutates the map.

Docs do **not** rank “HashMap always faster.” Uncontended `HashMap` has no publication protocol; `ConcurrentHashMap` pays for concurrent readers and writers. Use `HashMap` when the map is confined or already locked; use `ConcurrentHashMap` when many threads hit the map. `Collections.synchronizedMap(new HashMap<>(...))` is the HashMap page’s concurrent recipe — a single wrapper lock, not CHM’s retrieval concurrency.

```text
                 HashMap                         ConcurrentHashMap
Thread safety    not synchronized                thread-safe; get does not lock table
Nulls            null key + null values          neither; NPE
get == null      absent or stored null           absent
Iterators        fail-fast (best-effort CME)     weakly consistent; no CME
Compound updates external lock / not atomic      putIfAbsent / compute* / merge
Default size     16, load 0.75                   default table size 16
```

**Listing 1.** Spec differences. “Faster / slower” is not a class-page guarantee.

```java
import java.util.HashMap;
import java.util.concurrent.ConcurrentHashMap;

class Demo {
    static void contrast() {
        HashMap<String, Integer> h = new HashMap<>();
        h.put(null, 1);           // allowed
        h.put("a", null);         // allowed
        Integer x = h.get("a");   // null: stored null, not “missing”

        ConcurrentHashMap<String, Integer> c = new ConcurrentHashMap<>();
        c.put("a", 1);
        // c.put(null, 1);        // NullPointerException
        // c.put("b", null);      // NullPointerException
        Integer y = c.get("missing"); // null means absent
    }
}
```

**Listing 2.** Null policy is the interview tell. Concurrent structural `put` on a plain `HashMap` is a data race, not a `ConcurrentModificationException` you can rely on.

> [!warning] “Synchronized” is the wrong word for `ConcurrentHashMap`
> Tables that mark it synchronized next to `Hashtable` hide the spec: thread-safe **without** locking the entire table, and **without** making `get` take a monitor. `synchronized (concurrentHashMap)` is not a supported freeze. Per-call safety is not `get` then `put`.

> [!warning] “Fail-safe” and “always slower”
> Official iterator wording is **weakly consistent**, not fail-safe and not a full snapshot. Fail-fast on `HashMap` is best-effort and not for control flow. Do not pick the map from a “CHM is slower” slogan; pick it from sharing vs confinement.

> [!tip] Interview answer
> **`HashMap` is unsynchronized, allows nulls, and has fail-fast iterators. `ConcurrentHashMap` is thread-safe, bans nulls so `get == null` means absent, and iterates without `ConcurrentModificationException`.** It is not `synchronizedMap`. Java 8 `put` CASes empty bins and locks bin heads; `computeIfAbsent` is the atomic check-then-insert.
