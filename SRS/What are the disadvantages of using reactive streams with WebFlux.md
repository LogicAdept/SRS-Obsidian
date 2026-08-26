<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Library/Reactor #SRS

# What are the disadvantages of using reactive streams with WebFlux?

> [!abstract] Short answer
> You pay **harder code, debugging, and libraries**. Imperative MVC is easier to write and debug; most existing APIs **block**. WebFlux adds a **steep learning curve**, **slightly more CPU** for non-blocking work, and a **tiny event-loop pool** that **starves** if you touch JDBC/JPA on it. R2DBC is **not** reactive JPA. For many apps the switch is **unnecessary**.

## Harder programming model

Spring WebFlux *Applicability*:

- **Imperative** is the easiest way to **write, understand, and debug**.
- **Most libraries historically block** — maximum choice stays on MVC.
- **Blocking persistence or networking (JPA, JDBC)** → **MVC** for common architectures. Offload with `publishOn` / `subscribeOn` is possible but you are **not** using a non-blocking stack.
- **Large team:** **steep learning curve** to non-blocking, functional, declarative pipelines. Start with **`WebClient` inside MVC**; **measure**. Spring expects the full shift is **often unnecessary**.

*Performance*: non-blocking can **slightly increase processing time**. It is **not generally faster**. Benefits need **I/O latency** — [[What are the benefits of Spring WebFlux]]. CPU-bound work still needs cores and **must not** sit on the loop — [[How does the WebFlux event loop work]].

```d2
direction: down
cost: "Mono / Flux pipelines" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
dbg: "Request hops threads\nharder stack traces" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
dep: "JDBC / JPA / sync SDK\nblocks the small pool" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}

cost -> dbg
cost -> dep
```

**Fig. 1.** The model’s costs are **cognition, tooling, and blocking deps** — not “WebFlux is slow CRUD” as a slogan. When to skip: [[When should you not use WebFlux]].

## Logging and data access

A **single request can run on several threads**, so a **thread id does not identify the request**. WebFlux prefixes logs with a **request id** (`ServerWebExchange.getLogPrefix()` / `LOG_ID_ATTRIBUTE`). Blocking loggers fight the event loop; async loggers **can drop** messages.

JDBC is a **fully blocking** API (R2DBC’s reason to exist). **R2DBC / Spring Data R2DBC** is a **different** stack: reactive SQL, **not** Hibernate sessions, lazy graphs, or classic JPA. Need those → stay on MVC — [[Why should you not use JDBC on the WebFlux event loop]].

```java
Mono.fromCallable(() -> jdbcTemplate.queryForObject(sql, args, mapper))
        .subscribeOn(Schedulers.boundedElastic());
```

**Listing 1.** Conceptual escape hatch — JDBC still **blocks a worker**; the loop is only spared. You keep two concurrency models. Offload details: [[How do you offload blocking work in WebFlux]].

Java **21+** virtual threads on **MVC** can cover **many concurrent blocking calls** without rewriting to `Flux` — different trade-off, not a WebFlux feature.

> [!warning] Blocking on the loop is worse than MVC
> MVC sized a **large pool** for waits. WebFlux sized a **small** one assuming **no** waits. JDBC/`block()` on Netty threads is an **outage** pattern, not “a bit slower”.

> [!warning] R2DBC is not “JPA but reactive”
> No session, no lazy load as in Hibernate. “Limited reactive DB” means **you cannot keep the JPA programming model** and stay non-blocking.

> [!warning] Stack traces lie if you think in servlet threads
> Operators hop threads. Debug with the **request log prefix** and Reactor assembly dumps (`Hooks.onOperatorDebug()` / checkpoint), not `Thread.currentThread()` alone.

> [!tip] Interview answer
> **Disadvantages: steep reactive learning curve, harder debugging, and a library world that still blocks.** JPA/JDBC push you back to MVC; R2DBC is not Hibernate. You also spend a bit more CPU to stay non-blocking. If MVC already works, Spring says you probably should not switch.
