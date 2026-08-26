<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What return types can a Spring MVC controller method have?

> [!abstract] Short answer
> **Many, and they mean different pipelines.** A **`String` is a view name** (unless `@ResponseBody` / `@RestController`). **`@ResponseBody` / `ResponseEntity` / `HttpEntity` / `HttpHeaders`** write through **`HttpMessageConverter`s**. **`Model` / `Map` / `@ModelAttribute` / `ModelAndView` / `View`** go to **`ViewResolver`**. **`void`/`null`** means “already handled” only with a servlet output argument, `@ResponseStatus`, or an ETag/`lastModified` check — otherwise REST empty body or a default view name. Async: **`Callable`**, **`DeferredResult`**, **`CompletableFuture`**, **`SseEmitter`**, **`StreamingResponseBody`**, plus Reactor **`Mono`/`Flux`** adapted on the **servlet** async stack.

## Body vs view vs later

MVC *Return Values*: reactive types are supported **for all** of these (via `ReactiveAdapterRegistry`). `Mono` ≈ `DeferredResult`. `Flux` streams if `Accept` is `text/event-stream` or `application/json+stream`; otherwise it is **collected to a `List`**.

| Return | What Spring does |
| --- | --- |
| `@ResponseBody` value | Converters → HTTP body |
| `ResponseEntity` / `HttpEntity` | Status, headers, body via converters |
| `HttpHeaders` | Headers, **no** body |
| `ErrorResponse` / `ProblemDetail` | RFC 9457 body |
| `String` | **View name** + implicit model |
| `View` | Render that instance + implicit model |
| `Model` / `Map` | Attributes; view name from **`RequestToViewNameTranslator`** |
| `@ModelAttribute` value | One model attribute; same implicit view name (`@ModelAttribute` optional) |
| `ModelAndView` | View + model, optional status |
| `FragmentsRendering` / `Collection<ModelAndView>` | HTML fragments (6.2+) |
| `void` / `null` | Fully handled **if** `ServletResponse`/`OutputStream`/`@ResponseStatus`/ETag check; else REST no body or HTML default view |
| `DeferredResult` | Any of the above, later, **any** thread |
| `Callable` / `WebAsyncTask` | Same, on MVC’s **`AsyncTaskExecutor`** |
| `CompletionStage` / `CompletableFuture` | Convenience vs `DeferredResult` |
| `ResponseBodyEmitter` / `SseEmitter` | Stream objects through converters |
| `StreamingResponseBody` | Async write to `OutputStream` |
| Unresolved other | Model attribute unless **`BeanUtils.isSimpleProperty`** (then left unresolved) |

```java
@GetMapping("/page")
public String page(Model model) {
    model.addAttribute("title", "Home");
    return "home";
}

@GetMapping("/api/{id}")
public ResponseEntity<Account> api(@PathVariable long id) {
    return ResponseEntity.ok(accounts.find(id));
}

@GetMapping("/sse")
public SseEmitter stream() {
    SseEmitter emitter = new SseEmitter();
    events.register(emitter);
    return emitter;
}
```

**Listing 1.** Conceptual: view name vs `ResponseEntity` vs stream. Model types: [[What is the difference between Model ModelMap and ModelAndView]]. Body vs entity: [[What is the difference between ResponseBody and ResponseEntity]]. JSON: [[How do you return JSON from a Spring MVC controller]]. Async: [[How do you implement asynchronous request processing in Spring MVC]]. Problems: [[What is ProblemDetail in Spring]].

```d2
direction: down
ret: "handler return" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
view: "ViewResolver\nString Model ModelAndView" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
body: "HttpMessageConverter\n@ResponseBody ResponseEntity" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
async: "Servlet startAsync\nCallable DeferredResult Flux" {
  width: 300
  height: 50
  style.fill: "#fce4ec"
}

ret -> view
ret -> body
ret -> async
```

**Fig. 1.** Same `HandlerAdapter`; the return type picks view rendering, converter write, or async resume.

> [!warning] `@RestController` + `String` is a body
> Type-level `@ResponseBody` makes `"home"` the **payload**, not the template `home`. Use `@Controller` (no `@ResponseBody`) for view names.

> [!warning] `void` is not always 200 empty
> Without `@ResponseStatus` or a response argument, HTML controllers still look up a **default view name**. REST `void` is “no body” only in that REST path.

> [!warning] `Mono` on MVC is not WebFlux
> Returning `Mono` still uses **Servlet async** and the MVC adapter. It does not switch the app to Netty / `DispatcherHandler`.

> [!tip] Interview answer
> **View name `String`, `ModelAndView`, `Model`/`Map`, `@ResponseBody` POJO, `ResponseEntity`, `void`, plus async wrappers (`Callable`, `DeferredResult`, `SseEmitter`).** `@RestController` turns objects (including `String`) into the HTTP body. Simple types without `@ResponseBody` are **not** treated as model attributes.
