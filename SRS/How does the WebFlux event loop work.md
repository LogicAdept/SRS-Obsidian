<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Library/Reactor #SRS

# How does the WebFlux event loop work?

> [!abstract] Short answer
> Non-blocking servers assume your code **does not block**, so they run requests on a **small, fixed event-loop pool** instead of a large servlet thread pool. On default **Reactor Netty** (Boot’s WebFlux server), **worker** threads ≈ **CPU cores, minimum 4**, shared by HTTP server and `WebClient` in the same JVM. A worker **registers I/O, returns, and resumes on a callback** when the channel is ready — there is **no thread-per-request**.

## MVC absorbs blocking; WebFlux does not

Spring WebFlux *Concurrency Model*:

| Stack | Assumption | Threads |
| --- | --- | --- |
| **Spring MVC** (servlet) | The current thread **may block** (remote calls, JDBC) | Servlet container keeps a **large pool** to absorb that wait |
| **WebFlux** (Netty-style) | The application **does not block** | **Small, fixed** event-loop workers |

“To scale with few threads” is not a contradiction: if the loop never waits on I/O, you do not need extra threads to cover blocked callers. Reactive pipelines then **react** when data arrives (Reactive Streams + Reactor `Mono`/`Flux`).

Vanilla WebFlux: **one server thread plus about as many request-processing threads as CPU cores**. Servlet containers used *as* WebFlux runtimes may start **more** (Spring cites **~10 on Tomcat**) because they still support blocking servlet I/O as well as Servlet 3.1 non-blocking I/O.

Boot’s WebFlux starter **defaults to Netty**. Tomcat/Jetty with WebFlux use **Servlet non-blocking I/O** behind an adapter — not MVC’s blocking servlet model. Runtime: [[What is Reactor Netty]].

## Reactor Netty workers vs selectors

Reactor Netty *Event Loop Group* (HTTP/TCP server):

- **`reactor.netty.ioWorkerCount`** — workers = available processors at start, **floor 4**.
- **`reactor.netty.ioSelectCount`** — default **`-1`**: **no dedicated selector**; workers also accept/select. A separate selector is for when workers are too busy to accept connections; configuring more than one still uses **only one** selector thread.
- **`reactor.netty.native`** — prefer native **epoll** (Linux) / **kqueue** when available.
- The default loop group is **shared by every server and client in the JVM**. Spring: `WebClient` on Reactor Netty shows threads such as **`reactor-http-nio-`**; **client and server share** that group unless you install custom `LoopResources`.

Dump “boss group / worker group, always `epoll`” is classic Netty `ServerBootstrap` talk. Reactor Netty’s documented knobs are **workers + optional selector**, native transport **when available**.

```d2
direction: down
accept: "Accept / select\n(worker, or optional selector)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
io: "Event-loop worker\nregister I/O, do not wait" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
cb: "Callback when ready\nDispatcherHandler / WebFilter" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
sched: "Optional Scheduler\nboundedElastic / parallel" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}

accept -> io -> cb
cb -> sched: "only if you publishOn / subscribeOn"
```

**Fig. 1.** One worker multiplexes many connections. Extra Reactor scheduler threads appear only when code switches pools.

```java
LoopResources loop = LoopResources.create("event-loop", 1, 4, true);

DisposableServer server = HttpServer.create()
        .runOn(loop)
        .bindNow();
```

**Listing 1.** Conceptual Reactor Netty sample — custom `LoopResources` (`selectCount` 1, `workerCount` 4). Spring does not start/stop the server; Boot or this API does. `server.onDispose().block()` on the **main** thread waits for shutdown; it is not request handling.

## Where work actually runs

After I/O is ready, `DispatcherHandler` / router functions run **on the same loop thread** until you **`publishOn` / `subscribeOn`**. JDBC, `Thread.sleep`, or **`Mono.block()`** on that thread stalls **every other connection on that worker**.

Escape hatch: wrap blocking work and **`subscribeOn(Schedulers.boundedElastic())`** — [[How do you offload blocking work in WebFlux]], [[Why should you not use JDBC on the WebFlux event loop]], [[What happens if you call block on a WebFlux event loop]].

> [!warning] Blocking the loop is the usual WebFlux outage
> `JdbcTemplate`, blocking SDKs, `Thread.sleep`, and `.block()` on event-loop threads freeze other requests on that worker. CPU can look idle while latency explodes.

> [!warning] “4–8 threads, 10k connections” is not a documented guarantee
> Worker count is **cores (minimum 4)**, not a magic 4–8. Benefit shows up with **I/O latency**; CPU-bound work still needs cores (or `Schedulers.parallel()`), and a blocked worker does **not** scale.

> [!warning] WebFlux-on-Tomcat is not a tiny Netty pool
> Spring: servlet containers may start **more** threads than a vanilla Netty server. Do not assume “always four `reactor-http-nio` threads” after switching the embedded server.

> [!tip] Interview answer
> **MVC: large pool, threads may block. WebFlux: small event-loop pool that must not block — register I/O, callback when ready, no thread-per-request.** Default Netty workers ≈ cores (min 4), shared with `WebClient`. JDBC/`block()` on the loop starves everyone on that worker; offload or use MVC.
