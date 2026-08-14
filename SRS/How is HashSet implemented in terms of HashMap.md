<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Map/HashMap #Java/HashCodeEquals #SRS

# How is `HashSet` implemented in terms of `HashMap`?

> [!abstract] Short answer
> **It is a `HashMap` whose keys are the set elements and whose values are a shared dummy object.** The javadoc says the set is backed by a hash table, actually a `HashMap` instance. `add` is `put(e, PRESENT)`, `contains` is `containsKey`, `remove` is `remove` on that map. Equality and hashing are the key contract. There is no second table.

## The backing map is the whole structure

OpenJDK keeps `transient HashMap<E,Object> map` and one dummy:

```java
static final Object PRESENT = new Object();
```

**Listing 1.** One shared sentinel. Every mapping’s value is that same reference; membership is “the key is present,” not the value.

```d2
direction: down
el: "Set element e" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
map: "HashMap<E, Object>" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
key: "key = e" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
val: "value = PRESENT" {
  width: 220
  height: 60
  style.fill: "#ffe0b2"
}

el -> map
map -> key
map -> val
```

**Fig. 1.** The set does not store elements beside the map. They **are** the map’s keys.

The no-arg constructor is `map = new HashMap<>()`, so default capacity 16 and load factor 0.75 belong to that map. Capacity and load-factor constructors forward to `HashMap` the same way. Iteration walks `map.keySet()`; cost is set size plus backing capacity, which is the `HashSet` javadoc. [[What is the internal structure of HashMap]] is the array of bins you actually pay for.

## Each mutator is one map call

```java
public boolean add(E e) {
    return map.put(e, PRESENT) == null;
}
public boolean contains(Object o) {
    return map.containsKey(o);
}
public boolean remove(Object o) {
    return map.remove(o) == PRESENT;
}
```

**Listing 2.** OpenJDK `HashSet` (Java 21). `add` is true only when `put` had no previous mapping. `remove` compares the dummy with `==`, which is safe because every live value is `PRESENT`.

`size`, `isEmpty`, and `clear` delegate. Duplicate `add` is the map’s equal-key overwrite: `put` replaces `PRESENT` with `PRESENT` and returns the old dummy, so the set reports `false` and does not grow. [[Can a HashMap contain two equal keys at the same time]] is that uniqueness. Lookup uses the same `hashCode` / identity / `equals` path as any `HashMap` key: [[Is equals invoked when a HashMap bucket contains a single element]].

A mutable element is a mutable key. After it is in the set, changing fields that `equals` or `hashCode` use can hide it. [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]] is the same failure.

## What this is not

`HashSet` does not wrap a `HashMap` you pass in. You cannot get the map back. Values are not user data; do not expect `map.get(e)` from outside.

`LinkedHashSet` is a `HashSet` subclass. A package-private `HashSet` constructor installs a `LinkedHashMap` instead, which is how insertion-order iteration appears. [[How does HashSet differ from LinkedHashSet]] is that subclass. [[What is the difference between HashMap and HashSet]] is the collection-type contrast, not a second implementation.

> [!warning] “Set of values, map of pairs” is the right model
> Interview answers that say `HashSet` is a `HashMap` with no values, or a separate hash table copied from `HashMap`, miss the dummy. There is always a value object. It is just unused. Tree bins, resize, and null (the `null` element is the `null` key) are whatever the backing `HashMap` does.

> [!tip] Interview answer
> **`HashSet` is a `HashMap<E,Object>`: elements are keys, every value is one static dummy `PRESENT`. `add`/`contains`/`remove` are `put`/`containsKey`/`remove`. Uniqueness, hashing, null, resize, and Java 8+ tree bins are the map’s. You do not get a second data structure.**
