<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Java/Collections/Map/HashMap #SRS

# Does putting an existing key change `LinkedHashMap` iteration order?

> [!abstract] Short answer
> **Not in the default map.** Encounter order is insertion-order unless you pass `accessOrder=true`. Re-`put` of a live key does **not** move that entry. In access-order, `put` **is** an access: the entry becomes youngest (last). `putFirst` / `putLast` (Java 21) relocate on purpose and are not the same as `put`.

## Two modes, two answers

Default constructors build an **insertion-ordered** map. Eldest is least recently inserted; youngest is last. The class javadoc: encounter order is **not** affected if a key is re-inserted with `put` — meaning `put(k, v)` when `containsKey(k)` is already true. The value is replaced; the list node stays. A **new** key is linked as youngest (end of the list). Default `accessOrder` is false. [[What are LinkedHashMap ordering guarantees]]

The three-argument constructor with `accessOrder == true` orders by last access, least-recently accessed first. `put` is in the access list (`put`, `putIfAbsent`, `get`, `getOrDefault`, `compute*`, `merge`; `putAll` accesses each copied mapping). If the entry exists after the call, it moves to last. `replace` accesses only when the value actually changes. `containsKey` is not an access. [[Can LinkedHashMap fully implement an LRU cache]] [[How do you build a cache with invalidation using LinkedHashMap]]

```d2
direction: down
put: "put(k, v)\ncontainsKey(k) already true" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
ins: "insertion-order (default)\nvalue replaced, node stays" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
acc: "access-order\nvalue replaced, node to last" {
  width: 300
  height: 80
  style.fill: "#c8e6c9"
}

put -> ins
put -> acc
```

**Fig. 1.** Same `put`. Only access-order treats it as a use that refreshes encounter order.

```java
LinkedHashMap<String, Integer> insertion = new LinkedHashMap<>();
insertion.put("a", 1);
insertion.put("b", 1);
insertion.put("a", 2);     // still a then b
insertion.putFirst("b", 3); // b then a — explicit relocate, not put

LinkedHashMap<String, Integer> access = new LinkedHashMap<>(16, 0.75f, true);
access.put("a", 1);
access.put("b", 1);
access.put("a", 2); // b then a — put is an access
```

**Listing 1.** Conceptual: default re-`put` keeps position. `putFirst` / `putLast` still relocate. Access-order re-`put` moves to last.

`removeEldestEntry` runs from `put` / `putAll` only **after a new entry is inserted**. Replacing a value does not consult it (size does not grow). In access-order the node still moves. [[What is the difference between HashMap and LinkedHashMap]]

> [!warning] “Re-put never moves, so LinkedHashMap cannot be LRU”
> That sentence is the **insertion-order** rule, then applied to an LRU question. LRU needs `accessOrder=true`, where `put` **does** move the node. The method in dumps named `recordAccess` is not part of the public API; the javadoc list of accesses is. `HashMap` has no encounter order to update.

> [!tip] Interview answer
> **Default `LinkedHashMap` is insertion-order: `put` of an existing key replaces the value and does not change iteration order.** Construct with `accessOrder=true` and that same `put` is an access, so the entry moves to last. New keys always go at the end. Java 21 `putFirst`/`putLast` relocate regardless of mode.
