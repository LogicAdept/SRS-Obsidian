<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is `HandlerMapping` in Spring MVC?

> [!abstract] Short answer
> **`HandlerMapping` chooses the handler for a request and returns a `HandlerExecutionChain` (handler + interceptors).** `getHandler` may return **`null`**; that is not an error — `DispatcherServlet` asks **every** mapping bean until one matches. Annotation apps use **`RequestMappingHandlerMapping`** (`@RequestMapping` / `@HttpExchange` → `HandlerMethod`). Defaults also include **`BeanNameUrlHandlerMapping`** (bean name starts with `/`). It does **not** invoke the handler — that is **`HandlerAdapter`**.

## Map, do not invoke

`HandlerMapping` javadoc: implementations wrap the handler in **`HandlerExecutionChain`**, optionally with **`HandlerInterceptor`s**. The servlet runs `preHandle` in order, then the adapter, if every `preHandle` returned **`true`**. The handler is a plain **`Object`** (no required interface) so an adapter can target other frameworks’ types.

`DispatcherServlet` detects mapping beans **by type**. Defaults: **`BeanNameUrlHandlerMapping`** and **`RequestMappingHandlerMapping`**. If you declare **any** `HandlerMapping` beans, those defaults are **replaced** — keep `RequestMappingHandlerMapping` if you still want `@RequestMapping`. `Ordered` mappings are sorted; non-`Ordered` ones run last.

```java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/home").setViewName("home");
    }
}
```

**Listing 1.** Conceptual: MVC config registers extra mappings (view controllers) **without** you calling `getHandler`. You rarely invoke `HandlerMapping` yourself. Adapter: [[What is HandlerAdapter in Spring MVC]]. Chain: [[How does the Spring MVC request lifecycle work]]. Servlet: [[What is Spring MVC DispatcherServlet]].

| Implementation | What it maps |
| --- | --- |
| `RequestMappingHandlerMapping` | Type + method `@RequestMapping` / `@HttpExchange` on `@Controller` |
| `BeanNameUrlHandlerMapping` | Bean names / aliases that start with `/` |
| `SimpleUrlHandlerMapping` | Explicit `urlMap` / properties (`PATH=beanName`) |

`DefaultAnnotationHandlerMapping` was the Spring **3.2-deprecated** type-level mapper. Current annotation mapping is **`RequestMappingHandlerMapping`** (method chosen at mapping time, not later in the adapter).

```d2
direction: down
req: "HttpServletRequest" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
hm: "HandlerMapping.getHandler\nnull → try next mapping" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
chain: "HandlerExecutionChain\nhandler + interceptors" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

req -> hm -> chain
```

**Fig. 1.** First mapping that returns a chain wins. Interceptors on that chain: [[What is a HandlerInterceptor in Spring MVC]].

Request attributes after a match (URL mappings): `BEST_MATCHING_HANDLER_ATTRIBUTE`, `BEST_MATCHING_PATTERN_ATTRIBUTE`, `URI_TEMPLATE_VARIABLES_ATTRIBUTE`. Boot 2.6+ / Framework 5.3+ prefer **`PathPattern`** (`usesPathPatterns()`); `LOOKUP_PATH` is **deprecated**.

> [!warning] Custom `HandlerMapping` beans wipe the defaults
> Register `RequestMappingHandlerMapping` (and its adapter) yourself or `@RequestMapping` methods are **never** found. Same trap as custom `HandlerAdapter`s.

> [!warning] Mapping is not “URL only”
> `getHandler` may use session, cookies, API version (`API_VERSION_ATTRIBUTE` since 7.0), or anything the implementation chooses. Returning `null` means “not me”.

> [!warning] It does not call the controller
> `HandlerMapping` **selects**. `HandlerAdapter.handle` **runs**. Interview answers that fuse the two are wrong.

> [!tip] Interview answer
> **`HandlerMapping` turns a request into a `HandlerExecutionChain` — the handler plus interceptors.** Annotation controllers use `RequestMappingHandlerMapping`. `DispatcherServlet` walks mapping beans until one returns a chain; `null` is normal. Invocation is a separate SPI: `HandlerAdapter`.
