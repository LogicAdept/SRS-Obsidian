<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/WeakHashMap #Java/JVM/Memory #SRS

# Why not build a `PhantomHashMap` on `PhantomReference`s the way `WeakHashMap` uses `WeakReference`s?

> [!abstract] Short answer
> **Because a map key must be retrievable, and a phantom referent never is.** `PhantomReference.get()` always returns `null` so the object cannot be resurrected. `WeakHashMap` needs `WeakReference.get()` (until the GC clears it) to run `equals`/`hashCode` and to expose `keySet`. Phantom refs are for **post-mortem cleanup** (`Cleaner`), not for canonicalizing mappings. There is no JDK `PhantomHashMap`.

## What `WeakHashMap` actually needs from the reference

`java.lang.ref`: soft = memory-sensitive caches, weak = canonicalizing mappings that do not pin keys, phantom = post-mortem cleanup. `WeakHashMap` is the weak case: each key is the referent of a `WeakReference`; the table polls a `ReferenceQueue` on access to drop stale entries. [[What is WeakHashMap used for]]

Lookup is still `Objects.equals(lookup, k)`. That `k` has to come back out of the reference object while the mapping is live.

```text
WeakReference.get()       referent, or null after GC clears it
PhantomReference.get()    always null (referent must stay inaccessible)
```

**Listing 1.** Java SE 21. `Reference.get()` in general returns the referent unless cleared. `PhantomReference` overrides that to **always** `null`, even before enqueue. `refersTo(obj)` can test identity without strengthening; it does not give you a key for `equals`.

```d2
direction: down
lookup: "map.get(key)" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
weak: "WeakRef.get() → k\nequals(key, k)" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
phant: "PhantomRef.get() → null\ncannot compare / cannot iterate keys" {
  width: 340
  height: 90
  style.fill: "#ffebee"
}

lookup -> weak
lookup -> phant
```

**Fig. 1.** A hash map of keys is a lookup structure. Phantom refs are a cleanup token. [[What is the difference between HashMap and WeakHashMap]]

When the collector decides an object is phantom reachable, it **atomically clears** phantom references to it, then enqueues those registered with a queue. That is the opposite of “keep the key around for `get`.” The point is that a reclaimable object stays reclaimable.

## What you would use phantom refs for instead

Schedule work after the object is otherwise dead: `Cleaner`, or your own `ReferenceQueue` consumer. You associate **side data** (a resource id, a native handle) with the `PhantomReference` subclass or with the queue entry — not a `Map` whose keys are the dying objects.

A `null` queue means the phantom reference is **never** enqueued. That is useless as a “GC removed this entry” signal. `WeakHashMap` depends on that queue.

Soft refs are a different question: `get()` still returns the object until the GC clears them under memory pressure. The JDK still has no `SoftHashMap`; [[Why not build a SoftHashMap on SoftReferences the way WeakHashMap uses WeakReferences]] is why copying the `WeakHashMap` recipe there is also a bad fit.

> [!warning] “Weaker than weak, so a better WeakHashMap”
> Reachability order is strong → soft → weak → phantom. Weaker does not mean “same map, more GC.” Phantom is a **lifecycle notification** after finalization, with an API that forbids retrieving the referent. Building `keySet`/`get` on `get() == null` always is not a map.

> [!tip] Interview answer
> **`WeakHashMap` works because a live weak ref still yields the key for `equals` and iteration, and a queue tells the table the GC dropped it. `PhantomReference.get()` is always `null` by contract — cleanup, not lookup. There is no phantom-key `HashMap` in the JDK; use `Cleaner` / a `ReferenceQueue` for post-mortem work.**
