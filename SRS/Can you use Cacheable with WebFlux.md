<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Framework/WebFlux #SRS

# Can you use `Cacheable` with WebFlux?

> [!abstract] Short answer
> **Yes, from Spring Framework 6.1.** `@Cacheable` on a method that returns **`Mono`/`Flux` caches the emitted values**, not the publisher instance. Hits come back as `Mono`/`Flux` backed by a `CompletableFuture`. Before 6.1 (or if you restore 6.0 mode), the interceptor cached the **`Publisher` object** — a useless hit that never re-subscribes to I/O.

## What 6.1 actually stores

Spring *Declarative Annotation-based Caching*: cache annotations **adapt** `CompletableFuture` and reactive return types.

* **`Mono<T>`:** cache `T` when the publisher emits; a hit is a `Mono` over a `CompletableFuture`.
* **`Flux<T>`:** **collect into a `List`**, cache that list when complete; a hit is a `Flux` over the cached list.

```java
@Service
public class BookService {

    @Cacheable("books")
    public Mono<Book> findBook(ISBN isbn) {
        return this.books.findById(isbn); // values cached as of 6.1
    }

    @Cacheable("booksByAuthor")
    public Flux<Book> findBooks(String author) {
        return this.books.findByAuthor(author); // collected List in the cache
    }
}
```

**Listing 1.** Conceptual methods from Spring Framework cache reference. Enable with `@EnableCaching` as usual. Controllers that return these publishers: [[How do you implement a reactive REST controller in WebFlux]].

The cache must support **`CompletableFuture` retrieval**. `ConcurrentMapCacheManager` adapts; **`CaffeineCacheManager` needs `setAsyncCacheMode(true)`**. `sync = true` can compute once on concurrent misses.

```d2
direction: down
pre: "Spring ≤ 6.0\ncache the Mono/Flux instance" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
post: "Spring 6.1+\ncache emitted T / List<T>" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

pre -> post: "reactive adaptation"
```

**Fig. 1.** Dump-era “`@Cacheable` is broken on WebFlux” describes the **old** behavior. Restore it only with `spring.cache.reactivestreams.ignore=true` (`CacheAspectSupport`) — not recommended.

`Mono.cache()` / `Flux.cache()` are **Reactor operators** that replay one subscription to downstreams; they are not the Spring `Cache` abstraction. reactor-extra **`CacheMono`/`CacheFlux` are deprecated** (removed from extra 3.6+) — prefer Spring 6.1 annotations or a cache with native async + stampede protection (Caffeine).

> [!warning] Coarse grain — not for live streams
> Spring: annotation caching is **not** for sophisticated composition and **backpressure**. A `@Cacheable` `Flux` waits until **complete**, then stores the **whole list**. Infinite SSE is a bad fit — [[How do you implement Server-Sent Events in WebFlux]], [[How does Spring WebFlux handle backpressure]].

> [!warning] Multiple cache names vs late misses
> Async/reactive lookup may **not consult every named cache** when the miss is determined late (for example Redis). Multiple names make sense mainly with **early** misses (Caffeine).

> [!warning] Blocking `.block()` to “make `@Cacheable` work”
> That puts JDBC-style blocking on the event loop — [[What happens if you call block on a WebFlux event loop]]. Use 6.1 reactive adaptation instead.

> [!tip] Interview answer
> **On Spring 6.1+, yes: `@Cacheable` caches `Mono`/`Flux` emissions, not the publisher.** `Flux` is collected to a `List`. Need a `CompletableFuture`-capable cache (Caffeine async mode). Do not use it for infinite streams; old 6.0 code really did cache the `Mono` object.
