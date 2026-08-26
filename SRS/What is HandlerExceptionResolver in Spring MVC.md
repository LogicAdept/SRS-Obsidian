<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is `HandlerExceptionResolver` in Spring MVC?

> [!abstract] Short answer
> **`HandlerExceptionResolver` turns exceptions from mapping or handler execution into an error view or an already-written response.** `DispatcherServlet` walks the resolver chain. **`resolveException`** returns a **`ModelAndView`**, an **empty** `ModelAndView` (handled, no view — e.g. status only), or **`null`** (try the next resolver). If every resolver returns `null`, the exception **bubbles to the servlet container**. `@ExceptionHandler` is not a separate bus — it is **`ExceptionHandlerExceptionResolver`**.

## Chain, then container

Spring MVC *Exceptions*: resolvers run for exceptions during **request mapping** or from a **handler**. MVC Java config installs three built-ins (also `DispatcherServlet` defaults):

| Resolver | Role |
| --- | --- |
| `ExceptionHandlerExceptionResolver` | `@ExceptionHandler` on `@Controller` / `@ControllerAdvice` |
| `ResponseStatusExceptionResolver` | `@ResponseStatus` on the exception type (causes since 4.2); also `ResponseStatusException` (5.0+) |
| `DefaultHandlerExceptionResolver` | Spring MVC’s own exceptions → HTTP status (`mvc.support` package) |

Also: **`SimpleMappingExceptionResolver`** (exception class name → error **view** name) for HTML apps. REST-oriented alternative to the default MVC statuses: **`ResponseEntityExceptionHandler`**.

```java
@Override
public void extendHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {
    resolvers.add(0, new MyResolver());
}
```

**Listing 1.** Conceptual: **extend** the default list. `configureHandlerExceptionResolvers` starts **empty** — if you add anything, **you own the whole chain** and must register fully initialized resolvers. `@ExceptionHandler`: [[What does the ExceptionHandler annotation do]]. Advice types: [[What is the difference between ControllerAdvice and RestControllerAdvice]].

```d2
direction: down
ex: "Exception in mapping or handler" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
chain: "HandlerExceptionResolver chain\nnull → next" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
ok: "ModelAndView or empty MAV" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
bubble: "null to the end\n→ Servlet container" {
  width: 260
  height: 55
  style.fill: "#fce4ec"
}

ex -> chain
chain -> ok
chain -> bubble
```

**Fig. 1.** Higher `order` = later in the chain. Lifecycle slot: [[How does the Spring MVC request lifecycle work]].

`handler` on `resolveException` may be **`null`** if nothing was chosen yet (for example multipart failure). After interceptors, exceptions already resolved are **not** passed as `ex` to `afterCompletion`.

Unresolved exceptions (or a 4xx/5xx status) can trigger the container **ERROR** dispatch (`web.xml` `<error-page>`). That is a **new** request into `DispatcherServlet`, not the original handler.

> [!warning] `configureHandlerExceptionResolvers` wipes defaults
> Put one custom resolver in that callback and you **lose** `@ExceptionHandler` / `@ResponseStatus` / default MVC statuses unless you add them back. Prefer **`extendHandlerExceptionResolvers`**.

> [!warning] `@ExceptionHandler` is a resolver, not magic
> No `ExceptionHandlerExceptionResolver` in the chain → those methods never run. Same class of trap as missing `RequestMappingHandlerAdapter`.

> [!warning] `DefaultHandlerExceptionResolver` is not the only default
> Dumps that name only that class skip `ExceptionHandlerExceptionResolver` and `ResponseStatusExceptionResolver`. Boot/MVC config registers the **set**, not one bean.

> [!tip] Interview answer
> **`DispatcherServlet` does not catch exceptions with a giant switch.** It asks `HandlerExceptionResolver` beans in order. `@ExceptionHandler` is `ExceptionHandlerExceptionResolver`. Return `null` to keep going; empty `ModelAndView` means handled with no view. If nothing resolves it, the servlet container’s error page runs.
