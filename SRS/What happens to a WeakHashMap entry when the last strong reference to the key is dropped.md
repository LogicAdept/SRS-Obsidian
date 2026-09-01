<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/WeakHashMap #Java/JVM/Memory #Java/JVM/GarbageCollector #SRS

# What happens to a `WeakHashMap` entry when the last strong reference to the key is dropped?

> [!abstract] Short answer
> **The mapping becomes eligible to disappear — it is not deleted on that assignment.** If the key is no longer strongly **or** softly reachable, it is weakly reachable: the collector may clear the `WeakReference` and enqueue it. A later `get`/`put`/`size`/iteration **polls** the queue and unlinks the row. `System.gc()` does not promise that. A remaining local (`final Key key2`) or a value that points back at the key keeps the entry.

## Dropping the last ordinary ref is not `remove()`

`WeakHashMap`: an entry is automatically removed when its key is no longer in ordinary use. The mapping does not keep the key alive. After the key is discarded, the entry is effectively gone. “Discarded” is the collector’s job, on its schedule. [[How does WeakHashMap work]] [[What is WeakHashMap used for]]

Reachability (`java.lang.ref`): weakly reachable means **neither strongly nor softly** reachable, only through weak refs. Clearing the last **strong** local is necessary but not sufficient if a `SoftReference` still points at the key — `get` can still hit. The map then `poll`s a `ReferenceQueue` on access and expunges. Between enqueue and poll, `size()` may still count the stale row. [[How does WeakHashMap use ReferenceQueue]]

```d2
direction: down
drop: "key1 = null" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
gc: "GC may clear WeakReference\nand enqueue (not promised)" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
exp: "next map access polls\nand unlinks the entry" {
  width: 280
  height: 80
  style.fill: "#c8e6c9"
}

drop -> gc
gc -> exp
```

**Fig. 1.** Three steps. The dump’s printout is the *end* of that chain, not `key1 = null` itself.

```java
WeakHashMap<Object, String> w = new WeakHashMap<>();
Object key1 = new Object();
final Object key2 = new Object();
w.put(key1, "ACTIVE");
w.put(key2, "INACTIVE");

key1 = null;
System.gc(); // hint only — may no-op; collection is unspecified

// if GC ran and expunge happened, iteration may show only key2 → INACTIVE
// key2 is still strongly reachable (the local), so that row must stay
```

**Listing 1.** Conceptual dump sample. `key2` survives because the local is a strong ref, not because `WeakHashMap` made that key strong. `key1`’s row *may* be gone after GC + poll. [[How do you attach extra data to an object with WeakHashMap]]

Values are strong: a sidecar that refers to its key pins it, so dropping your local does nothing. The **null key** uses a static sentinel and is never weakly collected. [[Does WeakHashMap allow null keys or values]] [[Why not build a SoftHashMap on SoftReferences the way WeakHashMap uses WeakReferences]]

> [!warning] `System.gc()` then assert the size
> The class does not contract that `gc()` collects the key or that expunge has run. Tests that `print` only `INACTIVE` after `gc()` are illustrating a possible outcome. Keep a live local and that mapping **must** remain. Do not treat two puts as “one strong key and one weak key” inside the map — both keys are weak; only *your* remaining refs differ.

> [!tip] Interview answer
> **The entry is not removed at `key = null`.** If nothing strong or soft refers to the key, the GC may clear the weak ref and enqueue it; the map drops the row on a later access. `System.gc()` is a hint. A still-reachable local or a value that points at the key keeps the mapping.
