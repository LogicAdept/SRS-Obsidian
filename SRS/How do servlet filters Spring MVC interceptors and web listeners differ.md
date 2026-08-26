<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/Spring/Framework/WebMvc #Java/Listeners #SRS

# How do servlet filters Spring MVC interceptors and web listeners differ?

> [!abstract] Short answer
> **`Filter`** wraps **any** servlet or static resource in the container (`doFilter` + `FilterChain`) and **can replace** request/response. **`HandlerInterceptor`** runs **inside `DispatcherServlet` after `HandlerMapping`** around one mapped handler (`preHandle` / `postHandle` / `afterCompletion`) and **cannot** swap those objects. **Listeners** (`ServletContextListener`, `HttpSessionListener`, `ServletRequestListener`, …) observe **lifecycle events**, not a per-request wrap of a controller. Spring Security sits in the **filter** chain **before** the servlet. Interceptors are **not** “Java EE filters renamed” and **not** Spring AOP.

## Container wrap vs MVC chain vs events

Jakarta Servlet `Filter`: `init` once, then `doFilter` on every matching request. Skip `chain.doFilter` to abort. Typical: gzip, multipart, CORS, Security.

`HandlerInterceptor`: `preHandle` **true** continues the chain; **false** means you already wrote the response (it does **not** mean “send the controller’s response to the client”). `postHandle` is **after a successful handler**, **before view render**. `afterCompletion` runs only if **this** interceptor’s `preHandle` returned true. Register via `WebMvcConfigurer.addInterceptors` (or a `HandlerMapping`’s interceptor list). A `@Component` interceptor is **not** applied until registered.

Listeners implement `EventListener` subtypes. `ServletContextListener.contextInitialized` runs **before** any filter or servlet is initialized.

```d2
direction: down
l: "Listeners\ncontext / session / request events" {
  width: 300
  height: 55
  style.fill: "#f3e5f5"
}
f: "Filter chain\n(can wrap request/response)" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
ds: "DispatcherServlet" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
hi: "HandlerInterceptor\npreHandle → handler → postHandle" {
  width: 320
  height: 55
  style.fill: "#e8f5e9"
}

l -> f
f -> ds
ds -> hi
```

**Fig. 1.** Listeners are not in the HTTP wrap. Filters enclose the servlet. Interceptors enclose a **mapped handler** only. AOP vs these layers: [[How do servlet filters interceptors and AOP differ in Spring]]. Callbacks: [[What is a HandlerInterceptor in Spring MVC]]. Register: [[How do you register a HandlerInterceptor in Spring MVC]].

```java
public boolean preHandle(HttpServletRequest request, HttpServletResponse response,
        Object handler) {
    return true; // continue; false → you own the response
}
```

**Listing 1.** Conceptual: interceptor abort is `false`, not “return the response.” Filters abort by not calling `chain.doFilter`.

> [!warning] Not the same SPI
> Dumps that say “Java EE Filter = Spring Interceptor = AOP” are **wrong**. Three APIs, three places in the stack. AOP advises **bean methods**.

> [!warning] Interceptors cannot wrap the request
> You cannot swap `HttpServletRequest` in `preHandle`. Set **attributes** or **response headers**. Content wrapping (GZIP, multipart) belongs on a **Filter**.

> [!warning] `@Component` is not registration
> An interceptor bean still needs **`addInterceptors`**. Security as an interceptor is a **mismatch** with MVC path matching; use the **filter** chain.

> [!tip] Interview answer
> **Filters wrap the servlet (and static files) and can replace request/response. Interceptors wrap a Spring MVC handler after it is mapped. Listeners fire on context, session, or request lifecycle — they do not sit in the controller call chain.** Spring Security is a filter in front of `DispatcherServlet`.
