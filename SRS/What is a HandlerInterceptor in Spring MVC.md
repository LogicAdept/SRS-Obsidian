<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is a `HandlerInterceptor` in Spring MVC?

> [!abstract] Short answer
> A **`HandlerInterceptor`** is a callback on the **`DispatcherServlet` execution chain** around a mapped handler: **`preHandle`** (after `HandlerMapping`, before `HandlerAdapter`), **`postHandle`** (after a successful handler, before view render), **`afterCompletion`** (after the request, including view render). Return **`false` from `preHandle`** to abort the chain (you own the response). Common for locale, logging, shared model data — **not** a substitute for Spring Security.

## Three callbacks on the mapped handler

`HandlerInterceptor` javadoc: register interceptors for groups of handlers to factor out preprocessing. `preHandle` runs **after** an appropriate handler is chosen, **before** the adapter invokes it. `postHandle` runs **after successful** handler execution, **before** the servlet renders the view, and can add model attributes via `ModelAndView` (which **may be `null`**). `afterCompletion` runs after rendering; **only if this interceptor’s `preHandle` returned `true`**. `postHandle` and `afterCompletion` run in **inverse** chain order.

```java
public class TimingInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response,
            Object handler) {
        request.setAttribute("t0", System.nanoTime());
        return true; // false → chain stops; you must write the response
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response,
            Object handler, ModelAndView modelAndView) {
        if (modelAndView != null) {
            modelAndView.addObject("serverTime", Instant.now());
        }
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response,
            Object handler, Exception ex) {
        // cleanup; ex excludes exceptions already handled by an ExceptionResolver
    }
}
```

**Listing 1.** Conceptual interceptor using default interface methods (no `HandlerInterceptorAdapter`). Registration: [[How do you register a HandlerInterceptor in Spring MVC]].

```d2
direction: down
map: "HandlerMapping\nselects handler" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
pre: "preHandle" {
  width: 160
  height: 50
  style.fill: "#fff3e0"
}
adp: "HandlerAdapter\ninvokes controller" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
post: "postHandle" {
  width: 160
  height: 50
  style.fill: "#fff3e0"
}
view: "View render" {
  width: 160
  height: 50
  style.fill: "#fce4ec"
}
done: "afterCompletion" {
  width: 180
  height: 50
  style.fill: "#ffebee"
}

map -> pre -> adp -> post -> view -> done
```

**Fig. 1.** Interceptors sit on the MVC handler chain, not around every servlet request. Filters vs interceptors vs AOP: [[How do servlet filters interceptors and AOP differ in Spring]].

Async: the handler may run on another thread; `postHandle` / `afterCompletion` may be skipped until a dispatch back — see `AsyncHandlerInterceptor`.

Spring MVC *Interceptors* docs: **not ideally suited as a security layer** because path matching can diverge from annotated controllers. Prefer Spring Security (or a Servlet filter) **early** in the chain.

Compared with a Filter: interceptors cannot replace request/response objects; Filters can. Interceptors are Spring beans on `HandlerMapping`; Filters are servlet-container mapping.

> [!warning] `ModelAndView` is often `null` for REST
> `@ResponseBody` / `ResponseEntity` typically have no view. `postHandle` cannot rewrite a body already written by the adapter. Use **`ResponseBodyAdvice`** (or wrap earlier) for response-body mutation.

> [!warning] `afterCompletion`’s `Exception` omits handled errors
> Exceptions already processed by a `HandlerExceptionResolver` are **not** passed in `ex`.

> [!warning] `HandlerInterceptorAdapter` is obsolete
> The interface has **default methods** since 5.3. Do not learn the old adapter class as the current API.

> [!tip] Interview answer
> **`HandlerInterceptor` runs `preHandle` → controller → `postHandle` → view → `afterCompletion` for mapped Spring MVC handlers.** `preHandle` returning `false` aborts the chain. Use it for cross-cutting MVC concerns; use Spring Security or a Filter for real security and for requests that never hit a `HandlerMapping`.
