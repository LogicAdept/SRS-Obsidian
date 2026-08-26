<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Spring/Framework/WebMvc #SRS

# What is the difference between Spring MVC and Spring WebFlux?

> [!abstract] Short answer
> **Spring MVC** (`spring-webmvc`) is the **Servlet, blocking-I/O** web stack: a **large thread pool** may wait on JDBC/HTTP. **Spring WebFlux** (`spring-webflux`, since **5.0**) is the **reactive, non-blocking** stack: a **small event-loop pool** and **Reactive Streams**. Both offer **`@Controller` / `@RestController`**. WebFlux also has **functional endpoints** and **reactive `@RequestBody`**. They are **sibling modules**, not “faster MVC.” Pick by **blocking vs non-blocking dependencies**, not by QPS slogans.

## Concurrency and I/O

Spring *Overview* / *Concurrency Model*:

| | **MVC** | **WebFlux** |
| --- | --- | --- |
| API | Servlet (blocking I/O by default) | `HttpHandler` / `WebHandler`; Netty or Servlet **non-blocking I/O** |
| Threads | Large pool **absorbs blocking** | Small **event-loop** workers; **do not block** |
| Body args | Blocking `@RequestBody` | **Reactive** `@RequestBody` (`Mono`/`Flux`) |
| Client | **`RestClient`** (blocking); `RestTemplate` **deprecated in 7.0** | **`WebClient`** (reactive; usable from MVC too) |
| Boot default server | Tomcat | **Reactor Netty** |

Both can run on **Tomcat/Jetty** — **how** they use the container differs. Mixing servlet `Filter`s into WebFlux I/O is **advised against**.

Dump “thread-per-request vs event-loop” is the **usual picture**, not a JVM guarantee (virtual threads change the MVC side — [[When should you use WebFlux versus Spring MVC versus virtual threads]]).

```d2
direction: right
mvc: "MVC\nblocking Servlet I/O\nlarge pool" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
wf: "WebFlux\nnon-blocking I/O\nsmall loop" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Same mapping annotations; different **runtime contract**. Async MVC vs this stack: [[What is the difference between Spring MVC async and WebFlux]]. Dual classpath: [[Can you use Spring MVC and WebFlux in the same application]].

> [!warning] Not generally faster
> Spring *Performance*: reactive usually **does not** speed CRUD. Win is **scale with few threads when there is I/O latency**.

> [!warning] Blocking persistence → MVC
> JPA/JDBC: Spring’s **usual** choice is MVC. Offloading JDBC does not make the architecture reactive.

> [!warning] Boot both starters → MVC
> Adding `starter-webflux` next to `starter-web` is for **`WebClient`**, not two servers.

> [!tip] Interview answer
> **MVC is Servlet blocking I/O with a large pool; WebFlux is non-blocking Reactive Streams with a small loop.** Same `@RestController` family. WebFlux adds reactive bodies and `RouterFunction`. Choose from dependencies and I/O style, not “WebFlux is faster.”

## See also

- [[What is Spring WebFlux]]
- [[When should you not use WebFlux]]
- [[When should you use WebFlux versus Spring MVC versus virtual threads]]
- [[What is the difference between Spring MVC async and WebFlux]]
- [[What is the difference between RestTemplate WebClient and RestClient]]
- [[Can you use Spring MVC and WebFlux in the same application]]
- [[How does the WebFlux event loop work]]
- [[What is Reactor Netty]]
