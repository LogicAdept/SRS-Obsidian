<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Framework/WebFlux #Java/Servlet #SRS

# Can you use the Servlet request object in every Spring application?

> [!abstract] Short answer
> **No.** `HttpServletRequest` is the **Jakarta Servlet** API. You get it in **Spring MVC** (and other servlet apps) as a controller argument. **WebFlux** uses **`ServerWebExchange` / `ServerHttpRequest`**, not the Servlet request. **Non-web** Spring (`WebApplicationType.NONE`, batch, CLI) has **no HTTP request** at all. Even in MVC it exists only **for the current request thread** (`RequestContextHolder`); `@Async` and scheduled jobs do not have one unless you pass data yourself.

## Servlet stack only, and only during a request

MVC *Method Arguments*: handler methods may declare `jakarta.servlet.ServletRequest` / `HttpServletRequest` (or `MultipartHttpServletRequest`). `WebRequest` / `NativeWebRequest` wrap the same data **without** importing Servlet types. `DispatcherServlet` binds the request on the thread; `RequestContextHolder.currentRequestAttributes()` throws **`IllegalStateException`** if nothing is bound.

WebFlux *Method Arguments*: `ServerWebExchange`, `ServerHttpRequest`, `ServerHttpResponse`. No Servlet request row. Boot’s WebFlux starter **defaults to Netty**. On Tomcat, WebFlux still uses **non-blocking** I/O; you still program to `ServerHttpRequest`.

Boot: `spring.main.web-application-type=none` does **not** start an embedded server. There is no `ServletContext` and no request object to inject.

```java
@GetMapping("/client")
public String client(HttpServletRequest request) {
    return request.getRemoteAddr();
}

@GetMapping("/rx")
public Mono<String> rx(ServerHttpRequest request) {
    return Mono.just(request.getRemoteAddress().toString());
}
```

**Listing 1.** Conceptual: MVC vs WebFlux argument types from Spring Framework method-argument tables. Stacks: [[Can you use Spring MVC and WebFlux in the same application]]. Reactive HTTP: [[What is Spring WebFlux]]. MVC handlers: [[How do you create a Spring MVC controller]].

```d2
direction: down
q: "Need HttpServletRequest?" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
mvc: "MVC DispatcherServlet\nyes, this request thread" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
flux: "WebFlux\nServerHttpRequest" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
none: "NONE / CLI / Batch\nno request" {
  width: 240
  height: 45
  style.fill: "#fce4ec"
}

q -> mvc
q -> flux
q -> none
```

**Fig. 1.** The Servlet request is not a Spring-wide API. It is a servlet-container request, live only while MVC handles that HTTP call.

> [!warning] `RequestContextHolder` off the dispatcher thread
> `currentRequestAttributes()` fails in **`@Async`**, Reactor workers, and `CommandLineRunner` unless you copied attributes. Prefer method arguments over a static holder in services.

> [!warning] Do not `@Autowired HttpServletRequest` on a singleton
> Controllers are **singleton**. Injecting the request as a field is a **request-scoped proxy** (when it works) or a **stale / wrong** request. Declare it on the **handler method**.

> [!tip] Interview answer
> **Only on the servlet MVC stack, during a request.** WebFlux uses `ServerWebExchange`. A Boot app with `web-application-type=none` has no servlet request. MVC controllers take `HttpServletRequest` as a method argument.
