<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/HashMap #Java/String #Java/HashCodeEquals #SRS

# Can two equal `String` objects both be keys in an `IdentityHashMap`?

> [!abstract] Short answer
> **Yes, when they are distinct instances (`==` is false).** `IdentityHashMap` treats keys as the same iff `k1 == k2`. `String.equals` compares character sequences, so two `new String("x")` copies are two keys. `HashMap` keeps one mapping and the second `put` replaces the value. Two interned literals `"x"` are the **same** instance, so they collapse even here.

## `==` keys, not `equals` keys

`IdentityHashMap` is not a general-purpose `Map`: two keys match only by reference. `HashMap` matches with `equals` (null-safe). `String.equals` is true when the other object is a `String` with the same characters. The copy constructor `new String(original)` allocates a **new** object that represents the same sequence. Those two facts together are the dump example. [[What is the difference between HashMap and IdentityHashMap]] [[How does IdentityHashMap decide whether two keys are the same]]

```d2
direction: down
s1: "new String(\"x\")" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
s2: "new String(\"x\")\nequals, not ==" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
ihm: "IdentityHashMap\ntwo entries" {
  width: 220
  height: 70
  style.fill: "#c8e6c9"
}
hm: "HashMap\none entry" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}

s1 -> ihm
s2 -> ihm
s1 -> hm
s2 -> hm: put replaces
```

**Fig. 1.** Same characters, two objects. Identity maps keep both. Value maps keep one.

```java
IdentityHashMap<String, String> byRef = new IdentityHashMap<>();
byRef.put(new String("identityKey"), "Google");
byRef.put(new String("identityKey"), "Facebook");
// size 2 — distinct copies, both keys

HashMap<String, String> byEq = new HashMap<>();
byEq.put(new String("identityKey"), "Google");
byEq.put(new String("identityKey"), "Facebook");
// size 1 — {identityKey=Facebook}

IdentityHashMap<String, String> literals = new IdentityHashMap<>();
literals.put("identityKey", "Google");
literals.put("identityKey", "Facebook");
// size 1 — both puts used the interned instance
```

**Listing 1.** Conceptual: copies are two identity keys; `equals` collapses them in `HashMap`; interned literals are one reference, so the second identity `put` replaces.

String literals (and other constant-expression strings) are interned to one instance. `"identityKey" == "identityKey"` is true, so they are **not** two keys. `put` of the same reference replaces the value, same as any `Map`. “Duplicate-looking keys” means two references that `equals` would merge, not two mappings for one `==` key. [[What is IdentityHashMap for]] [[Does overriding equals change IdentityHashMap lookup]]

> [!warning] Demo with `"x"` instead of `new String("x")`
> The interview snippet only works if each `put` gets a **new** instance. Literals, `intern()`, and many constant concatenations share one object; `IdentityHashMap.size()` stays 1 and you “prove” the wrong class. Overriding `String.equals` is not in play: the map never calls it.

> [!tip] Interview answer
> **Yes — `IdentityHashMap` keys match with `==`, so two `new String("x")` objects are two keys even though `equals` is true.** `HashMap` would keep one entry and the second value would win. Interned literals are the same instance, so they still collapse.
