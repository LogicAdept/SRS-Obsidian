<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #SRS

# How do you obtain synchronized wrappers for standard Java collections?

> [!abstract] Short answer
> **Call the `Collections.synchronizedXxx` factories.** `synchronizedList`, `synchronizedSet`, and `synchronizedMap` wrap an unsynchronized collection so each method call holds one lock on the wrapper. Use `synchronizedSortedSet` / `synchronizedNavigableSet` and `synchronizedSortedMap` / `synchronizedNavigableMap` when you still need the sorted or navigable type. All later access must go through the returned object, not the backing collection.

## Factories on `Collections`, not a synchronized constructor

`HashMap`, `HashSet`, `ArrayList`, `TreeMap`, and the other general-purpose implementations are not thread-safe. `Collections` returns a synchronized view: a mutex around that backing object. There is no `new SynchronizedHashMap()`. Pick the factory that matches the type you need to keep. [[Is HashSet synchronized]] [[Is LinkedHashMap synchronized]] [[How do you synchronize a TreeMap]]

| You have | You call | You get back |
| --- | --- | --- |
| `Collection` | `synchronizedCollection` | `Collection` |
| `List` | `synchronizedList` | `List` |
| `Set` | `synchronizedSet` | `Set` |
| `SortedSet` | `synchronizedSortedSet` | `SortedSet` |
| `NavigableSet` | `synchronizedNavigableSet` | `NavigableSet` |
| `Map` | `synchronizedMap` | `Map` |
| `SortedMap` | `synchronizedSortedMap` | `SortedMap` |
| `NavigableMap` | `synchronizedNavigableMap` | `NavigableMap` |

Wrapping a `TreeMap` with `synchronizedMap` is thread-safe as a `Map` but drops `SortedMap` / `NavigableMap` methods. `synchronizedCollection` on a `List` similarly drops `get` / `listIterator`. `Hashtable` and `Vector` are already synchronized types; they are not these wrappers. [[Can you unsynchronize a Hashtable]]

Every method on the wrapper locks the wrapper itself. Iteration is not one method: you must `synchronized (wrapper)` around the iterator or for-each. Failure to do that can yield non-deterministic behavior. Under many threads, prefer a concurrent collection instead of a wrapper. [[Why use concurrent collections instead of Collections synchronized wrappers]] [[How do you get a concurrent Set in Java]]

```java
List<String> list = Collections.synchronizedList(new ArrayList<>());
Set<String> set = Collections.synchronizedSet(new HashSet<>());
Map<String, Integer> map = Collections.synchronizedMap(new HashMap<>());
NavigableMap<String, Integer> tree =
        Collections.synchronizedNavigableMap(new TreeMap<>());
```

**Listing 1.** Obtain the wrapper from `Collections`. Keep the navigable factory when you still need `TreeMap` views.

```java
List<String> raw = new ArrayList<>();
List<String> sync = Collections.synchronizedList(raw);

raw.add("bypass");                      // still the unsynchronized list — wrong

synchronized (sync) {
    for (String s : sync) {
        process(s);
    }
}
```

**Listing 2.** Do not touch the backing collection. Lock the wrapper for the whole iteration.

```d2
direction: down
Client: threads
Wrapper: Collections.synchronizedMap
Backed: HashMap
Client -> Wrapper: all access
Wrapper -> Backed: under one lock
```

**Fig. 1.** The wrapper is the only safe handle. The original map must stay unused.

> [!warning] The backing collection is still unsynchronized
> Storing both `raw` and `Collections.synchronizedList(raw)` and mutating `raw` from another thread defeats the wrapper. Iteration needs `synchronized (theWrapper)` even though each `add` is already locked. `synchronizedMap(new TreeMap<>())` is not a synchronized `SortedMap` — use `synchronizedSortedMap` or `synchronizedNavigableMap`.

> [!tip] Interview answer
> **`Collections.synchronizedList`, `synchronizedSet`, and `synchronizedMap` wrap the ordinary collection.** After that, talk only to the wrapper, and lock that same wrapper around any iterator. Use the sorted or navigable factories when you still need `TreeMap` / `TreeSet` operations. For many threads, a concurrent collection is usually the better tool.
