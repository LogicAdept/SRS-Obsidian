<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/HashCodeEquals #SRS

# Does `IdentityHashMap` use the `hashCode` method?

> [!abstract] Short answer
> **Not the key’s `hashCode()`.** [[What is IdentityHashMap for]] buckets with **`System.identityHashCode(key)`** and treats keys as the same only when **`k1 == k2`**. It never calls the key’s overridden `hashCode` or `equals`. That is why the class javadoc says it intentionally violates the usual `Map` contract.

## What it calls instead

Java SE 21 documents constant-time `get` / `put` **assuming** `System.identityHashCode` disperses keys among buckets. OpenJDK’s private `hash` helper is exactly that call; there is no `key.hashCode()` on the lookup path.

```text
HashMap key path
  bucket ← key.hashCode() (then mix)
  same key ← equals (after == / null)

IdentityHashMap key path
  bucket ← System.identityHashCode(key)
  same key ← (k1 == k2)
```

**Listing 1.** Documented contrast with a normal `Map` such as [[What is the difference between HashMap and IdentityHashMap]].

```d2
direction: down
key: "Key instance" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
skip: "key.hashCode()\nkey.equals()\nNOT called" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
id: "System.identityHashCode(key)\n→ table index" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
eq: "Match only if\nk1 == k2" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}

key -> skip
key -> id
id -> eq
```

**Fig. 1.** Hashing still happens; the identity hash replaces the object’s `hashCode`, and reference equality replaces `equals`.

`System.identityHashCode(x)` returns the same `int` the default `Object.hashCode` would return, **even if** the class overrides `hashCode`. For `null` it returns `0`. So an override that returns a constant, or an expensive value-based hash, does not change where an `IdentityHashMap` places that object. See [[How are hashCode and equals implemented in java.lang.Object]] for the default hash that identity hash mirrors.

```java
record Box(int id) {
    @Override
    public int hashCode() {
        return 42; // ignored by IdentityHashMap
    }
}

Box a = new Box(1);
Box b = new Box(1);
IdentityHashMap<Box, String> map = new IdentityHashMap<>();
map.put(a, "A");
map.get(b); // null — a != b, even though equals would be true
map.get(a); // "A"
```

**Listing 2.** Conceptual: equal `Box` values are still two keys; the overridden `hashCode` is unused for placement.

The map’s own `hashCode()` (the `Map` object’s hash) also XORs `identityHashCode` of each key and value. That is the map’s contract bookkeeping, not “call the key’s `hashCode`.”

> [!warning] “No `hashCode`” does not mean “no hashing”
> Interview shorthand “`IdentityHashMap` does not use `hashCode`” means it skips **`Object.hashCode` / overrides**. It still hashes with **`System.identityHashCode`**. Without that, there would be no bucket index.

> [!warning] Overriding `equals` changes nothing here
> [[Does overriding equals change IdentityHashMap lookup]] — still only `==`. Two equal instances remain two keys unless they are the same reference.

> [!tip] Interview answer
> **No — not the key’s `hashCode()`.** `IdentityHashMap` uses **`System.identityHashCode`** for buckets and **`==`** for key identity, so it ignores overridden `hashCode`/`equals` and admits it breaks the normal `Map` equality contract. Use it only when reference identity is the rule you want.
