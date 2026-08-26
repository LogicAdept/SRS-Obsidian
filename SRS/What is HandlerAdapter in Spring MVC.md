<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is `HandlerAdapter` in Spring MVC?

> [!abstract] Short answer
> **`HandlerAdapter` is how `DispatcherServlet` invokes a handler it does not understand.** After `HandlerMapping` returns a handler object, the servlet finds the **first adapter whose `supports(handler)` is true** and calls **`handle`**. Annotated `@RequestMapping` methods use **`RequestMappingHandlerAdapter`** (`HandlerMethod` → argument resolvers → return-value handlers). `handle` returns a **`ModelAndView`**, or **`null`** if the adapter already wrote the response.

## SPI so the servlet stays handler-agnostic

`HandlerAdapter` javadoc: MVC SPI, **not** an application API. The servlet contains **no** handler-type-specific code. A handler may be any `Object` — other frameworks, or annotation objects with **no** required interface. Adapters may implement **`Ordered`**; non-ordered ones have lowest priority.

`DispatcherServlet` defaults: **`HttpRequestHandlerAdapter`** (`HttpRequestHandler`), **`SimpleControllerHandlerAdapter`** (legacy `Controller` interface), and **`RequestMappingHandlerAdapter`**. Like mappings, adapter beans are detected **by type**; declaring your own **replaces** that default list.

```java
public interface HandlerAdapter {

    boolean supports(Object handler);

    ModelAndView handle(HttpServletRequest request, HttpServletResponse response,
            Object handler) throws Exception;
}
```

**Listing 1.** Conceptual Spring Framework 7 contract. Call `supports` before `handle`. Mapping vs invoke: [[What is HandlerMapping in Spring MVC]]. Lifecycle: [[How does the Spring MVC request lifecycle work]].

`RequestMappingHandlerAdapter` (since 3.1) supports `@RequestMapping` **`HandlerMethod`s**. It uses **`HandlerMethodArgumentResolver`** (`@PathVariable`, `@RequestBody`, …) and **`HandlerMethodReturnValueHandler`**. Add extras with `setCustomArgumentResolvers` / `setCustomReturnValueHandlers`. Also runs `@InitBinder` and `@ModelAttribute` methods (`INIT_BINDER_METHODS`, `MODEL_ATTRIBUTE_METHODS`).

```d2
direction: down
h: "Handler object\n(HandlerMethod, HttpRequestHandler, …)" {
  width: 340
  height: 70
  style.fill: "#e3f2fd"
}
s: "adapters: first supports(handler)" {
  width: 300
  height: 60
  style.fill: "#fff3e0"
}
run: "handle → ModelAndView or null" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}

h -> s -> run
```

**Fig. 1.** The servlet does not `invoke` your controller. Body vs view: [[How do you return JSON from a Spring MVC controller]], [[What is a ViewResolver in Spring MVC]].

`HttpRequestHandler.handleRequest` writes the servlet response itself → adapter returns **`null`**. `@ResponseBody` is the same idea inside `RequestMappingHandlerAdapter`.

> [!warning] Custom adapters drop `@RequestMapping`
> If you register any `HandlerAdapter` beans, also register **`RequestMappingHandlerAdapter`**. Same rule as custom `HandlerMapping`s.

> [!warning] Mapping is not invocation
> `HandlerMapping` **selects** (often a `HandlerMethod`). `HandlerAdapter` **runs** it. Fusing the two is the usual interview mix-up.

> [!warning] No supporting adapter is a servlet error
> `getHandlerAdapter` throws if **no** installed adapter `supports` the handler. That is a configuration bug (wrong handler type, missing default adapters), not a 404.

> [!tip] Interview answer
> **`DispatcherServlet` never calls your controller directly.** It asks `HandlerAdapter.supports`, then `handle`. For `@RequestMapping` that adapter is `RequestMappingHandlerAdapter`, which binds arguments and either returns a `ModelAndView` or writes the body and returns `null`.
