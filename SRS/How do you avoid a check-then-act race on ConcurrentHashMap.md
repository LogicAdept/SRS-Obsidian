<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Concurrency #SRS

# How do you avoid a check-then-act race on `ConcurrentHashMap`?

> [!abstract] Short answer
> **Do not compose `containsKey` / `get` with a later `put`.** Use one atomic method: `putIfAbsent` when the value is already in hand, `computeIfAbsent` when it should be built only if missing. `replace`, `remove(key, value)`, `compute`, and `merge` cover the other check-then-act shapes.

## Each call is safe; the pair is not

`get` does not lock the table ([[Does ConcurrentHashMap get lock the whole table]]), so two threads can both see “absent” and both insert. The map never makes a two-call sequence atomic. `putIfAbsent` is specified as the `containsKey` then `put` (else `get`) pattern **except that the action is performed atomically**. `computeIfAbsent` is stronger for lazy create: the whole invocation is atomic; if the key is absent the function runs exactly once for that call, else not at all.

```d2
direction: right
race: "containsKey / get\nthen put" {
  width: 220
  height: 80
  style.fill: "#ffebee"
}
atomic: "putIfAbsent / computeIfAbsent\nreplace / merge / compute" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
race -> atomic: "replace with"
```

**Fig. 1.** A thread-safe map still races on a check-then-act pair. One `ConcurrentMap` method is the fix.

```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.LongAdder;

class Demo {
    final ConcurrentHashMap<String, LongAdder> freqs = new ConcurrentHashMap<>();
    final ConcurrentHashMap<String, String> cache = new ConcurrentHashMap<>();

    // Lost update / double load: both threads can pass the check
    void wrong(String key) {
        if (!cache.containsKey(key)) {
            cache.put(key, load(key));
        }
    }

    String rightLazy(String key) {
        return cache.computeIfAbsent(key, this::load);
    }

    void rightReady(String key, String value) {
        cache.putIfAbsent(key, value);
    }

    void count(String key) {
        freqs.computeIfAbsent(key, k -> new LongAdder()).increment();
    }

    String load(String key) {
        return key;
    }
}
```

**Listing 1.** `containsKey` then `put` is the race. `computeIfAbsent` builds the value only while establishing the mapping; `putIfAbsent` publishes a value you already have. The `LongAdder` line is the class’s own frequency-map recipe.

`putIfAbsent` returns the **previous** value, or `null` if this call installed the mapping (`null` cannot be stored — [[Does ConcurrentHashMap allow null keys or values]]). `computeIfAbsent` returns the **current** value (existing or newly computed). If the function returns `null`, nothing is recorded.

Same idea for other races: `remove(k, v)` and `replace(k, old, new)` are the atomic forms of “get, test, mutate.” `compute` / `merge` when the new value depends on the old one. HashMap’s `put` vs `computeIfAbsent` is a single-thread API split, not a concurrency tool ([[What is the difference between HashMap put and computeIfAbsent]]). Why `computeIfAbsent` is the usual cache call: [[Why should you use computeIfAbsent on ConcurrentHashMap]].

> [!warning] `HashMap.putIfAbsent` does not make a `HashMap` concurrent
> The method name matches. The class is unsynchronized. Concurrent `HashMap` mutation still needs an external lock or a real concurrent map. Thread-safe **per call** on `ConcurrentHashMap` is also not a transaction: `get` then `put` still races.

> [!warning] `putIfAbsent` still allocates the argument
> You build `v` before the call, so two threads can each construct an expensive object and only one mapping remains. Prefer `computeIfAbsent` when creation is the cost you wanted to skip. Keep that function short: other **updates** on the same bin may wait, and the function must not modify the map (recursive update is `IllegalStateException`).

> [!tip] Interview answer
> **`containsKey` then `put` (or `get` then `put`) is a race even on `ConcurrentHashMap` — each call is safe, the sequence is not.** Use `putIfAbsent` for a ready value, `computeIfAbsent` to create only if absent, and `replace` / `merge` / `compute` for the other atomic shapes. `HashMap.putIfAbsent` is still just `HashMap`: not thread-safe.
