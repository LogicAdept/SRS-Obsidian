<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/HashCodeEquals #SRS

# How does `IdentityHashMap` decide whether two keys are the same?

> [!abstract] Short answer
> **By reference identity only:** keys `k1` and `k2` count as the same key **if and only if** `k1 == k2`. The map never asks `equals` or the key’s `hashCode`. That is the opposite of `HashMap`, which uses null-safe `equals` after hashing.

## The documented key test

Java SE 21 `IdentityHashMap` javadoc:

```text
IdentityHashMap:  same key  ⇔  (k1 == k2)
HashMap (typical): same key  ⇔  (k1 == null ? k2 == null : k1.equals(k2))
```

**Listing 1.** Spec formulas. Reference equality replaces object equality for keys **and** values (for example `containsValue` and entry equality).

Bucketing uses `System.identityHashCode`, not `key.hashCode()`. [[Does IdentityHashMap use the hashCode method]] and [[Does overriding equals change IdentityHashMap lookup]] spell out that overrides are ignored.

```d2
direction: down
keys: "Two String copies\nsame text, different refs" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
ihm: "IdentityHashMap\nk1 == k2 ? → two entries" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
hm: "HashMap\nequals ? → one entry" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}

keys -> ihm
keys -> hm
```

**Fig. 1.** Value-equal but distinct instances: identity map keeps both; equals-based map coalesces.

```java
Map<String, Integer> id = new IdentityHashMap<>();
Map<String, Integer> eq = new HashMap<>();

String a = new String("key");
String b = new String("key");

id.put(a, 1);
id.put(b, 2);   // second mapping — a != b
eq.put(a, 1);
eq.put(b, 2);   // replaces — a.equals(b)

id.size(); // 2
eq.size(); // 1
```

**Listing 2.** Conceptual demo with distinct `String` instances (not literals).

This intentionally **violates** the general `Map` contract that compares with `equals`. Use it only when reference identity is the requirement (node tables for copy/serialization, proxy maps). [[What is the difference between HashMap and IdentityHashMap]] is the broader contrast; [[What is IdentityHashMap for]] is the niche.

> [!warning] String literals can lie in demos
> `"key"` literals may be **interned**, so two `"key"` occurrences can be `==` and look like one `IdentityHashMap` entry. Use `new String("key")` (or other distinct allocations) when you mean to show reference inequality.

> [!warning] Values use `==` too
> The same reference rule applies to **values** in this map’s API (for example whether a value is present). Do not assume `containsValue` means `equals` the way it does on `HashMap`.

> [!tip] Interview answer
> **`IdentityHashMap` treats two keys as the same only when they are the same object (`==`).** It does not call `equals` or `hashCode` on the key; it buckets with `System.identityHashCode`. That is why two equal `String` copies are two keys here and one key in `HashMap`.
