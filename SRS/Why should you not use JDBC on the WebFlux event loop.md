<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/JDBC #SRS

# Why should you not use JDBC on the WebFlux event loop?

> [!abstract] Short answer
> **JDBC is blocking I/O.** WebFlux (and Netty-style servers) run requests on a **small fixed event-loop pool** that must not block. Calling JDBC on those threads stalls other requests. Prefer **Spring MVC** for JDBC/JPA stacks, a **reactive driver (R2DBC)**, or **offload** blocking work to another scheduler — never run bare JDBC on the loop.

## Why the event loop cannot wait on JDBC

Spring’s WebFlux overview states that non-blocking servers assume applications **do not block**, so they use a **small, fixed-size** thread pool of event-loop workers. JDBC APIs such as **`ResultSet.next()`** wait on the network and the database — they hold the calling thread until data arrives.

If that thread is an event-loop worker, **every other connection sharing the loop waits**. Under load this looks like latency spikes or a “frozen” reactive server even though CPU is idle.

The same docs say: if your dependencies are **blocking persistence APIs (JPA, JDBC)**, **Spring MVC is usually the better fit**. You *can* wrap blocking calls, but you are not getting the benefit of a non-blocking stack.

```d2
direction: right
req: "HTTP request" {
  width: 140
  height: 60
  style.fill: "#e3f2fd"
}
loop: "Event-loop thread" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
jdbc: "JDBC blocks\n(ResultSet / query)" {
  width: 200
  height: 70
  style.fill: "#fce4ec"
}
starve: "Other requests\nstall on same loop" {
  width: 200
  height: 70
  style.fill: "#fce4ec"
}

req -> loop -> jdbc -> starve
```

**Fig. 1.** Blocking JDBC on an event-loop worker starves concurrent reactive traffic.

## Safer options

| Approach | Role |
|---|---|
| **Spring MVC + JDBC/JPA** | Default when the data layer is blocking |
| **R2DBC / Spring Data R2DBC** | Non-blocking SQL API and `ReactiveCrudRepository` — not JPA (no lazy loading, entity graphs, or classic L2 cache) |
| **Offload** | Switch work with Reactor **`publishOn` / `subscribeOn`** onto an I/O scheduler (for example **`Schedulers.boundedElastic()`**), or configure WebFlux **blocking execution** with an `AsyncTaskExecutor` |

```java
Mono.fromCallable(() -> jdbcTemplate.queryForObject(sql, args, mapper))
    .subscribeOn(Schedulers.boundedElastic());
```

**Listing 1.** Conceptual escape hatch — JDBC runs on a bounded elastic pool, not on Netty’s event-loop threads. Prefer redesigning the stack when JDBC is the primary store.

> [!warning] Bare `fromCallable` is not enough
> Wrapping JDBC in **`Mono.fromCallable(...)`** without **`subscribeOn`** (or an equivalent executor) still executes the callable on the **subscribing** thread — often the event loop. The rule remains: **do not block Netty / event-loop threads**. See [[How does the WebFlux event loop work]] and [[How do you offload blocking work in WebFlux]].

> [!tip] Interview answer
> JDBC blocks the calling thread; WebFlux event loops are few and must stay non-blocking, so JDBC on the loop freezes other requests. Use MVC for JDBC/JPA, R2DBC for reactive SQL, or explicitly offload blocking calls — never call JdbcTemplate directly on the event loop.
