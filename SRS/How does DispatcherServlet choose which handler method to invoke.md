<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# How does `DispatcherServlet` choose which handler method to invoke?

> [!abstract] Short answer
> It **does not scan methods itself.** It asks each **`HandlerMapping`** for a **`HandlerExecutionChain`**. For `@Controller` methods that is **`RequestMappingHandlerMapping`**, which matches a **`RequestMappingInfo`**: path, HTTP method, params, headers, consumes, produces, and (Framework 7) API **version**. **`getMatchingCondition`** must succeed; among matches **`compareTo`** picks the **best** (more specific path, tighter conditions). The handler object is usually a **`HandlerMethod`**. **`HandlerAdapter`** then **invokes** it — mapping does not call the method.

## Map first, invoke second

`HandlerMapping.getHandler` may use URL, session, cookies, or anything the implementation chooses. **`null` is not an error** — the servlet tries the next mapping bean. `Ordered` mappings run first. Defaults include **`RequestMappingHandlerMapping`** and **`BeanNameUrlHandlerMapping`**.

`RequestMappingInfo` **combines** type-level and method-level `@RequestMapping`. A match returns a new info with patterns **sorted best-first**. Ambiguous mappings (two methods equally specific) fail **at startup**, not per request.

After a URL mapping match, the request holds `BEST_MATCHING_HANDLER_ATTRIBUTE`, `BEST_MATCHING_PATTERN_ATTRIBUTE`, `URI_TEMPLATE_VARIABLES_ATTRIBUTE`. Path matching defaults to **`PathPattern`** (6.0+).

```java
@GetMapping(path = "/pets/{id}", produces = "application/json")
public Pet json(@PathVariable long id) { … }

@GetMapping(path = "/pets/{id}", produces = "text/html")
public String html(@PathVariable long id) { … }
```

**Listing 1.** Conceptual: same path, **`produces`** + `Accept` decide which `HandlerMethod` wins. Mapping SPI: [[What is HandlerMapping in Spring MVC]]. Invoke: [[What is HandlerAdapter in Spring MVC]]. Full chain: [[How does the Spring MVC request lifecycle work]].

```d2
direction: down
ds: "DispatcherServlet" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
hm: "HandlerMapping.getHandler" {
  width: 280
  height: 45
  style.fill: "#fff3e0"
}
info: "RequestMappingInfo\npath method params headers\nconsumes produces version" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
hmeth: "HandlerMethod" {
  width: 200
  height: 40
  style.fill: "#fce4ec"
}

ds -> hm
hm -> info
info -> hmeth
```

**Fig. 1.** First mapping that returns a chain wins. `RequestMappingHandlerAdapter` then binds arguments and calls the Java method.

No match → **`NoHandlerFoundException`** (unless a default-servlet / static `/**` handler swallowed the path). Path matches, method does not → **`HttpRequestMethodNotSupportedException`**. Media type mismatch → **`HttpMediaTypeNotAcceptableException` / `HttpMediaTypeNotSupportedException`**.

> [!warning] Custom `HandlerMapping` beans
> Declaring **any** mapping beans **replaces** servlet defaults. Keep **`RequestMappingHandlerMapping`** or `@RequestMapping` methods are invisible.

> [!warning] Mapping ≠ interceptor security
> CORS and `produces` participate in **which method is chosen**. Spring Security still belongs in the **filter** chain, not as a substitute for mapping.

> [!warning] More specific path wins
> `/pets/{id}` vs `/pets/me`: after `getMatchingCondition`, **`compareTo`** prefers the more specific pattern. Two equally specific methods are a **startup** failure.

> [!tip] Interview answer
> **`DispatcherServlet` asks `HandlerMapping` beans until one returns a `HandlerExecutionChain`.** For annotated controllers, `RequestMappingHandlerMapping` scores `RequestMappingInfo` (path, verb, headers, media types). The winner is a `HandlerMethod`; `HandlerAdapter` is what actually invokes it.
