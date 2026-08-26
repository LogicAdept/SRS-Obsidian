<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Boot/AutoConfiguration #SRS

# What is `spring-boot-starter-cache`?

> [!abstract] Short answer
> **The Boot starter that pulls cache auto-configuration dependencies** — notably **`spring-context-support`** (JCache and Caffeine adapters). It does **not** turn caching on and is **not** a cache product. You still add **`@EnableCaching`**. With no extra library, Boot’s **Simple** in-memory map is used.

## Dependencies and hooks, not a store

Spring Boot *Caching*: use the starter to add basic caching dependencies quickly. If you add libraries **manually**, you must include **`spring-context-support`** to use **JCache or Caffeine** support.

Then:

1. **`@EnableCaching`** on a `@Configuration` class (Boot warns against putting it on the main application class if slice tests should stay cache-free)
2. Annotate service methods (`@Cacheable`, `@CachePut`, `@CacheEvict`)
3. Optionally add **Caffeine**, **Redis** (`spring-boot-starter-data-redis`), or a **JSR-107** provider so auto-config picks a real `CacheManager`

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
```

**Listing 1.** Maven coordinate. Gradle: `implementation 'org.springframework.boot:spring-boot-starter-cache'`. Enablement: [[What is the EnableCaching annotation]]. Default manager: [[Which CacheManager does Spring Boot configure by default]].

```d2
direction: down
st: "spring-boot-starter-cache\nspring-context-support" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
en: "@EnableCaching" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
prov: "optional Caffeine / Redis / JCache" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}

st -> en -> prov
```

**Fig. 1.** Auto-config of `CacheManager` runs only with enablement; the starter alone is not enough.

`CacheManagerCustomizer` beans can tweak the auto-configured manager before it is fully initialized. Tests: `@AutoConfigureCache` or `spring.cache.type=none` for no-op.

> [!warning] Not Redis, not a cluster
> The starter does **not** start a distributed cache. Default remains **one JVM’s concurrent map** until another provider is on the classpath (or `spring.cache.type` is set).

> [!warning] Starter ≠ `@EnableCaching`
> Without the annotation, `@Cacheable` methods are ordinary calls even with the starter on the classpath.

> [!tip] Interview answer
> **`spring-boot-starter-cache` is Boot’s dependency pack for the cache abstraction** (`spring-context-support`). You still enable caching with `@EnableCaching`. Pair it with Caffeine or Redis for production; otherwise you get an in-memory map.
