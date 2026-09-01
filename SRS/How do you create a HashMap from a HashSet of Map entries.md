<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Map/HashMap #SRS

# How do you create a `HashMap` from a `HashSet` of `Map` entries?

> [!abstract] Short answer
> **There is no `HashMap` constructor that takes a `Collection` of entries.** Allocate a map, iterate the `HashSet<Map.Entry<K,V>>`, and `put` each `getKey()` / `getValue()`. `HashMap(Map)` copies another map, not a set of pairs. `HashSet(Collection)` is the opposite direction.

## Loop `put` — the constructor that does not exist

`HashMap` offers `HashMap()`, `HashMap(int)` / `(int, float)`, `HashMap(Map)`, and (since 19) `newHashMap(int numMappings)`. None accepts `Set<Map.Entry<K,V>>`. `putAll` also wants a `Map`. So you copy field-wise:

```java
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

class FromEntries {
    static <K, V> HashMap<K, V> toHashMap(Set<Map.Entry<K, V>> set) {
        HashMap<K, V> map = HashMap.newHashMap(set.size());
        for (Map.Entry<K, V> entry : set) {
            map.put(entry.getKey(), entry.getValue());
        }
        return map;
    }
}
```

**Listing 1.** Java 21. `newHashMap(n)` sizes for **n mappings** at load factor 0.75 so the puts usually skip a resize. `new HashMap<>(set.size())` is **bucket capacity**, not expected size; with 0.75 you still rehash once `n` exceeds about `0.75 * capacity` ([[What is initial capacity in Java collections such as HashMap]]).

A stream is the same puts with extra rules:

```java
HashMap<K, V> map = set.stream().collect(
        Collectors.toMap(
                Map.Entry::getKey,
                Map.Entry::getValue,
                (a, b) -> b,
                HashMap::new));
```

**Listing 2.** The four-argument `Collectors.toMap` is the one that both **merges** duplicate keys and **supplies** a `HashMap`. The two-argument form throws `IllegalStateException` on duplicate keys and does not promise a `HashMap`. `Map.ofEntries(...)` is an unmodifiable map, not a `HashMap`, and rejects null keys, values, and entries.

```d2
direction: down
set: "HashSet<Map.Entry<K,V>>\nequals = key AND value" {
  width: 320
  height: 80
  style.fill: "#e3f2fd"
}
loop: "for each entry\nput(getKey(), getValue())" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
map: "HashMap<K,V>\nunique by key only" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}

set -> loop
loop -> map
```

**Fig. 1.** The set stores **pairs**. The map stores **keys**. Same-key, different-value entries can all sit in the `HashSet` and then collapse on `put`.

## Entry equality is not map equality

`Map.Entry.equals` is true when **both** key and value match (`getKey` / `getValue`, null-safe). `hashCode` is `key.hashCode ^ value.hashCode` (zeros for nulls). A `HashSet` therefore treats `("a",1)` and `("a",2)` as two elements ([[Does HashSet allow a null element]] is a different null: a null *entry* vs a null key).

`HashMap.put` replaces on key only: “If the map previously contained a mapping for the key, the old value is replaced” ([[Can a HashMap contain two equal keys at the same time]]). HashSet iteration order is unspecified, so **which value survives is unspecified**.

```java
Set<Map.Entry<String, Integer>> set = new HashSet<>();
set.add(new AbstractMap.SimpleEntry<>("a", 1));
set.add(new AbstractMap.SimpleEntry<>("a", 2));
set.size(); // 2

HashMap<String, Integer> map = HashMap.newHashMap(set.size());
for (Map.Entry<String, Integer> e : set) {
    map.put(e.getKey(), e.getValue());
}
map.size(); // 1 — value is 1 or 2
```

**Listing 3.** Two set members, one map key. `AbstractMap.SimpleEntry` allows null keys/values; `Map.entry` / `Map.Entry.copyOf` do not (`NullPointerException`).

Live `map.entrySet()` entries stay tied to that map during iteration of the view. Copying those objects into a `HashSet` stores the same references: later mutation of the source map can change `equals` / `hashCode` of set elements, which is unspecified for any `Set`. Snapshot with `SimpleEntry` (nulls allowed) or `Map.Entry.copyOf` (Java 17+, no null key or value).

`HashSet` may hold one `null` element. `entry.getKey()` then throws `NullPointerException`. A non-null entry with a null key is a legal `HashMap` put ([[Can HashMap store a null key]]).

The reverse conversion is one constructor: `new HashSet<>(map.keySet())` or `new HashSet<>(map.entrySet())` — because `HashSet` has `HashSet(Collection)` and those views are collections. That is not this direction ([[What is the difference between HashMap and HashSet]]).

> [!warning] `HashSet<Map.Entry>` does not mean unique keys
> Interview code that assumes `set.size() == map.size()` after the loop is wrong whenever two entries share a key and differ in value. `put` silently keeps one. `Collectors.toMap` without a merge function fails instead (`IllegalStateException`).

> [!warning] `new HashMap<>(set)` does not compile
> `HashMap` has no collection copy constructor. `new HashMap<>(someMap)` needs a `Map`. Passing the `HashSet` is a type error, not a copy of entries.

> [!tip] Interview answer
> **Loop the `HashSet<Map.Entry<K,V>>` and `put` each key and value into a new `HashMap` — there is no entries constructor.** Size with `HashMap.newHashMap(set.size())` if you are on 19+. Entry equality uses key **and** value, so the set can hold two pairs with the same key; the map will not.
