<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# What is Reactor Netty?

> [!abstract] Short answer
> **Reactor Netty** is Project Reactor’s **backpressure-ready network engine** on **Netty 4**: **HTTP** (including WebSocket), **TCP**, and **UDP** clients and servers. It is **not** another name for Reactor Core (`Mono`/`Flux`). **Spring WebFlux** talks to it through an **`HttpHandler` adapter**. **`spring-boot-starter-webflux` defaults to it** so the **server and `WebClient` share event-loop resources**.

## Engine vs web framework vs Reactor Core

Reactor Netty *Introducing Reactor Netty*: suited to microservices; engines for HTTP, TCP, UDP; Java 8+; depends on **Reactive Streams**, **Reactor Core 3.x**, **Netty 4.2.x**.

Spring *Reactive Core* `HttpHandler` table (current): **Netty** (Reactor Netty), **Tomcat**, **Jetty**, **any Servlet container**. **Undertow is not in that table.**

Spring *Servers*: Boot’s WebFlux starter **defaults to Netty** because it is common in the non-blocking space and **lets client and server share resources**. Switch Tomcat/Jetty by changing the starter dependency — still **Servlet non-blocking I/O** behind an adapter, not MVC’s blocking servlet model.

```java
HttpHandler handler = ...
ReactorHttpHandlerAdapter adapter = new ReactorHttpHandlerAdapter(handler);
HttpServer.create().host(host).port(port).handle(adapter).bindNow();
```

**Listing 1.** Framework sample — bind Reactor Netty to an `HttpHandler`. Typical apps let **Boot** start the server. Front controller: [[What is DispatcherHandler in WebFlux]].

Workers ≈ **CPU cores, minimum 4** (`reactor.netty.ioWorkerCount`) — [[How does the WebFlux event loop work]]. Dump “thousands of connections on a few threads” is **capacity under non-blocking I/O**, not a documented connection quota. One **`sleep` / JDBC / `.block()`** on a worker stalls every exchange on that thread.

```d2
direction: down
app: "WebFlux / WebClient" {
  width: 220
  height: 55
  style.fill: "#e3f2fd"
}
rn: "Reactor Netty\nHttpServer / HttpClient" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
n: "Netty event loop\n(epoll / kqueue / NIO)" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

app -> rn -> n
```

**Fig. 1.** Boot `ReactorResourceFactory` shares loops between server and client unless you replace it. Client: [[What is WebClient]].

> [!warning] Not “WebFlux is Netty”
> Framework adapts several servers. **Netty is Boot’s default**, not the only runtime. Tomcat can host **WebFlux** (non-blocking servlet I/O) or **MVC** (blocking) — different models.

> [!warning] Not Undertow on the current adapter list
> Recite **Netty / Tomcat / Jetty / Servlet container**. Old dumps still name Undertow.

> [!warning] Shared loops
> Custom `LoopResources` / `ReactorResourceFactory` if you must isolate client and server. Default is **one JVM-wide group**.

> [!tip] Interview answer
> **Reactor Netty is the reactive TCP/HTTP engine on Netty that WebFlux and `WebClient` use by default in Boot.** It is not Reactor Core. Few event-loop threads; do not block them. Tomcat/Jetty are optional adapters, not the Boot default.

## See also

- [[What is Spring WebFlux]]
- [[How does the WebFlux event loop work]]
- [[What happens if you call block on a WebFlux event loop]]
- [[What is WebClient]]
- [[What are the main components of Spring WebFlux]]
- [[What is the difference between Project Reactor and WebFlux]]
- [[How do you configure a WebFlux application]]
