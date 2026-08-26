<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Framework/WebMvc #API/REST #SRS

# What happens between an HTTP client and a Spring REST controller under sustained load?

> [!abstract] Short answer
> For **Servlet MVC + Tomcat**, each **non-async** request occupies a **worker thread** for the whole handler (filters → **`DispatcherServlet`** → singleton **`@RestController`** → **`HttpMessageConverter`**). Boot **4.1** defaults: **`server.tomcat.threads.max=200`**, **`min-spare=10`**, **`max-connections=8192`**, **`accept-count=100`**. When workers are busy, Tomcat still **accepts** until **`maxConnections`**; then the **OS** queues about **`acceptCount`** more; beyond that connections are **refused or time out**. That is **not** Reactive Streams backpressure. **`spring.threads.virtual.enabled=true`** makes **`threads.max` / `min-spare` no-ops**.

## One worker, then queues, then the OS

Tomcat HTTP Connector: a non-async request **needs a thread for its duration**. Extra load creates workers up to **`maxThreads`** (Tomcat default **200**, same as Boot’s **`server.tomcat.threads.max`**). Further arrivals are **accepted** until **`maxConnections`** (default **8192**); sockets wait for a free worker. After that the **OS accept queue** (Boot **`server.tomcat.accept-count`**, Tomcat default **100**) may fill; then the OS **refuses or times out**. Clients see **latency**, **connection refused**, or **timeouts** — not a Spring `@ExceptionHandler` for “pool full.”

Inside a worker: **servlet filters** (Security) → **`DispatcherServlet`** (mapping, adapter, converters). The controller bean is **`singleton`**: one instance, many threads. Blocking JDBC holds the **worker** until the pool or query returns. HikariCP **`maximumPoolSize` default 10**: extra Tomcat workers **block on `getConnection()`** up to **`connectionTimeout`**, then fail — the HTTP thread is still occupied while waiting.

Servlet async (`Callable` / `DeferredResult` / emitters) **releases** the container thread until completion. Virtual threads keep **MVC/blocking** code; they do **not** turn the app into WebFlux.

```properties
server.tomcat.threads.max=200
server.tomcat.threads.min-spare=10
server.tomcat.max-connections=8192
server.tomcat.accept-count=100
spring.threads.virtual.enabled=false
```

**Listing 1.** Conceptual Boot **4.1** appendix defaults. `threads.max` / `min-spare` **do not apply** when virtual threads are on. `threads.max-queue-capacity` default is **`Integer.MAX_VALUE`** and only matters if you set it **> 0**.

```d2
direction: down
cli: "HTTP clients" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
tcp: "TCP accept\nmaxConnections then acceptCount" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
pool: "Tomcat workers\nmaxThreads (200)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
mvc: "filters → DispatcherServlet\n@RestController + converters" {
  width: 300
  height: 55
  style.fill: "#f3e5f5"
}
db: "Optional JDBC\nHikari max 10" {
  width: 240
  height: 45
  style.fill: "#fce4ec"
}

cli -> tcp -> pool -> mvc -> db
```

**Fig. 1.** Sustained load fills **workers first**, then **connection caps**, then the **OS queue**. MVC path: [[How does the Spring MVC request lifecycle work]]. Singleton bean: [[What is the default scope of a Spring MVC controller]]. Release the worker: [[How do you implement asynchronous request processing in Spring MVC]]. MVC vs WebFlux vs VT: [[When should you use WebFlux versus Spring MVC versus virtual threads]].

> [!warning] Raising `threads.max` without the DB pool starves workers
> **200** HTTP threads on **10** JDBC connections means most workers sit in **`getConnection()`**. Throughput is the **pool**, not Tomcat. Timeouts then look like “the API is slow” while the connector still has free **`maxConnections`**.

> [!warning] Full Tomcat queues are not an MVC 503 you handle in `@ExceptionHandler`
> Past **`maxConnections` + `acceptCount`**, the **OS** may refuse the TCP handshake. The request **never** reaches `DispatcherServlet`. Tune connectors and timeouts; do not expect a controller `catch`.

> [!warning] Mutable controller fields race under load
> One `@RestController` instance serves every worker. Request state belongs on **arguments / `Model`**, not fields. Same as any singleton Spring bean.

> [!warning] WebFlux backpressure is a different stack
> MVC + Tomcat **queues threads and sockets**. `Flux.request(n)` is **WebFlux**. Mixing both Boot web starters still leaves you on **MVC** unless you force **`WebApplicationType.REACTIVE`**.

> [!tip] Interview answer
> **Each blocking MVC request owns a Tomcat worker (default max 200) through filters, `DispatcherServlet`, and the singleton controller.** When workers are busy, connections wait up to **8192**, then the OS accept queue (~**100**), then refuse or timeout. The JDBC pool is a **separate**, usually **smaller** cap. Async or virtual threads change **who** blocks, not the fact that MVC is thread-per-request unless you opt into Servlet async.
