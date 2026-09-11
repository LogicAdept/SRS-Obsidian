<!--
reps: 0
priority: 0
-->
#Caching #SystemDesign #SRS

# What simple approach would you use to implement an in memory cache

> [!abstract] Short answer
> The simple correct shape is a bounded concurrent map with a time-to-live: get checks expiry (and the map only), set stores value plus expiry timestamp, a size bound evicts least-recently-used entries. In Java that means a `ConcurrentHashMap` with timestamps for a tiny case, or Caffeine — the library behind Spring's default cache manager — when eviction, TTL and hit-rate accounting must be production-grade.

## The minimal hand-rolled version

Two invariants drive the design: reads must not block each other, and stale values must not outlive their TTL. A `ConcurrentHashMap<K, ExpiryBox<V>>` where the box carries value plus `expiresAtMillis` gives lock-free reads; `get` compares the timestamp and removes the entry on expiry (cache-aside semantics: the origin stays the source of truth). Bounding memory needs eviction — the classic O(1) answer is a map plus a doubly linked list of access order, the LinkedHashMap trick: access moves the node to the tail, eviction removes from the head. The vault already dissects that construction in [[Can LinkedHashMap fully implement an LRU cache]] and the invalidation-aware variant in [[How do you build a cache with invalidation using LinkedHashMap]].

```java
class TtlCache<K, V> {
    private record Box<V>(V value, long expiresAt) {}
    private final ConcurrentHashMap<K, Box<V>> map = new ConcurrentHashMap<>();

    V get(K key) {
        Box<V> b = map.get(key);
        if (b == null) return null;                       // miss
        if (System.currentTimeMillis() > b.expiresAt) {   // expired
            map.remove(key, b);                           // remove only if unchanged
            return null;
        }
        return b.value;                                   // hit
    }
    void put(K key, V value, long ttlMillis) {
        map.put(key, new Box<>(value, System.currentTimeMillis() + ttlMillis));
    }
}
```

**Listing 1.** A TTL cache on ConcurrentHashMap: expiry checked on read, removal via the two-argument remove to avoid clobbering a concurrent refill.

## When to reach for a library

The hand-rolled version misses the parts that hurt under load: size-based and time-based eviction working together, admission control against one-shot keys, and lock-free statistics. Caffeine's documentation groups eviction exactly as size-based, time-based (expire after write or access) and reference-based, and implements an adaptive W-TinyLFU policy that keeps a higher hit rate than plain LRU under skewed access. Spring's caching abstraction builds on it — [[How do you choose a Spring Cache provider]] compares the providers and [[How do you implement caching in Spring]] wires the annotations, while a fleet-scale version graduates to [[How would you explain distributed caching and cache hierarchies at a high level]].

> [!warning] Lazy expiration still holds memory until touched
> Checking TTL on read leaves expired entries resident if nobody reads them. A periodic sweep or an eviction-capable structure is required, otherwise the "simple" cache leaks memory until it crashes the process.

> [!tip] Interview answer
> I would start with a bounded ConcurrentHashMap of value-plus-expiry boxes: reads are lock-free, expiry is checked on get, and TTL bounds staleness. If size or hit-rate control matters, use Caffeine — it adds size/time eviction and W-TinyLFU admission — and expose it through Spring's cache abstraction rather than reinventing statistics.
