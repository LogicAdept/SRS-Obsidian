<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# How do you implement caching in Spring?

> [!abstract] Short answer
> **Enable annotation-driven caching, register a `CacheManager`, then mark service methods.** `@EnableCaching` on a `@Configuration` class plus a `CacheManager` bean; `@Cacheable` / `@CachePut` / `@CacheEvict` on **public** methods of a Spring bean. Boot: add **`spring-boot-starter-cache`**, still add **`@EnableCaching`**, optionally a provider (Caffeine, Redis, JCache).

## Two pieces: declaration and store

Spring *Understanding the Cache Abstraction*: you must (1) declare which methods cache and (2) configure the backing store. Enablement registers AOP — [[What is the EnableCaching annotation]]. The store is a **`CacheManager`** — there is no Framework default.

**Plain Spring:**

```java
@Configuration
@EnableCaching
class CacheConfig {

    @Bean
    CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("books");
    }
}

@Service
public class BookService {

    @Cacheable("books")
    public Book findBook(String isbn) {
        return catalog.load(isbn);
    }

    @CacheEvict(cacheNames = "books", key = "#isbn")
    public void deleteBook(String isbn) {
        catalog.delete(isbn);
    }
}
```

**Listing 1.** Conceptual setup from Framework enablement + `@Cacheable` examples. `ConcurrentMapCacheManager("books")` pre-creates that region; a no-arg manager creates regions on first use. Map store has **no TTL** — [[How do you configure TTL for Spring Cache]].

**Spring Boot:** `spring-boot-starter-cache` brings `spring-context-support`. Auto-config runs **only with `@EnableCaching`**. No extra library → in-memory concurrent maps. Add Caffeine, Redis, or a JSR-107 provider and Boot selects it (or set `spring.cache.type`). Override by declaring your own `CacheManager` bean.

```d2
direction: down
en: "@EnableCaching +\nCacheManager bean" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
svc: "@Cacheable / @CachePut / @CacheEvict\non public bean methods" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
hit: "proxy: get → skip or invoke+put" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}

en -> svc -> hit
```

**Fig. 1.** Same path as [[What is the Spring cache abstraction]]. XML alternative: `<cache:annotation-driven/>` plus a `cacheManager` bean.

Use `@CachePut` when the method must always run and refresh the cache; `@CacheEvict` when data changes. Several operations on one method: `@Caching`. Custom keys: SpEL `key` or a `KeyGenerator`.

> [!warning] Public + through the proxy
> In default **proxy** mode, cache annotations on **non-public** methods do not apply (no error). `this.findBook(...)` and `@PostConstruct` self-calls skip the interceptor — [[Why might the Cacheable annotation not work]].

> [!warning] Boot does not enable caching by the starter alone
> `spring-boot-starter-cache` is dependencies + auto-config **hooks**. Without `@EnableCaching`, annotations stay inert. Boot also advises against putting `@EnableCaching` on the main application class if slice tests should not require a cache.

> [!warning] Same-context beans only
> Enablement in a child `WebApplicationContext` does not advise `@Service` beans in the parent context.

> [!tip] Interview answer
> **Turn on `@EnableCaching`, provide a `CacheManager`, annotate public service methods.** Boot still needs `@EnableCaching`; the starter plus a cache library only chooses the store. Calls must go through the Spring proxy, or caching never runs.
