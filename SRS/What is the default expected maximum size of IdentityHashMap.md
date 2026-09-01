<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/HashMap #SRS

# What is the default expected maximum size of `IdentityHashMap`?

> [!abstract] Short answer
> **21.** The no-arg constructor builds an empty identity hash map with that default expected maximum size. It is **not** HashMap’s initial capacity **16** (load factor 0.75). Exceeding the expected size may rehash; iteration cost tracks bucket count, so do not set it wildly high.

## One tuning knob, not capacity + load factor

`IdentityHashMap` has a single performance parameter: **expected maximum size** — how many mappings you expect to hold. Internally that chooses the initial number of buckets. The relationship is unspecified in the spec; putting more than expected may grow the table (rehash). Iteration over views is proportional to **bucket count**, so overstating the expected size wastes memory and slows iteration. Negative `expectedMaxSize` is `IllegalArgumentException`. [[What is IdentityHashMap for]] [[How does IdentityHashMap resolve collisions]]

The no-arg constructor’s javadoc: default expected maximum size **(21)**. OpenJDK `jdk-21-ga` uses internal `DEFAULT_CAPACITY = 32` (power of two) because 32 at a 2/3 load factor is that specified 21. The public table is an interleaved key/value `Object[]` of length `2 * capacity`.

```d2
direction: down
ihm: "IdentityHashMap()\nexpected max size = 21" {
  width: 300
  height: 70
  style.fill: "#c8e6c9"
}
hm: "HashMap()\ncapacity 16, load 0.75" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}

ihm -> hm: do not swap 21 and 16
```

**Fig. 1.** Two defaults. Recap tables that put IdentityHashMap at 16 and HashMap at 21 have the numbers backwards.

```java
IdentityHashMap<Object, String> id = new IdentityHashMap<>();        // expected max 21
IdentityHashMap<Object, String> big = new IdentityHashMap<>(1000);   // hint, may still rehash

HashMap<Object, String> hm = new HashMap<>(); // initial capacity 16, load factor 0.75
```

**Listing 1.** Conceptual: pass `expectedMaxSize` when you know the count. That argument is not HashMap’s `initialCapacity`. [[What are the initial capacity and load factor parameters of HashMap]] [[Why can IdentityHashMap be faster than HashMap]]

> [!warning] Cheat sheet that swaps 16 and 21
> 21 is **expected maximum mappings**, not “capacity 21.” HashMap’s 16 is **buckets**, and it still uses load factor 0.75. Copy-paste tables in the same dump sometimes reverse the two numbers. Linear-probe growth is 2/3 occupancy in the JDK, not HashMap’s 0.75.

> [!tip] Interview answer
> **The default expected maximum size of `IdentityHashMap` is 21.** `HashMap`’s default initial capacity is 16. They are different knobs: expected entries versus bucket count plus load factor. Size past the hint and the identity table rehashes.
