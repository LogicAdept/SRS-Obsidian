<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# What is the `EnableCaching` annotation?

> [!abstract] Short answer
> **`@EnableCaching` (since 3.1) turns on annotation-driven cache AOP** — it registers **`CacheInterceptor`** and the proxy (or AspectJ) advice that applies `@Cacheable` / `@CachePut` / `@CacheEvict` / `@Caching`. Put it on a **`@Configuration`** class. It is **not** a store: you still need a **`CacheManager` bean**. Without it, cache annotations are inert.

## Enablement, not storage

Spring *Enabling Caching Annotations*: declaring `@Cacheable` does **not** start caching. You enable the feature in **one** place so you can disable it by removing that line. XML equivalent: `<cache:annotation-driven/>`.

`EnableCaching` javadoc: the annotation searches for a **`CacheManager` by type** — there is **no** convention bean name and **no** default store the Framework invents. (XML `<cache:annotation-driven/>` assumes a bean named **`cacheManager`**.) Pick a manager explicitly with **`CachingConfigurer`** when more than one exists.

```java
@Configuration
@EnableCaching
class CacheConfiguration {

    @Bean
    CacheManager cacheManager() {
        return new CaffeineCacheManager();
    }
}
```

**Listing 1.** Pattern from the Framework reference / javadoc. Boot: auto-configures a `CacheManager` **only after** this annotation is present; with no cache library that is an in-memory concurrent map — [[What is the Spring cache abstraction]].

```d2
direction: down
en: "@EnableCaching on @Configuration" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
adv: "CacheInterceptor +\nproxy or AspectJ advice" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
mgr: "CacheManager bean\n(required, no Framework default)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

en -> adv
en -> mgr
```

**Fig. 1.** Enablement wires AOP; a separate bean supplies storage. Custom keys / resolvers: [[What is CachingConfigurer]].

**`mode`** defaults to **`PROXY`**: only **external** calls through the proxy are advised. **`ASPECTJ`** weaves bytecode (`spring-aspects` + compile- or load-time weaving) so `this.` calls participate. **`proxyTargetClass`** requests CGLIB subclass proxies (ignored in AspectJ mode) and upgrades **all** proxied beans, including `@Transactional`.

Spring Boot warns **not** to put `@EnableCaching` on the **main** `@SpringBootApplication` class if you want slice tests to stay cache-free; use a dedicated `@Configuration`. JSR-107 (`@CacheResult`, …) components register **only if** the JCache API and Spring’s JCache support are on the classpath — do not mix Spring and JCache annotations on the same methods.

> [!warning] Not a cache
> `@EnableCaching` does not allocate a map or Redis. Missing `CacheManager` fails at runtime. `@CacheConfig` only shares names/keys — it **does not** enable processing.

> [!warning] Same application context
> Annotation-driven setup sees `@Cacheable` beans **only in the context where it is defined**. Putting it only in a child `WebApplicationContext` skips `@Service` beans in the root context.

> [!warning] Default proxy mode skips `this`
> Local calls never hit `CacheInterceptor` — [[Why might the Cacheable annotation not work]].

> [!tip] Interview answer
> **`@EnableCaching` is the on-switch for cache AOP: it registers `CacheInterceptor` and looks up a `CacheManager` by type.** Put it on a `@Configuration` class and supply a manager bean. Without it, `@Cacheable` does nothing. Default proxy mode does not intercept self-invocation; AspectJ mode does.
