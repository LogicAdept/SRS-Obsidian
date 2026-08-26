<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Framework/WebFlux #Java/Concurrency/VirtualThreads #SRS

# When should you use WebFlux versus Spring MVC versus virtual threads?

> [!abstract] Short answer
> **MVC** is the default when the app **already works**, libraries **block** (JPA/JDBC), or the team wants **imperative** code. **WebFlux** when you **already want a non-blocking stack** (streaming, many idle I/O connections, reactive all the way down). **Virtual threads** (Java **21+**, Boot `spring.threads.virtual.enabled=true`; docs **strongly recommend Java 24+**) keep **MVC/blocking** style with **cheap threads** — they are **not** WebFlux. WebFlux is **not** faster CRUD.

## Three knobs, not one ranking

Spring WebFlux *Applicability*: if MVC is fine, **do not migrate**. Blocking persistence → **MVC**. Steep reactive curve → try **`WebClient` inside MVC** first.

Boot *Virtual threads*: enable with **`spring.threads.virtual.enabled=true`**. Read JDK pinning docs. **Thread-pool properties no longer apply** (virtual threads use the JVM carrier pool). Daemons: consider **`spring.main.keep-alive=true`**.

```properties
spring.threads.virtual.enabled=true
```

**Listing 1.** Conceptual Boot switch — **servlet/MVC concurrency**, not a Netty setting. Skip WebFlux checklist: [[When should you not use WebFlux]].

```d2
direction: down
q: "I/O and libraries?" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
mvc: "Spring MVC\nblocking, simple" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
vt: "MVC + virtual threads\nJava 21+" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
wf: "WebFlux\nnon-blocking + Reactor" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

q -> mvc: "typical CRUD / JPA"
q -> vt: "many blocking waits,\nkeep servlet code"
q -> wf: "shopping for reactive I/O"
```

**Fig. 1.** Mixing Boot web starters still yields **one** `WebApplicationType` (MVC if both present) — [[Can you use Spring MVC and WebFlux in the same application]]. HTTP client pick: [[What is the difference between RestTemplate WebClient and RestClient]].

| Need | Usual pick |
| --- | --- |
| JPA, JDBC, blocking SDKs | **MVC** |
| Lots of concurrent **blocking** I/O, keep imperative style | **MVC + virtual threads** |
| Streaming, backpressure, non-blocking drivers, Netty | **WebFlux** |
| Remote calls from an existing MVC app | **`WebClient`** (return reactive types) **without** rewriting the server |

Dump “virtual threads often better than rewriting to WebFlux” matches Spring’s **“shift often unnecessary.”** Pinning can **hurt** throughput — not a free lunch.

> [!warning] Virtual threads ≠ event loop
> You still **block**. You do not get WebFlux backpressure or `RouterFunction` for free.

> [!warning] WebFlux + JDBC on the loop is the worst mix
> Offload or don’t choose WebFlux — [[Why should you not use JDBC on the WebFlux event loop]].

> [!tip] Interview answer
> **MVC by default; virtual threads to scale blocking I/O on Java 21+ without going reactive; WebFlux only when the stack is non-blocking.** It is not a CRUD turbo. Do not put JDBC on Netty workers.

## See also

- [[When should you not use WebFlux]]
- [[What is the difference between Spring MVC and Spring WebFlux]]
- [[What is the difference between Spring MVC async and WebFlux]]
- [[How does the WebFlux event loop work]]
- [[What is Spring WebFlux]]
- [[What is Reactor Netty]]
- [[Can you use Spring MVC and WebFlux in the same application]]
