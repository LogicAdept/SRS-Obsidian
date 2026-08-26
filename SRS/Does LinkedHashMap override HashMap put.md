<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Java/Collections/Map/HashMap #SRS

# Does `LinkedHashMap` override `HashMap.put`?

> [!abstract] Short answer
> **No** (OpenJDK / Oracle JDK). `LinkedHashMap` inherits `HashMap.put` and the `final` `putVal` implementation. It customizes behavior by overriding **package-private hooks** that `putVal` calls — node factories and `afterNodeAccess` / `afterNodeInsertion` / `afterNodeRemoval` — so the doubly-linked encounter-order list stays updated.

## What `put` actually runs

```d2
direction: down
put: "HashMap.put\n(inherited)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
putVal: "HashMap.putVal\n(final)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
hooks: "LinkedHashMap overrides\nnewNode / afterNode*" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
list: "before/after list\nhead…tail" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

put -> putVal
putVal -> hooks
hooks -> list
```

**Fig. 1.** Insertion still goes through `HashMap.put` → `putVal`; `LinkedHashMap` plugs into hooks, not a `put` override.

`HashMap` documents that subclass `LinkedHashMap` is why those hooks exist: insertion, removal, and access callbacks keep linked-map internals independent of the table mechanics. `put` itself remains:

```java
// HashMap (Java SE / OpenJDK 21) — conceptual
public V put(K key, V value) {
    return putVal(hash(key), key, value, false, true);
}
```

**Listing 1.** Conceptual `put`; `LinkedHashMap` does not replace this method on the map class.

On a successful update of an existing key, `putVal` calls `afterNodeAccess`. After a new mapping is added, it calls `afterNodeInsertion` (which may invoke `removeEldestEntry` for LRU-style maps). New bin nodes are allocated via `newNode`, which `LinkedHashMap` overrides to create `LinkedHashMap.Entry` instances and link them into the encounter-order chain. See [[Does LinkedHashMap extend HashMap]] and [[What is the difference between HashMap and LinkedHashMap]].

## Two kinds of links on an entry

```java
// Conceptual OpenJDK shape (Java 8+)
static class Entry<K,V> extends HashMap.Node<K,V> {
    Entry<K,V> before, after; // encounter order
}
// HashMap.Node also has: Node<K,V> next; // same-bucket chain
```

**Listing 2.** Conceptual entry: bucket collision uses `next`; iteration / access-order uses `before` / `after`. They are different fields.

Java 21 also adds `putFirst` / `putLast` on `LinkedHashMap`; those temporarily set an internal put mode and then call **`this.put`**, still the inherited `HashMap.put`.

> [!warning] Hook names changed with Java 8
> Pre-Java-8 OpenJDK used names like `recordAccess`, `addEntry`, and `createEntry`. From Java 8 onward the hooks are `afterNodeAccess`, `afterNodeInsertion`, `afterNodeRemoval`, plus `newNode` / `replacementNode`. The interview claim “does not override `put`” stayed true; only the hook API renamed.

> [!warning] Do not conflate `next` with `after`
> Walking `next` follows one hash bucket. Walking `after` follows encounter order across the whole map. Same entry object, two unrelated link fields.

> [!tip] Interview answer
> **`LinkedHashMap` does not override `put`.** It inherits `HashMap.put` / `putVal` and overrides hooks such as `newNode` and `afterNodeAccess` / `afterNodeInsertion` so the entry doubly-linked list stays correct. Older JDKs used different hook names (`addEntry`, `recordAccess`), but still did not replace `put`.
