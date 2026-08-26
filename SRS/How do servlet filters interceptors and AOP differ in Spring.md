<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Framework/AOP #SRS

# How do servlet filters interceptors and AOP differ in Spring?

> [!abstract] Short answer
> **Filters** wrap the **Servlet** (`jakarta.servlet.Filter`) — all dispatches, can **replace request/response**. **`HandlerInterceptor`s** wrap a **mapped MVC handler** inside **`DispatcherServlet`**. **Spring AOP** wraps **bean method executions** (any layer), not the HTTP chain. Put **security as early as a Servlet filter** (Spring Security), not in an MVC interceptor.

## Three layers, three APIs

| | **Filter** | **HandlerInterceptor** | **Spring AOP** |
| --- | --- | --- | --- |
| **Where** | Outside / around `DispatcherServlet` | After `HandlerMapping`, before/after `HandlerAdapter` | Proxy around a Spring bean |
| **Sees** | `ServletRequest` / `Response` | `HttpServletRequest`, handler `Object` (often `HandlerMethod`), `ModelAndView` | Join point (`JoinPoint` / `ProceedingJoinPoint`) |
| **Abort** | Don’t call `chain.doFilter` | `preHandle` returns `false` (you own the response) | Throw, or skip `proceed()` in `@Around` |
| **Config** | `web.xml` / Servlet registration / Boot `Filter` bean | Application context (`WebMvcConfigurer.addInterceptors`) | `@Aspect` + auto-proxy |

`HandlerInterceptor` javadoc: similar to a Filter but **cannot swap** the request/response objects; Filters are stronger for **content** (multipart, GZIP, all URLs or content types). Fine-grained **handler** preprocessing (locale, shared handler code) belongs on the interceptor. Spring MVC *Filters*: CORS via `CorsFilter` **ahead of** Spring Security; built-ins include form-data, forwarded headers, shallow ETag.

AOP is not HTTP-specific: `@Transactional`, `@Cacheable`, custom `@Around` on **services**. It never runs for static resources that never hit a bean, and **`this.foo()`** skips it — [[Why does a self-invocation skip Spring AOP advice]]. Advice: [[What is Advice in Spring AOP]]. Interceptor callbacks: [[What is a HandlerInterceptor in Spring MVC]]. Lifecycle: [[How does the Spring MVC request lifecycle work]].

```d2
direction: down
f: "Servlet Filter chain\n(CORS, Security, gzip)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
ds: "DispatcherServlet" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
hi: "HandlerInterceptor\npreHandle → handler → postHandle" {
  width: 300
  height: 70
  style.fill: "#fce4ec"
}
aop: "AOP proxy on @Service\n(optional, not only web)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

f -> ds -> hi -> aop
```

**Fig. 1.** A request can hit filters without any interceptor (no mapping) and can hit AOP without any servlet (CLI, messaging). `@ResponseBody`: the adapter **commits** the body **before** `postHandle` — too late to add headers there (`ResponseBodyAdvice` instead).

> [!warning] Do not implement security as an MVC interceptor
> Official `HandlerInterceptor` note: path matching can **diverge** from annotated controllers. Use **Spring Security on the filter chain**, as early as possible — [[Is security a cross-cutting concern]].

> [!warning] “Has HandlerMethod” is not the type
> `preHandle`’s `handler` is **`Object`**. For `@RequestMapping` it is often a **`HandlerMethod`**; for other mappings it is not. Cast only after `instanceof`.

> [!tip] Interview answer
> **Filter = Servlet API around the servlet. Interceptor = MVC chain around the mapped handler. AOP = method interceptor on Spring beans.** Filters can wrap request/response; interceptors cannot. Security belongs in the filter chain, not `HandlerInterceptor`.
