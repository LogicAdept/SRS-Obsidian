<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# What are the benefits of Spring WebFlux?

> [!abstract] Short answer
> The documented win is **concurrency with a small, fixed event-loop pool and less memory**, so the app **scales more predictably under load** — **if there is I/O latency**. Extra benefit: **compose remote calls without blocking** (`WebClient` + Reactor). WebFlux is **not** generally **faster** CPU-for-CPU; non-blocking work can even cost a bit more processing time.

## Scale with few threads — when I/O waits

Spring WebFlux *Performance*:

- Reactive/non-blocking **generally does not make applications run faster**.
- It **can** in cases such as **`WebClient` running remote calls in parallel**.
- Doing work the non-blocking way takes **more programming effort** and can **slightly increase** processing time.
- **Key expected benefit:** scale with a **small, fixed number of threads** and **less memory** → more **resilient, predictable** load behavior.
- You **observe** that only with **latency** (slow or mixed network I/O). Then differences can be **dramatic**.

*Why WebFlux exists*: handle concurrency with **few threads** and **fewer hardware resources**; a common API for **Netty-style** runtimes; **annotated controllers and functional endpoints**. Back pressure is Reactive Streams — [[How does Spring WebFlux handle backpressure]]. Event loop: [[How does the WebFlux event loop work]].

The dump’s “thousands of connections on 4–8 threads” is **not** a Framework number. Worker count is **about CPU cores (Netty min 4)**; connections multiplex on those workers **only while nothing blocks**.

```d2
direction: right
mvc: "MVC\nlarge pool absorbs blocking" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
wf: "WebFlux\nsmall loop; callbacks on I/O" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

mvc -> wf: "same latency-heavy load\n(if nothing blocks)"
```

**Fig. 1.** Benefit is **thread and memory headroom under wait**, not a quicker `SELECT`. Skip it when that wait is missing — [[When should you not use WebFlux]].

## Compose I/O without occupying a request thread

Spring: in an **MVC** app that already calls remotes, try **`WebClient`** and **return reactive types**. **More latency per call** or **interdependent calls** → **larger** benefit. You do not have to rewrite the server to Netty to get that client-side win — [[What is WebClient]].

```java
Mono<Person> person = client.get()
        .uri("/person/{id}", personId)
        .retrieve()
        .bodyToMono(Person.class);

Mono<List<Hobby>> hobbies = client.get()
        .uri("/person/{id}/hobbies", personId)
        .retrieve()
        .bodyToFlux(Hobby.class)
        .collectList();

return Mono.zip(person, hobbies, (p, h) -> Map.of("person", p, "hobbies", h));
```

**Listing 1.** Conceptual Spring `WebClient` pattern — two calls overlap; **return** the `Mono` (do not `.block()` in a controller).

Also: **streaming** (`Flux`, SSE) on non-blocking writes; **client and server share** Reactor Netty loops when both use Netty; **same mapping annotations** as MVC plus **reactive `@RequestBody`**.

> [!warning] Not “faster CRUD”
> Without network wait, you mostly pay **pipeline complexity**. JDBC/JPA on the loop **cancels** the scalability story.

> [!warning] Benefits assume you never block the loop
> `Thread.sleep`, JDBC, `.block()` on event-loop threads turn a small pool into a **stall**. Then you have MVC’s blocking problem **without** MVC’s large pool.

> [!warning] Steep curve is a real cost
> Spring calls the shift to non-blocking, functional code a **steep learning curve**. If you cannot name the latency you are buying, stay on MVC.

> [!tip] Interview answer
> **WebFlux’s benefit is scaling idle I/O with few threads and less memory — not higher CRUD QPS.** You see it when calls wait on the network; `WebClient` can overlap those calls. Blocking persistence or a tiny, fast CRUD app does not get that win.
