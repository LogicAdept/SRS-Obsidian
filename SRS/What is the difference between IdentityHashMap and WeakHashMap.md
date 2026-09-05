<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/WeakHashMap #Java/HashCodeEquals #Java/JVM/Memory/References #SRS

# What is the difference between `IdentityHashMap` and `WeakHashMap`?

> [!abstract] Short answer
> **Identity is `==` keys (and values) with strong references. Weak is GC-droppable keys with `equals` lookup.** They solve different problems and can be combined in one sentence only as a contrast. Neither is an LRU cache. Both allow a null key. Overriding `equals` does not change IdentityHashMap lookup.

## Two knobs: sameness vs lifetime

`IdentityHashMap` is not a general-purpose `Map`. Keys (and values) match with `==`. Hashing is `System.identityHashCode`. The table is a strong linear-probe array; unused keys stay until you `remove` them. Typical job: topology-preserving copy/serialization node tables and per-instance proxies. Since 1.4. Default expected maximum size 21. [[What is IdentityHashMap for]] [[Does IdentityHashMap violate the Map contract]] [[Can IdentityHashMap be used as a cache]]

`WeakHashMap` is a HashMap-shaped table whose keys are weak. Lookup uses `equals` (and `key.hashCode()`). An entry can disappear when the key is no longer strongly or softly reachable; the map polls a `ReferenceQueue` on access. Values are strong and can pin the key. Typical job: a registry/sidecar that must not keep the object alive. Since 1.2. Intended mainly for identity-`equals` keys, but it still **calls** `equals`. [[What is WeakHashMap used for]] [[How does WeakHashMap work]] [[How do you attach extra data to an object with WeakHashMap]]

```d2
direction: down
q: "need a Map of objects" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
id: "must not collapse equals instances\nIdentityHashMap, pins keys" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
wk: "must not pin the object\nWeakHashMap, equals lookup" {
  width: 320
  height: 80
  style.fill: "#c8e6c9"
}

q -> id
q -> wk
```

**Fig. 1.** Orthogonal questions. `==` vs GC. You can need both (identity *and* non-pinning) only by building it yourself; these two classes each do one.

| | `IdentityHashMap` | `WeakHashMap` |
| --- | --- | --- |
| Key sameness | `==` | `equals` |
| Hash | `identityHashCode` | `key.hashCode()` |
| Key refs | strong (table slots) | weak (`WeakReference`) |
| GC | does not drop entries | may drop unused keys |
| Values | strong; compared with `==` | strong; can pin keys |
| Null key | yes (sentinel in table) | yes (sentinel, not collected) |
| Cache? | no | no (not LRU; not soft) |

Identity vs weak are orthogonal. LRU size eviction is `LinkedHashMap`. [[How do you build a cache with invalidation using LinkedHashMap]] [[Does IdentityHashMap allow null keys or values]] [[Does WeakHashMap allow null keys or values]] [[Does overriding equals change IdentityHashMap lookup]]

```java
String a = new String("x");
String b = new String("x"); // equals, not ==

IdentityHashMap<String, String> id = new IdentityHashMap<>();
id.put(a, "A");
id.put(b, "B");
id.size(); // 2

WeakHashMap<String, String> w = new WeakHashMap<>();
w.put(a, "A");
w.put(b, "B");
w.size(); // 1 — equals collapsed the second put

a = null;
b = null;
// id still pins both String copies
// w may lose its row after GC + poll (recreatable String keys are a Heisenbug)
```

**Listing 1.** Conceptual: identity keeps two equals strings; weak uses `equals` and may later drop the key. [[Can two equal String objects both be keys in an IdentityHashMap]] [[What happens to a WeakHashMap entry when the last strong reference to the key is dropped]]

> [!warning] “WeakHashMap is the cache; IdentityHashMap is the fast HashMap”
> Weak refs are for mappings that must not prevent reclaim, not for LRU. Soft refs are the cache story in `java.lang.ref`. IdentityHashMap’s linear probe can be faster, but it violates the `Map` `equals` contract and **pins** keys. FAQ “do not use IdentityHashMap as a cache” is the strong-ref rule, not “never store a computed value.”

> [!tip] Interview answer
> **`IdentityHashMap` compares keys with `==` and holds them strongly; `WeakHashMap` compares with `equals` and holds keys weakly so the GC can drop entries.** They are not two kinds of cache. Both allow null keys. Overriding `equals` does not change IdentityHashMap. For LRU use access-ordered `LinkedHashMap`.
