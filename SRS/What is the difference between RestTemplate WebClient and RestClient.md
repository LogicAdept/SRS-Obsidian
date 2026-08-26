<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Framework/WebFlux #SRS

# What is the difference between `RestTemplate`, `WebClient`, and `RestClient`?

> [!abstract] Short answer
> **`RestTemplate`** is the classic **blocking** template API — **deprecated in Spring Framework 7.0** in favor of **`RestClient`**. **`RestClient`** (Framework **6.1**) is the modern **synchronous fluent** client; a built instance is **safe for multiple threads**. **`WebClient`** (Framework **5.0**) is the **non-blocking, reactive** client (`Mono`/`Flux`, streaming). MVC + virtual threads → **`RestClient`**. WebFlux / streaming → **`WebClient`**. Do **not** `.block()` `WebClient` on an event-loop thread.

## Three clients, two I/O models

Spring *REST Clients*:

| Client | I/O | API | When |
| --- | --- | --- | --- |
| **`RestClient`** | Blocking | Fluent `get()` / `retrieve()` | Imperative apps; successor to `RestTemplate` |
| **`WebClient`** | Non-blocking | Fluent + Reactor | Reactive/streaming; also “sync” via `.block()` at a **boundary** |
| **`RestTemplate`** | Blocking | Template methods (`getForObject`, …) | Legacy; **remove in a future Framework version** |

Dump “maintenance mode” is **stale**: 7.0 **deprecates** it. It was **not** deprecated in Spring 5 (5.0 added `WebClient` as the **reactive** alternative).

```java
RestClient rest = RestClient.create();
Person person = rest.get()
        .uri("https://example.org/persons/{id}", id)
        .retrieve()
        .body(Person.class);

Mono<Person> reactive = WebClient.create("https://example.org")
        .get().uri("/persons/{id}", id)
        .retrieve()
        .bodyToMono(Person.class);
```

**Listing 1.** Conceptual — blocking fluent vs reactive decode. `WebClient`: [[What is WebClient]]. Decode: [[What is bodyToMono]].

```d2
direction: down
rt: "RestTemplate\n(deprecated 7.0)" {
  width: 240
  height: 55
  style.fill: "#ffebee"
}
rc: "RestClient\nblocking fluent" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
wc: "WebClient\nreactive / streaming" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}

rt -> rc: "migrate"
```

**Fig. 1.** Tests use **`WebTestClient`**, not production `WebClient` as MockMvc — [[What is the difference between WebClient and WebTestClient]].

> [!warning] `.block()` is not the WebFlux path
> REST Clients allow synchronous `WebClient` use; **never block in a WebFlux (or MVC) controller** — return the `Mono`. Loop: [[What happens if you call block on a WebFlux event loop]].

> [!warning] Built `WebClient` vs Boot `WebClient.Builder`
> The **built** client is immutable. Boot’s **`WebClient.Builder` is prototype / stateful** — inject the builder, `build()` per customization — [[Is WebClient thread-safe]].

> [!tip] Interview answer
> **`RestClient` replaces `RestTemplate` for blocking HTTP (deprecated in Framework 7).** `WebClient` is the reactive client from 5.0. Same fluent *feel*, different thread model. Virtual-thread MVC still wants `RestClient`, not Netty `WebClient` on the event loop.

## See also

- [[What is WebClient]]
- [[How do you call an external API from a WebFlux application]]
- [[Is WebClient thread-safe]]
- [[What is the difference between WebClient and WebTestClient]]
- [[What is the difference between Spring MVC and Spring WebFlux]]
- [[When should you use WebFlux versus Spring MVC versus virtual threads]]
