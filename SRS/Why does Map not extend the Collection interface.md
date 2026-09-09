<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #SRS

# Why does Map not extend the Collection interface?

> [!abstract] Short answer
> Because the two model different things: a `Collection` is **a group of elements**, while a `Map` is **a set of key-to-value mappings**. Element operations — `add(E)`, `remove(Object)`, iteration over elements — have no honest meaning for pairs ("add" *what* — a key, a value, a pair?). So `Map` is a separate hierarchy root (its Javadoc lists no superinterface beyond `Object`), and the framework bridges the two worlds with **collection views**: `keySet()` → `Set<K>`, `values()` → `Collection<V>`, `entrySet()` → `Set<Map.Entry<K, V>>` ([[What is the main purpose of the Map interface]]).

## Two roots, three views

The element tree answers "does this group contain x?" via `contains`; the mapping tree answers "what is mapped to this key?" via `get`. Forcing `Map` under `Collection` would have to pretend a mapping is an element, and then `Collection`'s contracts — duplicates, `equals` semantics, `add` returning whether the group changed — stop making sense. Instead `Map` exposes exactly three views, and each is a real, live collection backed by the map: removals through the view remove the mapping, while `add`/`addAll` are unsupported ([[What is the Map interface in Java]]).

```d2
direction: down
m: "Map<K, V>\nkey → value mappings\nput / get / remove by key" {
  width: 330
  height: 92
  style.fill: "#ffebee"
}
ks: "keySet()\nSet<K>" {
  width: 200
  height: 68
  style.fill: "#e3f2fd"
}
vs: "values()\nCollection<V>" {
  width: 220
  height: 68
  style.fill: "#e8f5e9"
}
es: "entrySet()\nSet<Map.Entry<K, V>>" {
  width: 280
  height: 68
  style.fill: "#fff3e0"
}
m -> ks: "view"
m -> vs: "view"
m -> es: "view"
```

**Fig. 1.** `Map` is not a `Collection`, but its three views are collections — that is the framework's official bridge, not inheritance.

```java
Map<String, Integer> m = new HashMap<>();
m.put("x", 1); m.put("y", 2);

for (Map.Entry<String, Integer> e : m.entrySet()) {  // idiomatic loop
    System.out.println(e.getKey() + "=" + e.getValue());
}
System.out.println(m.values().getClass().getSimpleName());
// Not a List: the view type is a Collection
```

**Listing 1.** Iterating mappings goes through `entrySet`, the pair-shaped view. Verified on JDK 21 — output: `x=1` / `y=2` / `Values`.

> [!warning] "Map is not part of the Collections Framework" is the wrong conclusion
> The framework's own docs count `Map` as a member — the split is about the type hierarchy, not membership. Two follow-up traps: `values()` returns `Collection`, not `List`, so no index access and ordering only if the map defines one; and a view mutation (`entry.setValue`) writes through to the map — iterating `entrySet` while structurally modifying the map elsewhere risks `ConcurrentModificationException` ([[Can you modify a collection while iterating with a for-each loop]]).

> [!tip] Interview answer
> **`Map` doesn't extend `Collection` because mappings are not elements: `add`/`remove`/iteration semantics of a group of objects don't fit key-value pairs.** The framework instead gives `Map` its own root and three backed views — `keySet`, `values`, `entrySet` — so every map operation that needs a real collection gets one. Ordered maps joined the sequenced side in Java 21 via `SequencedMap`, still outside the `Collection` tree.
