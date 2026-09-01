<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Concurrency #SRS

# Is `IdentityHashMap` synchronized?

> [!abstract] Short answer
> **No.** The implementation is not synchronized. Concurrent access plus a structural modify (add or delete a mapping) needs an external lock, or `Collections.synchronizedMap` wrapped at creation. `==` key equality is not a memory model and is not a lock. Replacing the value of a key already in the map is not a structural modification in that sentence.

## Same duty as `HashMap`, different equality

The class comment matches `HashMap` on threads: if several threads use the map and at least one modifies it structurally, synchronize externally — typically on an encapsulating object, or wrap:

```java
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.Map;

class Demo {
    static void wrap() {
        Map<Object, String> m =
                Collections.synchronizedMap(new IdentityHashMap<>());
        Object k = new Object();
        m.put(k, "v"); // safe: goes through the wrapper

        synchronized (m) {
            Iterator<Object> i = m.keySet().iterator();
            while (i.hasNext()) {
                i.next();
            }
        }
    }
}
```

**Listing 1.** Official wrap, at creation. Wrapper methods lock the returned map. **Iteration does not.** `Collections.synchronizedMap` requires `synchronized (m)` for `Iterator` / `Spliterator` / `Stream`. [[Is java.util.HashMap thread safe]]

```text
IdentityHashMap
  since 1.4
  not synchronized
  keys: k1 == k2  (not equals)
  null key and null values allowed
  wrap: Collections.synchronizedMap(new IdentityHashMap<>(...))
  iterators: fail-fast (best-effort)
```

**Listing 2.** Thread-safety is orthogonal to identity semantics. [[How does IdentityHashMap decide whether two keys are the same]]

```d2
direction: down
raw: "IdentityHashMap\n== keys, no monitor" {
  width: 280
  height: 70
  style.fill: "#ffcdd2"
}
wrap: "Collections.synchronizedMap\none lock; iterate under synchronized(m)" {
  width: 360
  height: 80
  style.fill: "#fff3e0"
}
chm: "ConcurrentHashMap\nconcurrent; equals/hashCode; no nulls" {
  width: 360
  height: 80
  style.fill: "#e8f5e9"
}

raw -> wrap
raw -> chm: "not a drop-in: different equality"
```

**Fig. 1.** Identity lookup does not buy concurrency. There is no `ConcurrentIdentityHashMap`.

Fail-fast view iterators throw `ConcurrentModificationException` after a structural change, except via that iterator’s `remove`. That check is best-effort under unsynchronized mutation and is **not** a happens-before protocol. [[Are IdentityHashMap iterators fail-fast]]

`ConcurrentHashMap` is a concurrent hash table: retrievals generally do not lock the whole table, iterators do not throw CME, **null is forbidden**, and keys use `equals` / `hashCode`. Wrapping `IdentityHashMap` keeps `==` keys and one mutex. It does not become CHM. Compound `containsKey` then `put` still needs the same lock around the whole sequence. [[Does ConcurrentHashMap allow null keys or values]]

> [!warning] `==` keys are not thread-safe keys
> Two threads `put`ting distinct objects that `equals` each other still race on the table. Two threads `put`ting the **same** reference still race. Identity comparison only answers “is this the same object.” It does not publish writes. Do not treat fail-fast CME as a lock, and do not skip `synchronized (m)` on a wrapped view iteration.

> [!tip] Interview answer
> **No — `IdentityHashMap` is not synchronized; `==` equality does not make it thread-safe.** Concurrent structural updates need an external lock or `Collections.synchronizedMap` at creation, and you still lock that wrapper when you iterate. For a concurrent hash map use `ConcurrentHashMap`, knowing it uses `equals` and rejects nulls — there is no concurrent identity map in the JDK.
