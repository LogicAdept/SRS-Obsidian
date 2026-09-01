<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/HashMap #Java/Versions #SRS

# In which Java version was `IdentityHashMap` introduced?

> [!abstract] Short answer
> **Java 1.4 (`Since: 1.4`).** `HashMap` is 1.2 — the Collections Framework wave. Identity maps are a later special-purpose table (`==` keys), not part of that 1.2 starter set. `LinkedHashMap` is also 1.4.

## 1.4 special-purpose map, not 1.2

The class javadoc marks `IdentityHashMap` `Since: 1.4`. It implements `Map` but is **not** a general-purpose map: keys (and values) compare with `==`. Typical uses — topology-preserving copy/serialization node tables, proxy maps — needed that identity table after `HashMap` already existed. [[What is IdentityHashMap for]] [[Does IdentityHashMap violate the Map contract]] [[What is the difference between HashMap and IdentityHashMap]]

`HashMap` is `Since: 1.2`. `WeakHashMap` is also 1.2. `Hashtable` is 1.0 (became a `Map` in 1.2). `LinkedHashMap` is 1.4, same release as identity maps. `EnumMap` and `ConcurrentHashMap` are 1.5. [[In which Java version was Hashtable introduced]] [[In which Java version was EnumMap introduced]]

```d2
direction: right
j10: "1.0\nHashtable" {
  width: 160
  height: 70
  style.fill: "#fff3e0"
}
j12: "1.2\nHashMap\nWeakHashMap\nMap" {
  width: 200
  height: 90
  style.fill: "#e3f2fd"
}
j14: "1.4\nIdentityHashMap\nLinkedHashMap" {
  width: 220
  height: 80
  style.fill: "#c8e6c9"
}
j15: "1.5\nEnumMap\nCHM" {
  width: 180
  height: 80
  style.fill: "#e8f5e9"
}

j10 -> j12
j12 -> j14
j14 -> j15
```

**Fig. 1.** Do not answer “1.2 with collections.” That date belongs to `HashMap`.

```java
IdentityHashMap<Object, String> nodes = new IdentityHashMap<>();
nodes.put(new Object(), "seen"); // API since 1.4
```

**Listing 1.** Conceptual: the type did not exist in 1.2. Linear-probe `==` tables are a 1.4 addition. [[How does IdentityHashMap resolve collisions]] [[How do you create an EnumMap]]

> [!warning] “Collections Framework, so IdentityHashMap is 1.2”
> The framework’s general-purpose hash map is `HashMap` (1.2). Identity and linked-hash maps landed in **1.4**. Mixing the two dates is the usual table error: HashMap 1.2, IdentityHashMap 1.4, separately.

> [!tip] Interview answer
> **`IdentityHashMap` was added in Java 1.4.** `HashMap` is 1.2. It is a special-purpose identity table, not one of the original Collections Framework maps. `LinkedHashMap` shares the 1.4 date.
