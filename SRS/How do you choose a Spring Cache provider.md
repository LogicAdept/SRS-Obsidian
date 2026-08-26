<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS

# How do you choose a Spring Cache provider?

> [!abstract] Short answer
> Match **topology and policies** to the **store**, not to `@Cacheable`. **One JVM, production local** → **Caffeine** (size/expire). **Several nodes sharing entries** → **Redis** (or another clustered JCache). **Tests / first spike** → Boot **Simple** concurrent map. **TTL, heap limits, disk** are **provider** settings — the abstraction does not define them.

## Topology first, then policies

Spring *How can I Set the TTL/TTI/Eviction policy*: the abstraction is **not** an implementation. ConcurrentHashMap has **no** eviction to expose; Caffeine/Redis/JCache do. Configure those on the **`CacheManager` bean** or native config. Multi-process: *Understanding the Cache Abstraction* — copy-per-node may suffice if data is static; **mutations** need a **propagation** story (shared store).

Boot: Simple is **great for getting started**, **not really recommended for production**. Auto-detect order: [[What cache providers does Spring Cache support]].

| Need | Typical `CacheManager` | Why |
| --- | --- | --- |
| Unit/slice tests, demo | `ConcurrentMapCacheManager` / Simple | Fast, zero deps; **unbounded**, **no TTL** |
| Production, **single** instance | `CaffeineCacheManager` | Local; spec for max size / expire |
| **Several** app instances, shared keys | `RedisCacheManager` | One Redis; Boot auto-config if Redis is on |
| JSR-107 product already in use | `JCacheCacheManager` | Ehcache 3, Hazelcast, Infinispan, … |
| Chain / missing region in tests | `CompositeCacheManager` + no-op fallback | Dummy cache instead of missing store |

```d2
direction: down
q: "Shared across nodes?" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
redis: "Redis / clustered JCache" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
local: "Need TTL or max size?" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
caf: "Caffeine" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}
map: "Simple map (dev/test)" {
  width: 220
  height: 50
  style.fill: "#ffebee"
}

q -> redis: "yes"
q -> local: "no"
local -> caf: "yes"
local -> map: "no"
```

**Fig. 1.** Interview sketch — still verify the product’s docs (disk overflow, `sync`, serialization). Wiring: [[How do you implement caching in Spring]].

Cache **what is expensive and stable enough**. Rapidly changing rows need **short TTL** or **`@CacheEvict`**, or they should not be cached. Hibernate **first-level** cache is the persistence `EntityManager` — **not** this choice.

> [!warning] Simple map in production
> No expire, no max size → heap growth; no cluster → **split brain** caches. Boot says read the **provider** documentation once you pick one.

> [!warning] Ehcache “disk” is not a Spring switch
> Ehcache 3 is **JCache**. Disk/heap mix lives in **Ehcache XML/config**, not on `@Cacheable`.

> [!tip] Interview answer
> **Pick the `CacheManager` for topology: Caffeine in one process, Redis when nodes must share, concurrent map only for tests.** TTL and eviction are configured on the provider. Spring Cache is cache-aside AOP, not Hibernate L1/L2.
