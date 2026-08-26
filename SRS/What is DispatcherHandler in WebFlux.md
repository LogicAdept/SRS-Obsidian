<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# What is `DispatcherHandler` in WebFlux?

> [!abstract] Short answer
> **`DispatcherHandler`** is WebFlux’s **front controller**: a **`WebHandler`** that maps a request, invokes a handler, and writes the result. Bean name **`webHandler`** so **`WebHttpHandlerBuilder`** can wrap it with **`WebFilter` / `WebExceptionHandler`**. Special beans: **`HandlerMapping`**, **`HandlerAdapter`**, **`HandlerResultHandler`**. Same pattern as MVC’s `DispatcherServlet`, **not** the Servlet API.

## Front controller on the reactive stack

Javadoc (since **5.0**): central dispatcher for HTTP handlers/controllers. Detects mappings, adapters, and result handlers from the context. Declared by **`@EnableWebFlux`**.

Spring *DispatcherHandler*:

1. Ask each **`HandlerMapping`**; **first match** wins (`RequestMappingHandlerMapping`, `RouterFunctionMapping`, `SimpleUrlHandlerMapping`).
2. **`HandlerAdapter`** invokes the handler → **`HandlerResult`**.
3. A **`HandlerResultHandler`** writes the response or a view.

Result handlers in WebFlux Config include `ResponseEntityResultHandler`, `ServerResponseResultHandler`, `ResponseBodyResultHandler`, `ViewResolutionResultHandler`.

```java
ApplicationContext context = ...
HttpHandler handler = WebHttpHandlerBuilder.applicationContext(context).build();
```

**Listing 1.** Official assembly — `HttpHandler` for a server adapter. Components: [[What are the main components of Spring WebFlux]]. Filters: [[What is a WebFilter in WebFlux]].

```d2
direction: down
ex: "ServerWebExchange" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
dh: "DispatcherHandler\n(webHandler)" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
map: "HandlerMapping" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
ad: "HandlerAdapter" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
res: "HandlerResultHandler" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}

ex -> dh
dh -> map -> ad -> res
```

**Fig. 1.** Functional endpoints and `@RestController` are **handlers**, not a second dispatcher — [[What are router functions in WebFlux]].

> [!warning] Bean name `webHandler`
> Rename it and `WebHttpHandlerBuilder` will not pick it up as the chain’s target.

> [!warning] Not `DispatcherServlet`
> Servlet MVC uses `DispatcherServlet`. WebFlux on Tomcat still uses this **`WebHandler`** behind a servlet adapter — do not mix servlet `Filter`s into that I/O model.

> [!tip] Interview answer
> **`DispatcherHandler` is WebFlux’s front controller `WebHandler`: mapping → adapter → result handler.** Register it as `webHandler`. Same idea as `DispatcherServlet`, reactive contracts throughout.

## See also

- [[What are the main components of Spring WebFlux]]
- [[What is Spring WebFlux]]
- [[What is a WebFilter in WebFlux]]
- [[What are router functions in WebFlux]]
- [[How do you implement a reactive REST controller in WebFlux]]
- [[What is the EnableWebFlux annotation]]
- [[What is the Front Controller pattern in Spring MVC]]
