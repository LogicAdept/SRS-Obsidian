<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Set/HashSet #SRS

# What is the difference between `HashMap` and `HashSet`?

> [!abstract] Short answer
> **Different types: key→value vs unique elements.** `HashMap` is a `Map`. `HashSet` is a `Set` (`Collection`). The set is **implemented as** a `HashMap`: elements are keys, every value is one dummy object. Same hash table, unspecified order, expected constant-time if hashes spread, one `null`, not synchronized. You still pick the API by whether you need a value beside the key.

## Contract vs backing store

`Map`: maps keys to values; no duplicate keys. Not a `Collection`; you walk it through `keySet` / `values` / `entrySet`. [[What is the main purpose of the Map interface]]

`Set`: a `Collection` with no pair `e1.equals(e2)`, and at most one `null`. `add` returns whether the set changed.

`HashSet` javadoc: the set is backed by a hash table, **actually a `HashMap` instance**. How that dummy works: [[How is HashSet implemented in terms of HashMap]].

```text
                 HashMap                         HashSet
type             Map<K,V>                        Set<E>  (Collection)
stores           unique keys → values            unique elements
lookup           get(key) → V or null            contains(e) → boolean
insert           put(k, v) → old V               add(e) → boolean (true if new)
null             one null key, null values       one null element
order            unspecified                     unspecified
time             expected O(1)*                  expected O(1)*
iteration cost   capacity + size                 backing capacity + size
```

**Listing 1.** Java SE 21 class javadocs. `*` assuming hashes disperse among buckets. `HashSet` iteration is explicitly the backing `HashMap`’s capacity plus the set’s size.

```d2
direction: down
api: "Need a value per key?" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
hm: "HashMap\nput / get" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
hs: "HashSet\nadd / contains" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
back: "same HashMap bins\nkeys + PRESENT" {
  width: 260
  height: 80
  style.fill: "#ffe0b2"
}

api -> hm: yes
api -> hs: no
hs -> back
```

**Fig. 1.** Choose `Map` vs `Set` first. `HashSet` is not a second hash-table codebase; it is a `HashMap` with a hidden value.

## What stays the same

Both default to capacity 16 and load factor 0.75 (`HashSet`’s constructors size the backing map). Both permit `null` in the key/element slot. Both are unsynchronized; wrap with `synchronizedMap` / `synchronizedSet`. Both have `newHashMap` / `newHashSet` (since 19) to size from expected count. Duplicate `put` replaces the value; duplicate `add` leaves the set unchanged and returns `false` — that is the map’s equal-key overwrite of `PRESENT` with `PRESENT`.

A mutable object used as a `HashMap` key or a `HashSet` element is the same hazard. [[What requirements apply to keys used in a HashMap]]

> [!warning] `HashSet` is not “HashMap without values”
> There is always a value object (`PRESENT`). You cannot retrieve user values from a `HashSet`, and `get` is not on `Set`. Conversely, `HashMap.keySet()` is a **view**, not a `HashSet` you own. Do not use `HashMap` as a set by stuffing dummy values by hand unless you mean `Collections.newSetFromMap`.

> [!tip] Interview answer
> **`HashMap` is a map: unique keys, each with a value, `put`/`get`. `HashSet` is a set: unique elements, `add`/`contains`, no user values. The set is a `HashMap` whose keys are the elements and whose values are one shared dummy. Same hashing, order, null, and concurrency story; different interface.**
