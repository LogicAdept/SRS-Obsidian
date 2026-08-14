<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/HashMap #Java/HashCodeEquals #SRS

# What is `IdentityHashMap` for?

> [!abstract] Short answer
> **The rare `Map` that treats keys as equal only when they are the same reference (`==`), not when `equals` is true.** The class javadoc says it is **not** a general-purpose `Map`: it intentionally violates the `Map` contract. Typical uses are a node table for serialization or deep copy, and a table of proxy objects. For ordinary value keys, use `HashMap`.

## When reference equality is the point

`IdentityHashMap` compares keys **and values** with `==`. Two objects that `equals` would merge stay two keys if they are distinct instances. Overriding `equals`/`hashCode` does not change that. Buckets use `System.identityHashCode`. [[What is the difference between HashMap and IdentityHashMap]] is the full contrast. [[Why should arbitrary objects not be compared with double equals in Java]] is why this map is the exception, not the default.

The javadoc names two jobs:

```text
1. Topology-preserving graph walks
   serialization, deep copy
   node table: "have I already processed THIS object?"
   must not collapse distinct instances that happen to be equals

2. Proxy / identity tables
   e.g. a debugger: one proxy per live object
```

**Listing 1.** Intended uses from the `IdentityHashMap` class javadoc (Java SE 21).

```d2
direction: down
a: "Object A" {
  width: 160
  height: 60
  style.fill: "#e3f2fd"
}
b: "Object B\nequals(A), A != B" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
tab: "IdentityHashMap\nnode table" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}

a -> tab: seen
b -> tab: also seen\n(separate entry)
```

**Fig. 1.** A copy or serializer must record both nodes. `HashMap` would keep one mapping and skip `B`.

That is the opposite of `WeakHashMap`’s advice (identity-`equals` keys so a discarded key cannot be recreated). `IdentityHashMap` keys are ordinary strong references; they stay until you remove them. [[What is WeakHashMap used for]] is GC eviction, not `==`.

## What it is not for

It is not a faster `HashMap`. An implementation note about linear probing vs chaining is not a reason to drop `equals`. Expected constant-time `get`/`put` still assumes the **identity** hash spreads. Default expected maximum size is 21, not `HashMap`’s capacity/load-factor pair.

It is not a `Set` of values. `get(new Key(id))` misses if that `new` is not the same instance you `put`. Null key and null values are allowed. Not synchronized. No iteration-order guarantee. Since 1.4.

> [!warning] “I want unique objects, so IdentityHashMap”
> Unique **values** still belong in `HashMap`/`HashSet` with a correct `equals`/`hashCode`. Use `IdentityHashMap` only when two `equals` objects must remain distinct because they are different instances in a graph.

> [!tip] Interview answer
> **`IdentityHashMap` is for identity-sensitive tables: graph copy, serialization node maps, per-instance proxies. Keys match with `==` and `identityHashCode`. It implements `Map` but admits it violates the `equals` contract. Default maps stay `HashMap`.**
