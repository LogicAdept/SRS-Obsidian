<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/Hashtable #SRS

# What need did `HashMap` address compared to older maps?

> [!abstract] Short answer
> **A Collections Framework hash table that is a `Map`, not a `Dictionary`, without a lock on every call, and with nulls allowed.** Before 1.2 the hash map you had was `Hashtable` (since 1.0). Java 2 retrofitted it as a `Map` but left it synchronized and null-hostile. `HashMap` (1.2) is the unsynchronized, null-friendly replacement the `Hashtable` page still names.

## What “older” was

`Dictionary` is the abstract 1.0 parent of `Hashtable`. The class javadoc: **obsolete**; new code should implement `Map`, not extend `Dictionary`. Keys and values are non-null objects. Iteration is `Enumeration` (`keys` / `elements`), not `Iterator`.

`Hashtable` is that dictionary: hash table, non-null keys and values, `put`/`get` synchronized on the instance. As of Java 2 v1.2 it **also** implements `Map`, so it is in the Collections Framework — unlike the new implementations, it stays synchronized.

```text
1.0  Dictionary + Hashtable     lock, no nulls, Enumeration
1.2  Map interface
     HashMap                    no lock, null key/values, fail-fast views
     Hashtable retrofitted      still lock, still no nulls
```

**Listing 1.** Timeline from the class javadocs (Java SE 21). `HashMap` is “roughly equivalent to `Hashtable`, except that it is unsynchronized and permits nulls.”

```d2
direction: down
need: "Need a hash Map?" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
hm: "HashMap\n(the 1.2 default)" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
ht: "Hashtable\nlegacy API / Properties" {
  width: 280
  height: 70
  style.fill: "#ffe0b2"
}
chm: "ConcurrentHashMap\nwhen the lock was the point" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}

need -> hm
need -> ht
need -> chm
```

**Fig. 1.** The need was a general-purpose `Map`, not a second `Hashtable`. Concurrent writers are a later, different need.

## Three gaps `HashMap` closed

**Framework type.** `Map` is the Collections hash-map contract (unique keys, `get`/`put`, three views). `HashMap` implements all optional map operations. `Dictionary.put` still forbids nulls in the obsolete API.

**Default concurrency.** Most maps are not shared by writers. A monitor on every `get`/`put` was the wrong default. `Hashtable` itself says: if you do not need thread safety, use `HashMap`; if you want a highly concurrent map, use `ConcurrentHashMap`. [[Is java.util.HashMap thread safe]]

**Nulls.** `HashMap` permits one `null` key and `null` values. `Hashtable`/`Dictionary` reject both (`NullPointerException`).

Pairwise API and bins: [[What is the difference between HashMap and Hashtable]]. Drawbacks of keeping the legacy class: [[How would you explain drawbacks of the legacy Hashtable class]].

`Properties` still extends `Hashtable`. That is leftover API, not a reason to pick `Hashtable` for a new `Map`.

> [!warning] `HashMap` did not make maps concurrent
> It removed the coarse lock. Unsynchronized concurrent mutation is still unsupported. Do not tell the story as “1.2 replaced `Hashtable` with a thread-safe `HashMap`.” The documented concurrent replacement is `ConcurrentHashMap`. `LinkedHashMap` / `TreeMap` solved order, not this gap.

> [!tip] Interview answer
> **`HashMap` is the 1.2 Collections `Map` that replaced `Hashtable` for ordinary use: same hash-table idea, but unsynchronized, `null` key and values allowed, `Map` views instead of `Dictionary`/`Enumeration`. `Hashtable` remains for legacy and `Properties`. If the old lock was load-bearing, use `ConcurrentHashMap`, not `HashMap`.**
