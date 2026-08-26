<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS

# How does the Spring TestContext framework cache the ApplicationContext?

> [!abstract] Short answer
> After the first load, the TestContext Framework keeps the **`ApplicationContext` in a static `ContextCache`**, keyed by **`MergedContextConfiguration`**. Later tests in the **same JVM / test suite** that declare the **same** configuration **reuse** it — one refresh, many classes. The key includes **`@ContextConfiguration` locations/classes/loader/initializers**, **`@ActiveProfiles`**, **`@TestPropertySource`**, **`@WebAppConfiguration`**, **parent hierarchy**, and **`ContextCustomizer`s** (`@MockitoBean` / `@TestBean` / `@DynamicPropertySource` / Boot `webEnvironment`, …). Default cache **max size is 32** (LRU). **`@DirtiesContext`** evicts and closes. Framework **6.1+**: a **failed** load for a key is retried only **`spring.test.context.failure.threshold`** times (default **1**), then **`IllegalStateException`**.

## Same key, same static cache

“Unique configuration” is that parameter tuple, not the test class name. Two classes with identical `@SpringBootTest` + the same profiles and bean overrides share one context. A **different** `@MockitoBean` field name, extra `@TestPropertySource`, or `@ActiveProfiles("test")` on only one class is a **new** key — a **second** refresh.

The cache is a **`static` variable**. Maven Surefire **`forkMode=always` / `pertest`** (or any per-class JVM) **clears** it; you pay a full refresh every class. Log **`org.springframework.test.context.cache` at DEBUG** for hit/miss counts. Override size with **`spring.test.context.cache.maxSize`**.

`@DirtiesContext` (class or method) means the test **mutated container state** (singleton, bean definition). Listeners **remove and close** the cached context; the next test with that key **rebuilds**. Prefer **`@Transactional` rollback** for database isolation — that **keeps** the cache. Framework: [[What is the Spring TestContext Framework]]. Evict: [[What is DirtiesContext]]. vs rollback: [[What is the difference between DirtiesContext and Transactional in tests]]. Profiles: [[What is the ActiveProfiles annotation]].

```java
@SpringBootTest
class OrderServiceTests { /* … */ }

@SpringBootTest
class PaymentServiceTests { /* … */ }
```

**Listing 1.** Conceptual: two classes, **one** cached Boot context if nothing else differs (same `webEnvironment`, no extra `@MockitoBean` / properties).

```java
@SpringBootTest
@ActiveProfiles("test")
class OrderServiceWithTestProfileTests { /* … */ }
```

**Listing 2.** Conceptual: **different** `activeProfiles` → **different** cache key. Same for `@TestPropertySource`, `@MockitoBean`, `@DynamicPropertySource`.

```d2
direction: down
key: "MergedContextConfiguration\nclasses · profiles · properties · customizers" {
  width: 360
  height: 55
  style.fill: "#e3f2fd"
}
cache: "static ContextCache\nmax 32, LRU" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
hit: "reuse ApplicationContext" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
miss: "refresh (or IllegalStateException\nif failure threshold hit)" {
  width: 300
  height: 50
  style.fill: "#ffebee"
}

key -> cache
cache -> hit: "same key"
cache -> miss: "new key / dirty / failed"
```

**Fig. 1.** `@DirtiesContext` and LRU eviction **close** a context. Shutdown of leftover contexts runs on the **`SpringContextShutdownHook`** thread.

> [!warning] Forked JVMs disable the cache
> Each process has its own static map. CI that forks **per test class** looks like “Spring tests are slow” even with identical `@SpringBootTest`.

> [!warning] `@MockitoBean` is part of the key
> Inconsistent field names for the **same** mocked type across classes create **extra** contexts. Name them the same. Boot `RANDOM_PORT` vs `MOCK` is also a **different** customizer.

> [!warning] One failed refresh poisons the key
> Default **failure threshold 1**: the next class with that config **does not retry** — **`IllegalStateException`**, “preemptively skipped.” Fix the config or raise **`spring.test.context.failure.threshold`**.

> [!tip] Interview answer
> **The TestContext Framework caches `ApplicationContext` by configuration, not by test class.** Same annotations → one refresh per suite. `@DirtiesContext` is expensive; a new profile or mock bean is a **new** cache entry. Forked Surefire and a size-32 LRU are the usual “why did it rebuild?” answers.
