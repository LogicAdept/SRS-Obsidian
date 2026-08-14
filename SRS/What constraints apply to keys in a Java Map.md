<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #Java/HashCodeEquals #Java/Immutability #SRS

# What constraints apply to keys in a Java `Map`?

> [!abstract] Short answer
> **Every `Map` forbids duplicate keys and treats key identity as `equals` (implementations may skip `equals` when hashes already differ).** Mutating a stored key so `equals` changes is unspecified. A map must not contain itself as a key. Extra limits are **per implementation**: `null`, type, `Comparable`, enum-only. `K` is a reference type; primitives only via boxing. Hash-table specifics: [[What requirements apply to keys used in a HashMap]].

## What every `Map` requires

`containsKey` / `get` use `(key==null ? k==null : key.equals(k))`. At most one such mapping. Inserting an ineligible key throws an unchecked exception, typically `NullPointerException` or `ClassCastException`. Querying one may throw or return `false` — that choice is optional in the `Map` spec.

```text
all Maps
  unique keys (put replaces)
  equals (unless the class documents ==)
  do not mutate equals-relevant state in place
  not the map itself as a key
  K is a reference type
```

**Listing 1.** Interface floor. [[Can a primitive value be used directly as a Map key in Java]] is `Map<int,V>` vs `Integer`.

```d2
direction: down
all: "Map contract\nequals, unique, stable" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
impl: "This implementation\nnull? type? order?" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
ok: "put succeeds" {
  width: 180
  height: 55
  style.fill: "#e8f5e9"
}
no: "NPE / CCE / unspecified" {
  width: 240
  height: 60
  style.fill: "#ffebee"
}
all -> impl
impl -> ok
impl -> no
```

**Fig. 1.** Interface rules plus the concrete class. Do not assume `HashMap`’s `null` key on every `Map`.

## What the class adds

```text
HashMap / LinkedHashMap / WeakHashMap
  one null key allowed
Hashtable / ConcurrentHashMap / Map.of, copyOf
  no null key  (Map.of: no null value; duplicate keys → IAE)
TreeMap / SortedMap
  Comparable or Comparator; mutually comparable (else CCE)
  ordering should be consistent with equals
  null key: NPE if natural order, or comparator forbids null
EnumMap
  keys from one enum type; no null key
IdentityHashMap
  == not equals (documented Map-contract violation)
```

**Listing 2.** Restrictions from the class javadocs (Java SE 21). `TreeMap.put`: NPE if the key is null and the map uses natural ordering or a comparator that does not permit null keys.

`Comparable.compareTo(null)` is specified to throw `NullPointerException`. Sorted maps compare with `compareTo` / `compare`, not `equals`, so two keys with `compareTo == 0` are one key even if `equals` is false — then the map fails the `Map` contract. [[What is the time complexity of lookup by key in a TreeMap]]

> [!warning] “Keys just need hashCode”
> That is hash tables. `TreeMap` does not look up by `hashCode`. `EnumMap` does not take an arbitrary `Object`. Unmodifiable factories reject `null` even though `HashMap` does not.

> [!tip] Interview answer
> **Interface: unique keys, `equals`, don’t mutate equality state, no self-as-key, reference-type `K`. Then name the class: `null` or not, `Comparable` for `TreeMap`, enum for `EnumMap`, `==` only for `IdentityHashMap`.**
