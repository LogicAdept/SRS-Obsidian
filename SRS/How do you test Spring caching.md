<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS

# How do you test Spring caching?

> [!abstract] Short answer
> Use a **real in-memory `CacheManager`** (`ConcurrentMapCacheManager` is documented for tests), call the **proxied** `@Cacheable` bean twice with the same key, and assert the **collaborator** ran **once** (or inspect `cache.get(key)`). To **disable** caching in a suite, Boot **`@AutoConfigureCache`** or **`spring.cache.type=none`** installs a **no-op** manager.

## Prove a hit without mocking the proxy wrong

`ConcurrentMapCache` / `ConcurrentMapCacheManager` javadoc: **useful for testing**. Keep `@EnableCaching` in the test context (or a dedicated `@TestConfiguration`) and a map manager so AOP actually puts.

```java
@SpringBootTest
class BookServiceCacheTests {

    @Autowired BookService books;       // Spring proxy
    @MockitoBean Catalog catalog;       // collaborator inside @Cacheable
    @Autowired CacheManager cacheManager;

    @Test
    void secondCallIsCacheHit() {
        ISBN isbn = new ISBN("123");
        Book book = new Book(isbn);
        given(catalog.load(isbn)).willReturn(book);

        books.findBook(isbn);
        books.findBook(isbn);

        then(catalog).should(times(1)).load(isbn);
        assertThat(cacheManager.getCache("books").get(isbn).get()).isEqualTo(book);
    }
}
```

**Listing 1.** Conceptual: verify **`catalog.load`**, not `books.findBook` with Mockito `times(1)` on a **real** `@Autowired` service — that bean is not a mock. Internals: [[How does Cacheable work internally]].

Evict: call `@CacheEvict` method, then assert `cache.get(key)` is empty and the next find hits the catalog again.

```d2
direction: down
proxy: "Test → BookService proxy" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
hit: "2nd call: Cache.get hit\ncatalog not invoked" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

proxy -> hit
```

**Fig. 1.** The interceptor must run — `this.findBook` inside the target still skips cache.

**Turn caching off (Boot *Testing*):** `@AutoConfigureCache` replaces auto-config with **no-op**; or `spring.cache.type=none`. Put `@EnableCaching` on an **isolated** `@Configuration` so **slice tests** do not require a cache. Custom `CacheManager` in production config: override it in `@SpringBootTest` or the tests always hit Redis.

> [!warning] `verify(bookService, times(1))` on a real bean
> Mockito cannot count invocations on an un-mocked `@Autowired` service. Spying a `@Cacheable` bean plus a Spring proxy is fragile. Mock the **inner** dependency instead.

> [!warning] No-op manager looks like “caching is broken”
> `@WebMvcTest` / slices plus `@AutoConfigureCache` or missing `@EnableCaching` → every call hits the method. That is **by design** for tests that should not keep cache state.

> [!warning] Self-invocation in the test double
> If the test calls a non-cached facade that uses `this.cached()`, you never exercise AOP — [[Why might the Cacheable annotation not work]].

> [!tip] Interview answer
> **Test with `ConcurrentMapCacheManager`, go through the Spring proxy, and assert the expensive collaborator ran once.** Boot can swap in a no-op manager with `@AutoConfigureCache` so other tests ignore cache. Do not Mockito-verify the cached service bean itself unless it is a mock.
