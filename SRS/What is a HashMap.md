<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #SRS

# What is a `HashMap`?

> [!abstract] Short answer
> **The general-purpose hash-table `Map` in `java.util`.** It implements all optional map operations, allows one `null` key and `null` values, does not specify iteration order, and is **not** synchronized. Expected `get` / `put` are constant-time **if** hashes spread across buckets. Since 1.2; the javadoc calls it roughly `Hashtable` without the lock and with nulls. [[What is the difference between HashMap and Hashtable]]

## What the class is

`HashMap<K,V>` extends `AbstractMap` and implements `Map`, `Cloneable`, and `Serializable`. A `Map` maps keys to values and cannot contain duplicate keys: each key maps to at most one value. Equality of keys is `equals` after `hashCode` selects a bucket. [[What is the Map interface in Java]]

```text
HashMap
  hash table Map
  null key, null values
  order unspecified (may change)
  not synchronized
  defaults: capacity 16, load factor 0.75
  Collections Framework, since 1.2
```

**Listing 1.** Contract from the `HashMap` class javadoc (Java SE 21). Bins and trees are implementation: [[What is the internal structure of HashMap]].

```d2
direction: down
map: "Map contract\nunique keys, get/put" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
hm: "HashMap\nhash → buckets" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
not: "not TreeMap (sorted)\nnot LinkedHashMap (encounter order)\nnot Hashtable (legacy sync)" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
map -> hm
hm -> not
```

**Fig. 1.** Default map when you need lookup by key and do not need order or a monitor on every call. [[What is the difference between HashMap, TreeMap, and LinkedHashMap]]

## Performance knobs, not identity

Capacity is the **number of buckets**, not `size()`. Load factor is how full the table may get before it is rebuilt with about twice as many buckets (default 0.75). The no-arg constructor uses initial capacity 16. Iteration cost is proportional to **capacity plus size**, so an oversized table slows `keySet` / `values` / `entrySet` walks. Many identical `hashCode()` values slow any hash table; `Comparable` keys may help break ties. [[What are the initial capacity and load factor parameters of HashMap]]

Constant-time is **assumed dispersion**, not a worst-case guarantee. [[Does HashMap guarantee its documented lookup time complexity]]

## What it is not

Not thread-safe: concurrent structural modification needs an external lock or `Collections.synchronizedMap` at creation. Iterators are fail-fast on a best-effort basis; do not use `ConcurrentModificationException` as control flow. [[Is java.util.HashMap thread safe]]

Not a sorted or sequenced map. `LinkedHashMap` subclasses it to add encounter order. Prefer `ConcurrentHashMap` when the point is concurrent maps, not a synchronized `HashMap`.

> [!warning] “HashMap is O(1), so any key is fine”
> The javadoc’s constant-time sentence is conditional on the hash spreading. A stable `equals` / `hashCode` pair is still required. [[What requirements apply to keys used in a HashMap]]

> [!tip] Interview answer
> **`HashMap` is the unsynchronized hash-table `Map`: all optional operations, `null` key and values, unspecified order, expected constant-time `get`/`put` if hashes disperse. Defaults 16 and 0.75. Use `LinkedHashMap` or `TreeMap` when order matters, and a concurrent map when threads share writes.**
