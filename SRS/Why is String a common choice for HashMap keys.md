<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/String #Java/HashCodeEquals #Java/Immutability #SRS

# Why is `String` a common choice for `HashMap` keys?

> [!abstract] Short answer
> **`String` matches what `HashMap` asks of a key: content `equals` / `hashCode` that cannot change.** The class javadoc: strings are constant after creation and can be shared. Two `String`s with the same characters are the same map key even if they are not the same object. That is the opposite of `byte[]` / `char[]`. Interning is **not** why this works; `HashMap` uses `equals`, not `==`. [[What requirements apply to keys used in a HashMap]]

## Stable content equality

`Map` lookup is `(k1==null ? k2==null : k1.equals(k2))` after `hashCode` selects a bin. `String.equals` is true iff the argument is a `String` with the same character sequence. `String.hashCode` is the documented polynomial `s[0]*31^(n-1) + … + s[n-1]` (`0` for empty), so equal strings have equal hashes. Nothing in that pair is allowed to change later: JLS §10.9, a `String`’s contents never change, while a `char[]` has mutable elements. The `Map` mutable-key clause therefore does not apply. [[Why are mutable keys such as byte arrays risky in a HashMap]]

```java
map.put(new String("id"), "v");
map.get(new String("id"));   // "v" — equals, not ==
map.get("id");               // "v" — same sequence
```

**Listing 1.** Conceptual lookup. Distinct instances with the same characters are one key. [[Why should arbitrary objects not be compared with double equals in Java]] is why `==` is the wrong test here.

```d2
direction: down
need: "HashMap key needs\nstable equals + hashCode" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
str: "String\nimmutable, content equals\nhash from characters" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
arr: "byte[] / char[]\nidentity equals\nmutable cells" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
need -> str
need -> arr
```

**Fig. 1.** Common is not “the JVM interned it.” Common is a value type the table can look up by text.

`String` implements `Comparable`. `HashMap` may use comparison order among `Comparable` keys to break ties in tree bins; that is a secondary help when many hashes collide, not the reason to pick `String`. Boxed primitives (`Integer`, `Long`) are the same pattern for numeric ids. OpenJDK 21 is `public final class String`. [[Why is a byte array a poor or unsafe choice for a HashMap key]]

## What is not the reason

`String.intern` canonicalizes by `equals` so `s.intern() == t.intern()` iff `s.equals(t)`. Literals are interned. `HashMap` does not intern keys and does not need `==`. Two non-interned equal strings still `get`.

The public `hashCode` formula does **not** say “computed at construction.” OpenJDK caches the polynomial in `hash` / `hashIsZero` on the **first** `hashCode()` call for that instance: if `hash` is still `0` and `hashIsZero` is false, it computes from the immutable `value` bytes, then writes **either** `hash` **or** `hashIsZero`. The copy constructor `String(String)` copies those fields if they were already filled; ordinary construction leaves `hash == 0`. Immutability makes that cache legal (the computation is idempotent and derived from immutable state). It is a later-call speed-up, not why `HashMap` accepts the key. [[Why is java.lang.String immutable and final]]

`HashMap` also stores the mixed hash on the **node** at `put` (resize does not call `key.hashCode()` again). A lookup `get(other)` still hashes `other`; a new equal `String` pays the polynomial once, then caches on *itself*. [[Can two equal String objects both be keys in an IdentityHashMap]]

`StringBuilder` is a mutable character sequence and **does not override `equals`**. Its javadoc warns that `Comparable` without `equals` is inconsistent; care if used as a `SortedMap` key. As a `HashMap` key it is identity, like an array. Call `toString()` and use the `String`.

> [!warning] “String is interned, so HashMap is O(1) identity”
> Dispersion still comes from `String.hashCode`, then `equals` on the bin. The pool does not replace that. `equalsIgnoreCase` is not `equals`; `"A"` and `"a"` are two keys. `IdentityHashMap` is the `==` map. Do not claim the hash is computed in every constructor.

> [!tip] Interview answer
> **`String` is immutable and compares by character sequence, with a matching `hashCode`. Copies look up; mutation cannot invalidate the mapping. OpenJDK caches `hashCode` after the first call (`hash` / `hashIsZero`), not at `new`. That is why it is the usual key, unlike `byte[]` or `StringBuilder`. Interning is optional and unused by `HashMap`.**
