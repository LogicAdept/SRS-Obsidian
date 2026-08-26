<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Library/Reactor #SRS

# What is the difference between Project Reactor and WebFlux?

> [!abstract] Short answer
> **Reactor** is a **JVM reactive library** (`reactor-core`): **`Mono` (0..1)** and **`Flux` (0..N)** implement Reactive Streams **`Publisher`**, with operators and back pressure. **WebFlux** is Spring’s **reactive HTTP module** (`spring-webflux`). It **depends on Reactor internally**, exposes `Mono`/`Flux` on web APIs, and adds servers, codecs, controllers, and `WebClient`. You can use Reactor **without** WebFlux; WebFlux **cannot** run without Reactor as a core dependency.

## Library vs web framework

Reactor 3: fully non-blocking foundation for the JVM; composable sequences (`Flux` / `Mono`); implements Reactive Streams. Cardinality: [[What is the difference between Project Reactor Mono and Flux]].

Spring WebFlux *Reactive API*: Reactor is the **library of choice**, developed with Spring. Operators support **non-blocking back pressure**. WebFlux *Reactive Libraries*: **`spring-webflux` depends on `reactor-core`** and uses it to compose async logic.

| | **Project Reactor** | **Spring WebFlux** |
| --- | --- | --- |
| Artifact | `reactor-core` (plus `reactor-netty` for I/O) | `spring-webflux` on `spring-web` |
| Job | Operators, schedulers, `Publisher` contract | HTTP: `HttpHandler`, `DispatcherHandler`, annotated + functional endpoints, `WebClient` |
| Types you write | `Mono` / `Flux` anywhere (batch, messaging, tests) | Controllers / routers that **return** those types; framework **subscribes** |

Rule of thumb for WebFlux APIs: **input** may be any `Publisher`; **internally** it becomes a Reactor type; **output** is `Flux` or `Mono`. A raw `Publisher` is treated as **0..N** (unknown cardinality). If you know 0..1 vs 0..N, wrap with **`Mono.from(publisher)`** or **`Flux.from(publisher)`** so codecs can encode correctly.

Annotated controllers: **`ReactiveAdapterRegistry`** adapts RxJava 3, Kotlin coroutines, Mutiny (and extras you register). You still need Reactor on the classpath.

```java
// Reactor only — no web stack
Mono<String> id = Mono.just("42");

@RestController
public class Ids {
    @GetMapping("/id")
    public Mono<String> id() {
        return Mono.just("42"); // WebFlux subscribes when writing the response
    }
}
```

**Listing 1.** Conceptual — same `Mono`; only the second snippet is WebFlux. Returning publishers: [[How do you implement a reactive REST controller in WebFlux]].

```d2
direction: down
rx: "reactor-core\nMono / Flux / Scheduler" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
wf: "spring-webflux\nHTTP + WebClient" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
net: "Reactor Netty\n(optional I/O)" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}

rx -> wf
net -> wf: "Boot default server"
```

**Fig. 1.** WebFlux is HTTP on top of Reactor, not a rename of Reactor. Module overview: [[What is Spring WebFlux]]. Streams: [[How does Spring WebFlux handle backpressure]].

MVC can **return** Reactor types and call **`WebClient`** without switching the server to WebFlux.

> [!warning] “WebFlux types” are Reactor types
> `Mono`/`Flux` live in **`reactor.core.publisher`**. WebFlux is the **web adapter** that subscribes and writes HTTP.

> [!warning] Passing a raw `Publisher` hides cardinality
> WebFlux then assumes **0..N**. Wrap with `Mono.from` / `Flux.from` when you know the size — it affects encoding.

> [!warning] RxJava on a controller does not remove Reactor
> Adaptation is for **annotated** methods. Core WebFlux still **requires** `reactor-core`.

> [!tip] Interview answer
> **Reactor is the reactive engine (`Mono`/`Flux`). WebFlux is Spring’s non-blocking web framework that uses that engine for HTTP.** You can run Reactor in a worker or a test with no servlet/Netty. You cannot ship WebFlux without Reactor; other libraries plug in through `Publisher` / `ReactiveAdapterRegistry`.
