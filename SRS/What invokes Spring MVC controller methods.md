<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What invokes Spring MVC controller methods?

> [!abstract] Short answer
> **`DispatcherServlet` does not call your `@GetMapping` method.** After **`HandlerMapping`** returns a **`HandlerMethod`**, the servlet picks a **`HandlerAdapter` that `supports` that handler** — for annotated controllers, **`RequestMappingHandlerAdapter`**. The adapter resolves arguments, runs `@ModelAttribute` / `@InitBinder`, **invokes the Java method**, then handles the return value. **`HandlerInterceptor.preHandle` must all return true** before that invoke. Filters and AOP are **not** the MVC invoker.

## Map, intercept, then adapt

`HandlerAdapter` javadoc: the servlet stays **handler-agnostic**. `handle(request, response, handler)` returns a **`ModelAndView`**, or **`null`** if the adapter already wrote the body (`@ResponseBody`). Defaults include **`RequestMappingHandlerAdapter`** (`HandlerMethod`), **`HttpRequestHandlerAdapter`**, and **`SimpleControllerHandlerAdapter`** (legacy `Controller`). Custom adapter beans **replace** that list.

`RequestMappingHandlerAdapter` uses **`HandlerMethodArgumentResolver`** and **`HandlerMethodReturnValueHandler`**. The reflective call is **`InvocableHandlerMethod`**. That is still a **synchronous** adapter call on the servlet thread unless the return type is an async wrapper (`Callable`, `DeferredResult`, …).

```java
public interface HandlerAdapter {
    boolean supports(Object handler);
    ModelAndView handle(HttpServletRequest request, HttpServletResponse response,
            Object handler) throws Exception;
}
```

**Listing 1.** Conceptual Framework 7 SPI. Mapping: [[What is HandlerMapping in Spring MVC]]. Adapter: [[What is HandlerAdapter in Spring MVC]]. Which method: [[How does DispatcherServlet choose which handler method to invoke]]. Full order: [[How does the Spring MVC request lifecycle work]].

```d2
direction: down
ds: "DispatcherServlet" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
hm: "HandlerMapping → HandlerMethod" {
  width: 280
  height: 45
  style.fill: "#fff3e0"
}
ix: "HandlerInterceptor.preHandle" {
  width: 260
  height: 40
  style.fill: "#fce4ec"
}
ha: "RequestMappingHandlerAdapter\ninvoke HandlerMethod" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}

ds -> hm
hm -> ix
ix -> ha
```

**Fig. 1.** Interceptors wrap the adapter call. The adapter is what reflects into `@RequestMapping` methods.

> [!warning] `this.otherMapping()` is not MVC
> A controller calling another of its handler methods is a **plain Java call**. No mapping, no argument resolvers, no `@ResponseBody` write.

> [!warning] Filters are outside the adapter
> Servlet **filters** run before `DispatcherServlet`. They do not invoke `@GetMapping`. Security filters may reject the request so the adapter **never runs**.

> [!warning] Custom `HandlerAdapter` beans
> Declaring adapter beans **drops** `RequestMappingHandlerAdapter` unless you keep it. Then `@Controller` methods are mapped but **never invoked**.

> [!tip] Interview answer
> **`RequestMappingHandlerAdapter` invokes `@RequestMapping` methods.** `DispatcherServlet` only chooses a mapping chain and the first adapter that `supports` the handler. Interceptors can veto; they are not the invoker.
