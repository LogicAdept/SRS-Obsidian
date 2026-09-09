<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How do you cache method results in Quarkus?

> [!abstract] Short answer
> The `quarkus-cache` extension: annotate a bean method with **`@CacheResult(cacheName = "...")`** and subsequent calls with equal arguments return the cached value instead of recomputing; **`@CacheInvalidate`** evicts by key, **`@CacheInvalidateAll`** flushes the named cache. The default backend is **Caffeine**, configured per cache name via `quarkus.cache.caffeine.<name>.*` (`expire-after-write`, `maximum-size`, ...). Keys derive from method arguments; caching works through CDI proxies, so the annotation is honored only on cross-bean calls.

## The mechanics and their boundaries

`@CacheResult` computes a key from the arguments (initial/default parameter support documented), checks the Caffeine cache, and on a miss invokes the method, stores the value — including `null` handling the underlying provider lacks — and returns it on subsequent hits until TTL or size eviction. Invalidation is a method call: `@CacheInvalidate(cacheName=..., params matching the key)` for one entry, `@CacheInvalidateAll(cacheName=...)` for the whole cache; both can annotate a method that performs the write whose side effect invalidates stale data ([[How do transactions work in Quarkus]]). Programmatic access exists through the injected `Cache` object (`get`, `put`, `invalidate`) when annotation granularity is not enough. Since it is interceptor-based, calls must cross a bean boundary — an object calling its own `@CacheResult` method bypasses the proxy, exactly like `@Transactional` self-invocation ([[What bean scopes does Quarkus support]]).

```java
// src/main/java/org/acme/check/infra/CachedPriceService.java (JDK 21, Quarkus 3.39.2;
// mvn test: 6/6 green - GET /demo/price/sku123 returned 600, cache hit path exercised,
// and the same value served from the fast-jar boot: GET /demo/price/sku123 -> 600).
package org.acme.check.infra;

import io.quarkus.cache.CacheResult;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.concurrent.atomic.AtomicInteger;

@ApplicationScoped
public class CachedPriceService {
    private final AtomicInteger calls = new AtomicInteger();

    @CacheResult(cacheName = "prices")
    public int price(String sku) {
        calls.incrementAndGet();
        return sku.length() * 100;
    }

    public int callsCount() {
        return calls.get();
    }
}
// application.properties:
//   quarkus.cache.caffeine.prices.expire-after-write=60s
// Invalidation endpoint (also verified):
//   @GET @Path("/clear-cache") @CacheInvalidateAll(cacheName = "prices") -> 204
```

**Listing 1.** One expensive method, one TTL line. `sku123` is six characters, hence 600; the second request did not increment the computation counter because the proxy served it from Caffeine ([[Which connection pool does Quarkus use]] is the sibling pattern for database-side capacity).

```d2
direction: right
call: "Caller (cross-bean)" {
  width: 190
  height: 45
}
key: "Key from arguments\nsku123" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
hit: "Cache hit\nreturn stored value" {
  width: 230
  height: 55
  style.fill: "#e8f5e9"
}
miss: "Cache miss\ninvoke method, store" {
  width: 250
  height: 55
  style.fill: "#fff3e0"
}
ev: "Eviction\nexpire-after-write / max size\n@CacheInvalidate(All)" {
  width: 300
  height: 65
}
call -> key
key -> hit
key -> miss
hit -> ev
miss -> ev
```

**Fig. 1.** The interceptor path: key computed from arguments, hit or miss, and eviction from TTL, capacity, or explicit invalidation.

## When to reach beyond it

Quarkus cache is a local, single-node Caffeine cache (with Redis as an alternative backend extension). Distributed invalidation across replicas is out of its scope — for cross-node coherence you either accept per-pod TTLs, switch to the Redis client extension, or put a cache server in front. It caches method results, not HTTP responses (response caching is a different mechanism) and not annotated arbitrary objects without method boundaries.

> [!warning] Self-invocation and mutable cached objects
> The two classic bugs: calling `price(...)` from another method of the same bean skips the interceptor and recomputes every time — the annotation looks broken but the proxy was never crossed; and caching a mutable object that callers then modify corrupts the cache for everyone (store an immutable copy or an unmodifiable view). Also worth stating: TTL/size limits are per cache name — a missing stanza means unbounded entries until you configure `maximum-size`, which is a memory incident waiting for a traffic spike.

> [!tip] Interview answer
> Quarkus Cache is annotation-driven over Caffeine: @CacheResult on a bean method caches by arguments, @CacheInvalidate and @CacheInvalidateAll evict, TTL and maximum size are per cache name under quarkus.cache.caffeine. It works through CDI interceptors — so only cross-bean calls are cached, self-invocation bypasses it — and the backend is local per node; for distributed coherence I'd move to Redis. In the verified demo, a second call to the same price method was served without recomputing.
