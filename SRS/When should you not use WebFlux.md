<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Spring/Framework/WebMvc #Java/Concurrency/VirtualThreads #SRS

# When should you not use WebFlux?

> [!abstract] Short answer
> Skip WebFlux when the app **already works on Spring MVC**, when the data layer is **blocking (JPA, JDBC, sync SDKs)**, when the team cannot afford the **reactive learning curve**, or when you only need **cheap concurrency for blocking I/O** — on **Java 21+** that is often **MVC + virtual threads**, not a Netty rewrite. WebFlux is for **non-blocking I/O at scale**, not faster CRUD.

## Check dependencies first

Spring WebFlux *Applicability*:

- **MVC is fine** — do not migrate. Imperative code is easier to write, debug, and library-fit (most libraries still block).
- **Blocking persistence or networking (JPA, JDBC, classic HTTP clients)** — **MVC is the usual choice**. You *can* `publishOn` / `subscribeOn` a blocking call, but you are **not** using a non-blocking stack.
- **Large team / little reactive experience** — the shift to non-blocking, functional pipelines is **steep**. A practical start is **`WebClient` inside MVC**, not a full rewrite.
- **Wide range of apps** — Spring expects the full switch is **often unnecessary**. If you cannot name the benefit, stay on MVC.

*Performance*: reactive/non-blocking generally **does not make the app faster**. Extra work can even add CPU. The win is **scaling with a small thread pool and less memory when there is I/O latency** (slow or mixed network). CPU-bound work still needs cores; pinning it on an event-loop worker is worse than MVC.

Need JPA/Hibernate (sessions, lazy load, L2 cache): that API **blocks**. R2DBC is a **different** stack, not “reactive JPA”. JDBC on the loop: [[Why should you not use JDBC on the WebFlux event loop]].

```d2
direction: down
q: "Need WebFlux?" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
mvc: "MVC / blocking\nJPA JDBC team fit" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
vt: "Java 21+ MVC +\nspring.threads.virtual.enabled" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
wf: "WebFlux\nnon-blocking I/O + latency" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

q -> mvc: "typical CRUD"
q -> vt: "many blocking waits,\nkeep servlet style"
q -> wf: "already non-blocking,\nor shopping for that model"
```

**Fig. 1.** WebFlux is the third box, not the default. Full three-way: [[When should you use WebFlux versus Spring MVC versus virtual threads]]. Mixing HTTP stacks: [[Can you use Spring MVC and WebFlux in the same application]].

## Virtual threads are not WebFlux

Boot *Virtual threads* (Java **21+**; docs currently **strongly recommend Java 24+**): `spring.threads.virtual.enabled=true`. That keeps **blocking** code and a **servlet** server (Tomcat can use a virtual-thread executor — Boot **3.2+**). It is **not** “WebFlux with cheap threads”, and it is **not** the MVC+WebFlux classpath rule.

```properties
spring.threads.virtual.enabled=true
```

**Listing 1.** Conceptual Boot property — servlet/MVC-style concurrency, not a Netty event-loop setting. Pinning can **hurt** throughput; read JDK virtual-thread docs before flipping it.

Choosing WebFlux anyway means **non-blocking I/O all the way down**, `Mono`/`Flux` (or Kotlin coroutines), backpressure, and a harder debug story — [[How does the WebFlux event loop work]].

> [!warning] WebFlux is not “faster CRUD”
> Without I/O wait to hide, you mainly pay pipeline complexity. Moderate traffic + JDBC is an MVC app.

> [!warning] Offloading JDBC does not make the architecture reactive
> `boundedElastic` is an **escape hatch**. Spring: you would not be making the most of a non-blocking web stack.

> [!warning] Virtual threads ≠ two web stacks
> `spring.threads.virtual.enabled` does not start Netty beside Tomcat. Both Boot web starters still collapse to **one** `WebApplicationType` (MVC if both are present).

> [!tip] Interview answer
> **Do not use WebFlux if MVC already fits, if you live on JPA/JDBC, or if the team is not ready to never block the event loop.** For many concurrent *blocking* calls on Java 21+, prefer MVC plus virtual threads. Use WebFlux when you actually have non-blocking I/O and latency to absorb — it is not a speed upgrade for simple CRUD.
