<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# What is Spring WebFlux?

> [!abstract] Short answer
> **Spring WebFlux** is the Spring Framework **reactive-stack web module** (`spring-webflux`), added in **5.0** beside **Spring MVC** (`spring-webmvc`). It is **fully non-blocking**, speaks **Reactive Streams back pressure**, and runs on **Netty** or **Servlet containers** (non-blocking I/O). Application types are **Reactor `Mono` / `Flux`** (other `Publisher`s via adapters). Boot’s WebFlux starter **defaults to Reactor Netty**.

## A second web stack, not a faster MVC

Spring *Spring WebFlux*: MVC was built for the **Servlet API**. WebFlux is the **reactive** web framework next to it. Both modules are **optional**; you pick one HTTP stack, or use MVC **and** reactive **`WebClient`**.

Why it exists (*Overview*): a **non-blocking** stack that handles concurrency with **few threads**, plus Java 8 lambdas for **functional endpoints** next to annotated controllers.

Reactor is the **library of choice**: `Mono` (0..1), `Flux` (0..N), operators, **non-blocking back pressure**. WebFlux **requires** Reactor internally; APIs accept a `Publisher` and typically return `Flux`/`Mono`. Engine vs framework: [[What is the difference between Project Reactor and WebFlux]].

Two programming models on `spring-web` (`HttpHandler` / `WebHandler`):

| Model | What you write |
| --- | --- |
| **Annotated controllers** | `@Controller` / `@RestController`, same mapping annotations as MVC; WebFlux also accepts **reactive `@RequestBody`** |
| **Functional endpoints** | `RouterFunction` + `HandlerFunction` — the app routes and handles explicitly |

```java
@RestController
public class HelloController {

    @GetMapping("/hello")
    public String handle() {
        return "Hello WebFlux";
    }
}
```

**Listing 1.** Conceptual Framework sample — a `String` body is valid; typical REST returns `Mono`/`Flux` — [[How do you implement a reactive REST controller in WebFlux]].

```d2
direction: down
app: "@RestController /\nRouterFunction" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
web: "spring-webflux\nDispatcherHandler" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
http: "HttpHandler adapter" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
srv: "Netty / Tomcat / Jetty" {
  width: 240
  height: 60
  style.fill: "#fce4ec"
}

app -> web -> http -> srv
```

**Fig. 1.** Framework does **not** start the server; Boot (or a few lines of Netty bind) does. Default Boot server: [[What is Reactor Netty]]. Front controller: [[What is DispatcherHandler in WebFlux]].

Supported server adapters (*Reactive Core*): **Reactor Netty**, **Tomcat**, **Jetty**, **any Servlet container** (Servlet non-blocking I/O bridged to Reactive Streams). MVC on Tomcat still uses **blocking** Servlet I/O; WebFlux on Tomcat does **not**.

*Performance*: reactive is **not** generally faster. The expected win is **scale with a small fixed thread pool and less memory when there is I/O latency**. CPU-bound CRUD does not magically speed up — [[When should you not use WebFlux]], [[How does the WebFlux event loop work]].

> [!warning] WebFlux is not “faster MVC”
> Extra pipeline work can **increase** CPU. Pick it for **non-blocking I/O and concurrency**, not for a quicker `findById`.

> [!warning] Netty is Boot’s default, not “built into Framework”
> `spring-webflux` adapts servers; **`spring-boot-starter-webflux`** brings Reactor Netty unless you switch the starter.

> [!warning] Blocking JDBC/JPA is a poor fit
> Check dependencies: if persistence blocks, **MVC is the usual choice** — [[Why should you not use JDBC on the WebFlux event loop]].

> [!tip] Interview answer
> **WebFlux is Spring’s reactive web stack since 5.0: non-blocking, Reactive Streams, Reactor `Mono`/`Flux`, annotated controllers or functional routes.** It sits beside MVC, not on top of it. Boot talks to Netty by default. It scales idle I/O with few threads; it is not a CRUD turbo.
