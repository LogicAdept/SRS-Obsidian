<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/HashCodeEquals #SRS

# Does overriding `equals` change `IdentityHashMap` lookup?

> [!abstract] Short answer
> **No.** Lookup still decides “same key” with **`k1 == k2` only**. Your overridden `equals` is never consulted on `get` / `put` / `containsKey`. That is the documented reference-equality rule, and why the class intentionally violates the usual `Map` contract that compares with `equals`.

## What lookup actually compares

Java SE 21: two keys in an `IdentityHashMap` are equal **if and only if** `(k1==k2)`. A normal map such as `HashMap` uses `(k1==null ? k2==null : k1.equals(k2))` instead. View collections (`keySet`, `values`, `entrySet`) keep the same reference-equality semantics for their elements.

```d2
direction: down
put: "put(a, value)" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
getB: "get(b) where\na.equals(b) && a != b" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
miss: "Miss\nequals never called" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
getA: "get(a)" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
hit: "Hit\na == stored key" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

put -> getB
getB -> miss
put -> getA
getA -> hit
```

**Fig. 1.** Value equality does not create a hit; only the same reference does.

```java
record Name(String s) {} // equals / hashCode from components

Name a = new Name("Ada");
Name b = new Name("Ada");
IdentityHashMap<Name, Integer> map = new IdentityHashMap<>();
map.put(a, 1);

map.containsKey(b); // false — a != b
map.get(b);         // null
map.get(a);         // 1
map.put(b, 2);      // second mapping; size == 2
```

**Listing 1.** Conceptual: equal `Name` instances are still two keys. Overriding or generating `equals` changes nothing for this map.

`containsKey` is documented as testing whether the specified **object reference** is a key — wording that matches `==`, not `equals`. Bucketing uses `System.identityHashCode`, not the key’s `hashCode`; see [[Does IdentityHashMap use the hashCode method]] and [[What is the difference between HashMap and IdentityHashMap]].

> [!warning] Equal copies are duplicate keys here
> If you `put` with one instance and `get` with another that only `equals` it, you miss — and a second `put` adds a **second** entry. That is correct for identity maps and wrong for value maps. Use [[What is IdentityHashMap for]] only when that behavior is intentional.

> [!warning] `hashCode` overrides are ignored the same way
> Placement does not call `key.hashCode()` either. Overriding `equals` without `hashCode` (or the reverse) still does not affect `IdentityHashMap` lookups; both value contracts are bypassed.

> [!tip] Interview answer
> **Overriding `equals` does not change `IdentityHashMap` lookup.** Keys match only with `==`; `equals` is never used. Two equal instances remain two keys unless they are the same reference. That is deliberate reference-equality semantics, not a bug in your override.
