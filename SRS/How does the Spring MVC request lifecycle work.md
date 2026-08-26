<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Servlet #SRS

# How does the Spring MVC request lifecycle work?

> [!abstract] Short answer
> **Filters run first (Servlet API). Then `DispatcherServlet` binds the web context, locale, and optional multipart wrapper, asks `HandlerMapping` for a `HandlerExecutionChain`, runs `preHandle`, lets a `HandlerAdapter` invoke the handler, runs `postHandle`, renders a `View` (or the adapter already wrote the body), then `afterCompletion`.** Exceptions go through **`HandlerExceptionResolver`** (`@ExceptionHandler` / `@ControllerAdvice`). Security belongs in the **filter** chain, not as the first MVC interceptor.

## Outside the servlet, then inside it

The Servlet container invokes **filters** mapped to the request (including Spring Security), then the **servlet** whose URL pattern matched. Spring MVC *Processing* is what happens **inside** `DispatcherServlet`:

1. Bind the servlet `WebApplicationContext` on the request (`WEB_APPLICATION_CONTEXT_ATTRIBUTE`).
2. Bind `LocaleResolver`.
3. If a `MultipartResolver` is configured and the request is multipart, wrap as `MultipartHttpServletRequest`.
4. Query `HandlerMapping`s in order → `HandlerExecutionChain` (handler + interceptors). Annotation apps usually hit **`RequestMappingHandlerMapping`** (`HandlerMethod`).
5. `HandlerInterceptor.preHandle` — **`false`** aborts; that interceptor owns the response. No handler invocation.
6. First `HandlerAdapter` that **`supports`** the handler runs it. For `@RequestMapping` that is **`RequestMappingHandlerAdapter`**: argument resolvers (`@PathVariable`, `@RequestBody`, …), then return-value handling (`HttpMessageConverter` or `ModelAndView`).
7. `postHandle` (successful handler only, **before** view render; `ModelAndView` may be **`null`**). Inverse interceptor order.
8. If a model/view remains, **`ViewResolver`** renders. Annotated controllers may already have written the body in step 6 — then **no view**.
9. `afterCompletion` after rendering (or after the adapter finished the body). Only interceptors whose `preHandle` returned **`true`**. Inverse order. `ex` omits exceptions already handled by a resolver.

```d2
direction: down
f: "Servlet filters" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
ds: "DispatcherServlet\ncontext, locale, multipart" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
hm: "HandlerMapping\nexecution chain" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
pre: "preHandle" {
  width: 160
  height: 45
  style.fill: "#ffe0b2"
}
ha: "HandlerAdapter" {
  width: 200
  height: 45
  style.fill: "#fce4ec"
}
post: "postHandle → View?" {
  width: 200
  height: 50
  style.fill: "#ffe0b2"
}
done: "afterCompletion" {
  width: 180
  height: 45
  style.fill: "#f3e5f5"
}

f -> ds -> hm -> pre -> ha -> post -> done
```

**Fig. 1.** Filters wrap the servlet; interceptors wrap the **mapped handler**. Front controller: [[What is the Front Controller pattern in Spring MVC]], [[What is Spring MVC DispatcherServlet]]. Mapping vs invoke: [[What is HandlerMapping in Spring MVC]], [[What is HandlerAdapter in Spring MVC]]. Callbacks: [[What is a HandlerInterceptor in Spring MVC]].

If no handler matches, Spring 6.1+ throws **`NoHandlerFoundException`** (`throwExceptionIfNoHandlerFound` default **true**, deprecated). A **default servlet** mapping still swallows leftover paths (no MVC 404).

Thrown exceptions are resolved by **`HandlerExceptionResolver`** beans (`ExceptionHandlerExceptionResolver` for `@ExceptionHandler`). See [[What does the ExceptionHandler annotation do]] and [[What is the difference between ControllerAdvice and RestControllerAdvice]].

Async (`Callable` / `DeferredResult`) **exits** the chain without `postHandle` / `afterCompletion` on the first pass; an **ASYNC** dispatch later resumes rendering. Details: [[How do you implement asynchronous request processing in Spring MVC]].

> [!warning] Interceptors are not Security
> Official `HandlerInterceptor` javadoc: path matching can **diverge** from annotated controllers. Use the **filter** chain (Spring Security) as early as possible.

> [!warning] `postHandle` is success-only
> A handler exception skips `postHandle`. `afterCompletion` still runs if `preHandle` returned `true`. `preHandle == false` skips the handler **and** that interceptor’s later callbacks.

> [!warning] View vs body
> `@ResponseBody` / `@RestController` finish the HTTP body **inside the adapter**. There is no `ViewResolver` step on that path.

> [!tip] Interview answer
> **Filters, then `DispatcherServlet`.** It binds context and locale, finds a handler plus interceptors, runs `preHandle`, the adapter invokes the controller, `postHandle`, maybe a view, then `afterCompletion`. Exceptions go to `HandlerExceptionResolver`. That is the same front-controller loop every mapped request takes.
