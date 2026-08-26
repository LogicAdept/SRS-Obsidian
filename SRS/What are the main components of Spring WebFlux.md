<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# What are the main components of Spring WebFlux?

> [!abstract] Short answer
> WebFlux is **not** “`RouterFunction` + `HandlerFunction`.” Those are **one programming model**. The stack is: **`HttpHandler`** (server adapters) → **`WebHandler` chain** (`WebFilter` / `WebExceptionHandler` / `webHandler`) → **`DispatcherHandler`** (front controller) → **`HandlerMapping` / `HandlerAdapter` / `HandlerResultHandler`**. You write **annotated controllers** and/or **functional endpoints**. **`WebClient`** is the reactive HTTP **client**. Types you return are usually Reactor **`Mono` / `Flux`**. Boot’s default server is **Reactor Netty**.

## Layers (Framework, not a dump pair)

`spring-web` *Reactive Core*:

| Layer | Role |
| --- | --- |
| **`HttpHandler`** | Minimal HTTP contract + adapters: **Reactor Netty**, **Tomcat**, **Jetty**, **any Servlet container** |
| **`WebHandler` API** | Chain: 0..N **`WebFilter`**, 0..N **`WebExceptionHandler`**, one **`WebHandler`** (bean name **`webHandler`**) |
| **Codecs** | `HttpMessageReader` / `HttpMessageWriter` for bodies |
| **Client** | **`ClientHttpConnector`**; apps use **`WebClient`** |

`WebHttpHandlerBuilder.applicationContext(context).build()` produces the `HttpHandler` the adapter binds.

`DispatcherHandler` *DispatcherHandler*: a **`WebHandler`** (front controller). Special beans:

- **`HandlerMapping`** — `RequestMappingHandlerMapping` (`@RequestMapping`), `RouterFunctionMapping` (WebFlux.fn), `SimpleUrlHandlerMapping`
- **`HandlerAdapter`** — invoke whatever was mapped
- **`HandlerResultHandler`** — write the response (`ResponseEntityResultHandler`, `ServerResponseResultHandler`, `ResponseBodyResultHandler`, `ViewResolutionResultHandler`)

Processing: first matching mapping → adapter → result handler.

Two **programming models** on that core (*Spring WebFlux*):

| Model | What you write |
| --- | --- |
| Annotated | `@Controller` / `@RestController` |
| Functional | `RouterFunction` + `HandlerFunction` |

They can run **side by side**. Dump “two main components” is **only** the functional column — [[What are router functions in WebFlux]], [[What is a HandlerFunction in WebFlux]].

```java
@Configuration
public class WebConfig implements WebFluxConfigurer {

    @Bean
    public RouterFunction<ServerResponse> routes(PersonHandler handler) {
        return RouterFunctions.route()
                .GET("/hi", req -> ServerResponse.ok().bodyValue("Hi"))
                .build();
    }
}
```

**Listing 1.** A router bean is **one** mapping source. Annotated `@RestController` is the other. Config: [[How do you configure a WebFlux application]].

```d2
direction: down
app: "@RestController /\nRouterFunction" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
dh: "DispatcherHandler\nMapping · Adapter · Result" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
chain: "WebFilter → webHandler\nWebExceptionHandler" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
http: "HttpHandler adapter" {
  width: 240
  height: 55
  style.fill: "#fce4ec"
}
srv: "Netty / Tomcat / Jetty" {
  width: 240
  height: 55
  style.fill: "#f3e5f5"
}

app -> dh -> chain -> http -> srv
```

**Fig. 1.** Client side is separate: [[What is WebClient]]. Default Boot server: [[What is Reactor Netty]]. Front controller: [[What is DispatcherHandler in WebFlux]].

Other dumps’ extras that **are** real: **`Mono`/`Flux`** (Reactor, required internally), **Netty** (adapter, not “the framework”), **`WebClient`**. They are not a substitute for the table above.

> [!warning] Router + handler is WebFlux.fn, not the module
> Interview “main components” that stop there miss **`DispatcherHandler`**, filters, codecs, and annotated controllers.

> [!warning] No Undertow adapter in current Framework table
> Live *HttpHandler* servers: **Netty, Tomcat, Jetty, Servlet container**. Do not recite an old Undertow row from memory.

> [!warning] `webHandler` is a bean name
> `WebHttpHandlerBuilder` looks up **`DispatcherHandler` named `webHandler`**. Renaming it drops it out of the chain.

> [!tip] Interview answer
> **HttpHandler adapters → WebFilter/WebExceptionHandler + DispatcherHandler → HandlerMapping/Adapter/ResultHandler; then `@RestController` and/or `RouterFunction`.** `WebClient` is the reactive client. `Mono`/`Flux` are the usual return types. Boot talks to Reactor Netty by default.

## See also

- [[What is Spring WebFlux]]
- [[What is DispatcherHandler in WebFlux]]
- [[What is a WebFilter in WebFlux]]
- [[What are router functions in WebFlux]]
- [[What is a HandlerFunction in WebFlux]]
- [[How do you implement a reactive REST controller in WebFlux]]
- [[How do you implement functional endpoints in WebFlux]]
- [[What is WebClient]]
- [[What is Reactor Netty]]
- [[What is the difference between Project Reactor and WebFlux]]
- [[How do you configure a WebFlux application]]
- [[What is the EnableWebFlux annotation]]
