<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/Hashtable #Java/Collections/Concurrency #Java/Versions/8 #SRS

# What is the difference between `HashMap` and `Hashtable`?

> [!abstract] Short answer
> **`HashMap` is the unsynchronized `Map` that allows a `null` key and `null` values. `Hashtable` is the legacy synchronized table that rejects both.** The `HashMap` javadoc calls them roughly equivalent except for those two points. Prefer `HashMap`, or `ConcurrentHashMap` when you actually need concurrent maps. `Hashtable` also never got Java 8 tree bins.

## What the APIs promise

`HashMap` (since 1.2) extends `AbstractMap`, permits `null` values and the `null` key, and is **not** synchronized. `Hashtable` (since 1.0) extends `Dictionary`, implements `Map` since 1.2, and maps **non-null** keys to **non-null** values. Its `put` javadoc: neither key nor value can be `null`. `get(null)` throws `NullPointerException`.

As of Java 2, `Hashtable` is synchronized. If you do not need thread safety, use `HashMap`. If you want a concurrent map, use `ConcurrentHashMap`. That recommendation is on the `Hashtable` class page, not a blog rule. `Hashtable` is **not** `@Deprecated`; `Properties` still extends it.

```d2
direction: down
q: "Need a hash map?" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
hm: "HashMap\nnulls OK, no locks" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
chm: "ConcurrentHashMap\nconcurrent writers" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
ht: "Hashtable\nlegacy, synchronized, no nulls" {
  width: 300
  height: 80
  style.fill: "#ffe0b2"
}

q -> hm: single thread / external lock
q -> chm: many threads
q -> ht: only if an API still requires it
```

**Fig. 1.** The documented replacement path. `Properties` still extends `Hashtable`; that is why the class remains, not because it is the default map. [[How would you explain drawbacks of the legacy Hashtable class]] and [[How does Hashtable differ from ConcurrentHashMap]] are those follow-ups.

## Nulls, locks, and iteration

```text
                 HashMap              Hashtable
null key/value   yes                  NPE
synchronized     no                   yes (the instance)
default buckets  16                   11
since            1.2                  1.0 (Map since 1.2)
superclass       AbstractMap          Dictionary
```

**Listing 1.** Contract and construction differences from the two class javadocs (Java SE 21).

`Hashtable` methods such as `get`, `put`, `remove`, and `size` are `synchronized`. That is one lock for the whole table. It is not the same as `ConcurrentHashMap`’s concurrent writers. `HashMap` iterators on collection views are fail-fast. `Hashtable` view iterators are fail-fast too; `keys()` / `elements()` return `Enumeration`s that are **not** fail-fast — structural mutation during enumeration is undefined.

## Implementation extras (not extra API)

Both chain colliding entries in a bucket. OpenJDK `Hashtable` indexes with `(hash & 0x7FFFFFFF) % table.length` and grows with `rehash()` to `(oldCapacity << 1) + 1`. Default capacity 11 is not a power of two. `HashMap` uses a power-of-two table and `(n - 1) & hash`. [[How and when does HashMap resize its buckets]] is that doubling.

JEP 180 put tree bins in `HashMap`, `LinkedHashMap`, and `ConcurrentHashMap`. It explicitly did **not** change `Hashtable`, so a crowded `Hashtable` bucket stays a list. [[How does HashMap handle collisions]] is the Java 8+ `HashMap` path.

> [!warning] “Thread-safe `HashMap`” is not `Hashtable`
> Coarse `synchronized` on every call is still a single lock, and `null` is still forbidden. `Collections.synchronizedMap(new HashMap<>(...))` is the wrapper the `HashMap` javadoc shows when you must share a `HashMap`. For real concurrent maps, the `Hashtable` page names `ConcurrentHashMap`.

> [!tip] Interview answer
> **`HashMap` allows a `null` key and `null` values and is unsynchronized. `Hashtable` forbids nulls, synchronizes each public mutator/lookup on `this`, and is the 1.0 `Dictionary` later retrofitted as a `Map`. Use `HashMap` or `ConcurrentHashMap`. `Hashtable` still chains only; it did not get Java 8 tree bins.**
