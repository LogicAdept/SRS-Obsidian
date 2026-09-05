<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/WeakHashMap #Java/JVM/Memory/References #Caching #SRS

# Why not build a `SoftHashMap` on `SoftReference`s the way `WeakHashMap` uses `WeakReference`s?

> [!abstract] Short answer
> **Different jobs.** Weak refs are for canonicalizing maps that must **not pin** keys. Soft refs are for **memory-sensitive caches**, cleared at the collector’s discretion under memory demand. Copying `WeakHashMap`’s “entry extends a reference to the key” recipe would keep unused keys softly alive until the heap is in trouble — the opposite of `WeakHashMap`. The JDK has `WeakHashMap` and no `SoftHashMap`. `get()` on a live `SoftReference` still works; the problem is the **policy**, not lookup.

## Two reference types, two sentences in `java.lang.ref`

```text
soft     memory-sensitive caches
weak     canonicalizing mappings that do not prevent reclaim
phantom  post-mortem cleanup
```

**Listing 1.** Package specification (Java SE 21). `WeakHashMap` is the weak-key table. [[What is WeakHashMap used for]] Phantom keys cannot implement `Map` at all: [[Why not build a PhantomHashMap on PhantomReferences the way WeakHashMap uses WeakReferences]].

`WeakHashMap`: a mapping does not stop the key from being discarded; when the key is no longer in ordinary use, the entry is effectively removed. That is **weak** reachability.

`SoftReference`: the GC **may** clear softly reachable referents in response to memory demand. The only hard guarantee: all such soft refs are cleared before `OutOfMemoryError`. Time and order of clearance are otherwise unspecified. VMs are encouraged to bias against clearing recently created or recently used soft refs.

```d2
direction: down
unused: "Key unused elsewhere" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
weak: "WeakHashMap\nGC may drop the entry now" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
soft: "Soft-key map\nGC may keep it until memory demand" {
  width: 320
  height: 90
  style.fill: "#ffe0b2"
}

unused -> weak
unused -> soft
```

**Fig. 1.** Same “only the map still mentions this key,” two eviction clocks. [[What is the difference between HashMap and WeakHashMap]]

## What the JDK tells you to build instead

`SoftReference` javadoc: direct instances for simple caches; subclasses inside larger structures for sophisticated ones. While the referent is **strongly** reachable (actually in use), the soft ref is not cleared. A sophisticated cache can hold **strong** refs to its most recently used entries and leave the rest softly reachable for the collector.

That is not `Entry extends SoftReference<K>`. It is “strong for hot, soft for the rest,” or a `SoftReference` **value**. A cache lookup key (`String` id, integer) is usually **strong**; you do not want the map to drop the row because the id object was a throwaway.

Bounded, application-defined eviction is [[How do you build a cache with invalidation using LinkedHashMap]] (`removeEldestEntry`, access-order). That policy does not wait for OOME.

`SoftReference.get()` returns the referent until the ref is cleared — unlike `PhantomReference`. A home-grown soft-key table is possible; it would still have `WeakHashMap`-style unstable `size()`/`get`, plus VM-specific when rows vanish. That is a poor `java.util.Map` to ship next to `HashMap`.

> [!warning] “Soft is just weaker HashMap keys”
> Reachability is strong → soft → weak → phantom. Soft is **stronger** than weak: unused keys linger. Values in `WeakHashMap` are already strong; swapping only the key ref type does not give you a value cache. Do not treat `WeakHashMap` as an LRU cache either.

> [!tip] Interview answer
> **There is no JDK `SoftHashMap` because soft refs are a cache GC policy, not a “don’t pin the key” map. `WeakHashMap` drops entries when the key is otherwise unused. Soft refs may keep softly reachable objects until memory is tight, and the documented cache is strong refs for hot entries plus `SoftReference`s (or `LinkedHashMap` size eviction), not a clone of `WeakHashMap`.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В `WeakHashMap` используются WeakReferences. А почему бы не создать `SoftHashMap` на SoftReferences?**

`SoftHashMap` представлена в сторонних библиотеках, например, в `Apache Commons`.
