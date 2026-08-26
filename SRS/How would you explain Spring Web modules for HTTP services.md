<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Framework/WebFlux #SRS

# How would you explain Spring Web modules for HTTP services?

> [!abstract] Short answer
> Three Framework jars, not one “Spring Web.” **`spring-web`** is shared HTTP infrastructure (mapping annotations, **`HttpMessageConverter`**, reactive **`HttpHandler`** / codecs). **`spring-webmvc`** is **Spring MVC**: Servlet **`DispatcherServlet`**. **`spring-webflux`** (since **5.0**) is the **reactive** server stack plus **`WebClient`**. Both stacks are **optional**; MVC + reactive **`WebClient`** is a supported mix. Boot wraps them as **`spring-boot-starter-webmvc`** (Boot **4**; Boot **3** used **`starter-web`**) and **`spring-boot-starter-webflux`**.

## Shared foundation, two HTTP stacks

Framework *Overview*: the Framework is modular. Web support includes **Servlet MVC** and, in parallel, **WebFlux**. MVC’s formal name is the **`spring-webmvc`** artifact; WebFlux’s is **`spring-webflux`**. Each module is optional.

**`spring-web`** sits under both:

| Piece | Where it lives | Role |
| --- | --- | --- |
| `@RequestMapping`, `@GetMapping`, `@RestController`, … | `spring-web` | Same annotations on **both** stacks |
| `HttpMessageConverter` | `spring-web` | Blocking body read/write (`InputStream` / `OutputStream`); **`RestClient`** / **`RestTemplate`** and MVC controllers |
| `HttpHandler`, `WebHandler`, codecs | `spring-web` | Non-blocking HTTP abstraction + Reactive Streams adapters (Netty, Tomcat, Jetty, Servlet) |
| `DispatcherServlet` | `spring-webmvc` | Servlet front controller |
| `DispatcherHandler` | `spring-webflux` | Reactive front controller |
| `WebClient` | `spring-webflux` | Reactive HTTP **client** (uses `spring-web` connectors/codecs) |
| `RestClient` | `spring-web` | Synchronous fluent HTTP **client** (Framework **6.1+**; **`RestTemplate` deprecated in 7.0**) |

MVC assumes **blocking Servlet I/O** and a **large thread pool**. WebFlux assumes **you do not block** and uses a **small event-loop pool**. Same `@RestController` text does **not** tell you which stack is running — check the module, the server (`DispatcherServlet` vs `DispatcherHandler` / Netty), and whether `@RequestBody` is reactive. Stack choice: [[What is the difference between Spring MVC and Spring WebFlux]]. Front controllers: [[What is Spring MVC DispatcherServlet]], [[What is DispatcherHandler in WebFlux]].

```xml
<!-- Conceptual: pick one HTTP server stack -->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
</dependency>
<!-- or -->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webflux</artifactId>
</dependency>
```

**Listing 1.** Conceptual Framework artifacts. `spring-webmvc` / `spring-webflux` pull **`spring-web`**. Boot apps depend on **starters**, not these jars directly.

```d2
direction: down
web: "spring-web\nannotations, converters,\nHttpHandler / codecs" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
mvc: "spring-webmvc\nDispatcherServlet\nblocking Servlet I/O" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
flux: "spring-webflux\nDispatcherHandler + WebClient\nnon-blocking I/O" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
client: "RestClient (spring-web)\nblocking fluent HTTP" {
  width: 260
  height: 55
  style.fill: "#f3e5f5"
}

web -> mvc
web -> flux
web -> client
```

**Fig. 1.** HTTP services share `spring-web`. You choose **one server module**. Clients can cross stacks: MVC controllers may return Reactor types from **`WebClient`**. Clients: [[What is the difference between RestTemplate WebClient and RestClient]]. Converters: [[What is HttpMessageConverter in Spring MVC]].

> [!warning] Two Boot web starters do not start two servers
> If **`starter-webmvc`** (or Boot 3 **`starter-web`**) and **`starter-webflux`** are both on the classpath, Boot keeps **MVC** so you can still inject **`WebClient`**. That is **not** “MVC and WebFlux request handling in one app.” Override only with **`WebApplicationType.REACTIVE`**. See [[Can you use Spring MVC and WebFlux in the same application]].

> [!warning] `@RestController` does not select the module
> Mapping annotations live in **`spring-web`**. A controller that compiles against MVC will often compile against WebFlux. Reactive **`@RequestBody`** is the WebFlux-side difference; blocking JDBC on the WebFlux loop is still the wrong fit.

> [!warning] `WebClient` is not in `spring-webmvc`
> The class lives in **`spring-webflux`**. MVC apps add the WebFlux starter (or the jar) **for the client**. That does not switch the server to Netty unless Boot’s web application type is reactive.

> [!tip] Interview answer
> **`spring-web` is shared HTTP plumbing. `spring-webmvc` is Servlet MVC. `spring-webflux` is the reactive stack plus `WebClient`.** Pick one server stack; Boot’s two web starters together still mean MVC. Same mapping annotations on both sides because they live in `spring-web`.
