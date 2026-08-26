<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Library/Reactor #SRS

# How do you offload blocking work in WebFlux?

> [!abstract] Short answer
> Wrap the blocking call in **`Mono.fromCallable` (or `Flux`)** and **`subscribeOn(Schedulers.boundedElastic())`** so wait time uses a **capped worker pool**, not the Netty event loop. Spring still says blocking APIs are a **poor fit** — prefer R2DBC / reactive clients, or **MVC** for JDBC/JPA. `publishOn` only switches **downstream** operators.

## Escape hatch, not the architecture

Spring WebFlux *Concurrency Model*: non-blocking servers use a **small event-loop pool** and assume you **do not block**. If you must call a blocking library, Reactor’s **`publishOn`** / **`subscribeOn`** move work to another scheduler — an **escape hatch**, not a reason to pick WebFlux.

Reactor FAQ *How Do I Wrap a Synchronous, Blocking Call?*:

```java
Mono<String> blockingWrapper = Mono.fromCallable(() -> slowJdbcQuery())
        .subscribeOn(Schedulers.boundedElastic());
```

**Listing 1.** Conceptual Reactor pattern — `fromCallable` + `subscribeOn` immediately after the source. JDBC on the loop: [[Why should you not use JDBC on the WebFlux event loop]].

`Schedulers.boundedElastic()` is for **longer / blocking** work: dedicated workers, **capped** thread and queue size (unlike deprecated unbounded `elastic()`). `parallel()` / `single()` are **not** for blocking; `block()` there can throw `IllegalStateException` on non-blocking threads.

```d2
direction: right
loop: "Event-loop thread" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
sub: "subscribeOn\nboundedElastic" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
blk: "JDBC / file I/O\nblocks worker only" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

loop -> sub -> blk
```

**Fig. 1.** The loop thread must not sit in `ResultSet.next()`. Event loop: [[How does the WebFlux event loop work]].

| Operator | Effect |
| --- | --- |
| **`subscribeOn`** | Chooses the scheduler **where the source is subscribed**. Place it **right after** the blocking source. |
| **`publishOn`** | Replays signals on a worker; **operators below it** run there until the next `publishOn`. |

Reactor: `subscribeOn` does **not** subscribe; it only picks the scheduler for when someone does. Extra `subscribeOn` later does not relocate an upstream source the way people expect — keep one, next to `fromCallable`.

> [!warning] Offload is still blocking I/O
> You can exhaust `boundedElastic` (cap + queue) under load. Spring: you would not be making the most of a non-blocking stack — consider MVC or a reactive driver.

> [!warning] `publishOn` after a blocking `map` is too late
> If `map` already ran `jdbcTemplate.query` on the event loop, switching threads afterward does not undo that stall. Wrap the blocking source with `subscribeOn`, or `publishOn` **before** the blocking operator.

> [!warning] Do not `.block()` on the loop to “get a value”
> That is the opposite of offloading — [[What happens if you call block on a WebFlux event loop]].

> [!tip] Interview answer
> **`Mono.fromCallable(blocking).subscribeOn(Schedulers.boundedElastic())` so JDBC/files do not pin Netty threads.** `boundedElastic` is capped; `publishOn` only moves downstream work. Prefer not blocking at all — R2DBC/`WebClient` or Spring MVC for JPA.
