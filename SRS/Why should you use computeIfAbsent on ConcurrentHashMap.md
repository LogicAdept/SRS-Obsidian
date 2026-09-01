<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Versions/8 #Java/Collections/Concurrency #SRS

# Why should you use `computeIfAbsent` on `ConcurrentHashMap`?

> [!abstract] Short answer
> **It is the atomic “if absent, create and install” for a shared map.** `containsKey` then `put` (or `get` then `put`) races even though each call is thread-safe. `computeIfAbsent` (Java 8) runs that check-and-insert as one invocation: if the key is missing the function runs once for that call and the mapping is published, else the function does not run.

## Lazy create belongs inside one atomic call

A cache or intern table wants “load once per key.” Two threads can both see absent and both load. `putIfAbsent` closes the race only after you already built `v`, so you still pay for duplicate construction. `computeIfAbsent` builds the value **while establishing** the mapping. The class page’s own recipe is a frequency map: `freqs.computeIfAbsent(key, k -> new LongAdder()).increment()`.

The contract: the **entire method** is atomic; if the key is absent the function is invoked exactly once **per that invocation**, else not at all. Other **updates** may wait while it runs, so keep the function short. It must **not** modify this map (`IllegalStateException` on a detectably recursive update). A `null` return records nothing — values cannot be null ([[Does ConcurrentHashMap allow null keys or values]]).

```d2
direction: down
race: "containsKey / get then put\ntwo loads, lost update" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
ok: "computeIfAbsent(k, f)\none atomic install" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
race -> ok: "replace with"
```

**Fig. 1.** Per-call safety is not a transaction. The function is the insert.

`putIfAbsent`, `compute`, and `merge` are the sibling atomic shapes ([[How do you avoid a check-then-act race on ConcurrentHashMap]]). Use `putIfAbsent` when the value is already in hand; use `computeIfAbsent` when creation is the cost you wanted to skip. HashMap’s `put` vs `computeIfAbsent` is a single-thread API split ([[What is the difference between HashMap put and computeIfAbsent]]); `HashMap.putIfAbsent` does not make `HashMap` concurrent ([[What is the difference between HashMap and ConcurrentHashMap]]). Concurrent structural use of `HashMap` is undefined (you must lock or wrap it) — that is the cache-map choice, not a Java 7 “infinite loop” spec.

Implementation sits on the same bin lock as other Java 8 writes ([[How does ConcurrentHashMap use CAS and synchronized in Java 8]]): empty bin uses a reservation node; occupied bin `synchronized`s the head, then applies `f`. `get` still does not lock the table ([[Does ConcurrentHashMap get lock the whole table]]).

```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.LongAdder;

class Demo {
    final ConcurrentHashMap<String, String> cache = new ConcurrentHashMap<>();
    final ConcurrentHashMap<String, LongAdder> freqs = new ConcurrentHashMap<>();

    void wrong(String key) {
        if (!cache.containsKey(key)) {     // race
            cache.put(key, load(key));
        }
    }

    String cached(String key) {
        return cache.computeIfAbsent(key, this::load);
    }

    void count(String key) {
        freqs.computeIfAbsent(key, k -> new LongAdder()).increment();
    }

    String load(String key) {
        return key;
    }
}
```

**Listing 1.** Cache load and the class’s `LongAdder` histogram both belong on `computeIfAbsent`, not on a hand-rolled check.

> [!warning] The function must not re-enter this map
> Nested `computeIfAbsent` / `put` on the **same** map can throw `IllegalStateException` (“recursive update”). Other threads’ **updates** on that bin wait for `f`; do not call a slow remote load while holding that path if you can precompute. `HashMap.putIfAbsent` is still `HashMap`: unsynchronized.

> [!warning] `null` from `f` is “do not map,” not a stored null
> Returning `null` leaves the key absent. That is how a loader declines to cache. It is not a way to store null on this map. Runtime exceptions from `f` leave the mapping unestablished.

> [!tip] Interview answer
> **Use `computeIfAbsent` so “check then create” is one atomic step — `containsKey` plus `put` still races on `ConcurrentHashMap`.** Prefer it over `putIfAbsent` when building the value is expensive. Keep `f` short, do not mutate the map inside it, and do not use `HashMap.putIfAbsent` as the concurrent substitute.
