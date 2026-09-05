<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/WeakHashMap #Java/JVM/Memory/References #Java/HashCodeEquals #SRS

# How do you attach extra data to an object with `WeakHashMap`?

> [!abstract] Short answer
> **Use the object as a weak key and the extra data as the value.** That is a registry: metadata without a new field on the class, and without the table pinning the object. While some other strong (or soft) reference to the object exists, `get` works. When the object is no longer in ordinary use, the collector can discard the key and the mapping disappears. It is not an LRU cache.

## Sidecar map, not a field and not a cache

`WeakHashMap` holds keys with weak references. The mapping does not keep the key alive. When the key is no longer in ordinary use, the entry is effectively removed. The collections tutorial calls this a **registry-like** structure: the entry is useful only while the key is still reachable from some thread *outside* the map. [[What is WeakHashMap used for]]

Weak references exist for canonicalizing mappings that must **not** prevent reclaim. Soft references are the memory-sensitive **cache** tool. Mixing those jobs is the usual interview mistake. [[Why not build a SoftHashMap on SoftReferences the way WeakHashMap uses WeakReferences]] [[How do you build a cache with invalidation using LinkedHashMap]]

```d2
direction: down
app: "Ordinary strong ref\n(the live object)" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
key: "Key object" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
map: "WeakHashMap\nweak key, strong value\n(sidecar data)" {
  width: 280
  height: 90
  style.fill: "#ffe0b2"
}

app -> key
map -> key: weak
```

**Fig. 1.** Drop the last ordinary reference and the sidecar row may go with the object. The map must not be the last strong ref.

```java
final class Widget { /* no extra field */ }

WeakHashMap<Widget, String> extra = new WeakHashMap<>();
Widget w = new Widget();
extra.put(w, "painted-blue");
extra.get(w); // "painted-blue" while w is strongly reachable

w = null;
// after GC, extra no longer has that mapping
// extra.get(??) — you no longer have a key to look up
```

**Listing 1.** Conceptual: attach data without changing `Widget`. Lookup needs the same instance (the class is aimed at identity-`equals` keys). After the last ordinary ref is gone, there is nothing left to `get`.

Values are **strong**. If the sidecar object points back at the key (directly or through other entries), that key never becomes weakly reachable and the row never drops. The documented workaround is `put(key, new WeakReference(value))` and unwrap on `get`. Prefer keys whose `equals` is `==`, so a discarded key cannot be recreated as a look-alike. [[How does WeakHashMap use ReferenceQueue]] [[Does WeakHashMap allow null keys or values]]

An `IdentityHashMap` (or `HashMap`) **pins** keys. Debugger-style object-to-meta tables that must keep the object alive are the identity-map job, not this one. [[What is IdentityHashMap for]] [[Can IdentityHashMap be used as a cache]]

Not synchronized. `size()` is a snapshot and may still count entries the GC has already logically discarded. The null key is a sentinel and is **not** weakly collected.

> [!warning] “Put it in WeakHashMap, that is my cache”
> You can look the sidecar up only while you still hold the key (or a soft ref to it). Weakly reachable means not strongly **and** not softly reachable. This is not LRU and not `removeEldestEntry`. If the value graph points at the key, you built a pin, not a registry.

> [!tip] Interview answer
> **Put the object as a weak key and the extra data as the value — a registry of sidecar fields you could not add to the class.** The map does not keep the object alive; when nothing else refers to it, the entry can disappear. Hold a strong reference while you still need `get`. Do not use this as an LRU cache, and do not let values point back at the key.
