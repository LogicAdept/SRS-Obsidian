<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #SRS

# Can `HashMap` store a null key?

> [!abstract] Short answer
> **Yes.** `HashMap` permits the `null` key and `null` values. Because keys are unique, there is at most **one** mapping whose key is `null`; a second `put(null, …)` replaces that mapping’s value.

## Contract vs other maps

The class javadoc states that `HashMap` provides all optional `Map` operations and **permits `null` values and the `null` key**. That is a deliberate contrast with [[What is the difference between HashMap and Hashtable]] (`Hashtable` rejects null keys and values) and with [[Does ConcurrentHashMap allow null keys or values]] (same ban; a null `get` result means absent).

```java
Map<String, Integer> map = new HashMap<>();
map.put(null, 1);
map.put(null, 2); // still one null-key entry; value becomes 2
map.get(null);    // 2
map.put("a", null);
map.put("b", null); // many null values are fine
```

**Listing 1.** One null key (replace on conflict); any number of null values.

## Where the null key lands (OpenJDK)

```d2
direction: down
key: "key == null" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
h: "hash(key) → 0" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
idx: "index = (n - 1) & 0 → 0" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
bin: "bucket 0\n(may also hold other keys)" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

key -> h
h -> idx
idx -> bin
```

**Fig. 1.** OpenJDK’s `HashMap.hash` returns `0` for a null key, so the bucket index is always `0`. That bucket is not reserved for null alone: any other key whose mixed hash also indexes to `0` shares the chain or tree.

```java
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

**Listing 2.** Conceptual `hash` from OpenJDK `HashMap` (Java 8+). Null never calls `hashCode`.

> [!warning] `get` returning null is ambiguous
> With null values allowed, `map.get(k) == null` means either “no mapping” or “mapped to null”. Use `containsKey` (or `getOrDefault` with a sentinel) when you must tell those apart. Concurrent maps ban nulls partly so a null `get` can mean absent without that race.

Natural-order [[Can TreeMap have null keys or null values]] is stricter: a null key throws `NullPointerException` unless a null-friendly `Comparator` is supplied. Do not treat “no null keys” as a universal `Map` rule.

> [!tip] Interview answer
> **Yes — `HashMap` allows one null key and any number of null values.** OpenJDK hashes null to `0`, so that entry sits in bucket index `0` (possibly with collisions). `Hashtable` and `ConcurrentHashMap` allow neither null keys nor null values; `TreeMap` rejects a null key under natural ordering.
