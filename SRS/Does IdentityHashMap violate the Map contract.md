<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/HashMap #Java/HashCodeEquals #SRS

# Does `IdentityHashMap` violate the `Map` contract?

> [!abstract] Short answer
> **Yes, on purpose.** It implements `Map` but is **not** a general-purpose map. The `Map` contract treats keys as the same when `equals` is true (`containsKey` is specified with `key==null ? k==null : key.equals(k)`). This class uses `==` for keys **and** values. Use it only when reference equality is the point (node tables, proxies). `get`/`put` still work.

## The broken rule is key sameness, not the method set

`Map.containsKey` (and the rest of the framework) is defined in terms of `equals`. `IdentityHashMap` documents that it **intentionally violates** that general contract. Two `equals` keys that are distinct instances are two mappings. That is the whole point of a serializer or deep-copy node table: do not collapse distinct objects. [[How does IdentityHashMap decide whether two keys are the same]] [[Can two equal String objects both be keys in an IdentityHashMap]] [[What is IdentityHashMap for]]

The views follow the same rule. `keySet` implements `Set` but does not obey `Set`’s general contract: `contains` / `remove` / `equals` / `hashCode` are identity-based. `values` is the same for `Collection`. `entrySet` entries compare keys and values with `==`, and `hashCode` uses `System.identityHashCode`.

```d2
direction: down
spec: "Map.containsKey\nkey.equals(k)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
ihm: "IdentityHashMap\nkey == k" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
ok: "get / put / size\nstill implemented" {
  width: 240
  height: 70
  style.fill: "#c8e6c9"
}

spec -> ihm: intentional break
ihm -> ok
```

**Fig. 1.** “Violates `Map`” means identity instead of `equals`, not a stub that forgot `get`.

```java
String a = new String("x");
String b = new String("x"); // a.equals(b), a != b

IdentityHashMap<String, Integer> id = new IdentityHashMap<>();
id.put(a, 1);
id.put(b, 1);
id.size();          // 2 — Map.equals-based sameness would keep one
id.containsKey(b);  // true via ==

HashMap<String, Integer> hm = new HashMap<>();
hm.put(a, 1);
hm.put(b, 1);
hm.size();          // 1
id.equals(hm);      // Object.equals symmetry/transitivity may fail vs a normal map
```

**Listing 1.** Conceptual: the `Map` rule would merge `a` and `b`. Identity maps do not. Comparing this map to a `HashMap` is the documented `equals` trap. [[What is the difference between HashMap and IdentityHashMap]] [[Does overriding equals change IdentityHashMap lookup]]

Among `IdentityHashMap` instances, `equals` / `hashCode` are consistent with each other (reference mappings, identity hash of entries). Against a “normal” map they need not be symmetric. That is a second, related breach of `Object.equals`, still from the same identity semantics.

This is not `WeakHashMap`. Weak maps still use `equals` for lookup; what they drop is the invariant that `size()` stays put when you do not mutate. Do not paste those two javadoc warnings into one sentence. [[What is WeakHashMap used for]]

> [!warning] “It implements Map, so equals keys must collide”
> Code that copies entries into a `HashMap`, uses `Map.equals`, or looks up with `new Key(id)` assumes the general contract. Here that is wrong by design. Overriding `equals`/`hashCode` on the key type does not fix it. Do not use this class as a general-purpose map.

> [!tip] Interview answer
> **Yes — `IdentityHashMap` implements `Map` but intentionally violates the contract that keys compare with `equals`; it uses `==`.** It is not a general-purpose map. Typical uses are identity-sensitive tables such as serialization or deep copy. `get` and `put` still work; `WeakHashMap` is a different contract break (GC can shrink `size()`).
