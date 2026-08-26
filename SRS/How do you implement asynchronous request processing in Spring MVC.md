<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Async #SRS

# How do you implement asynchronous request processing in Spring MVC?

> [!abstract] Short answer
> Return a Servlet-async wrapper from the controller so the container thread can **exit while the response stays open**. **`Callable` / `WebAsyncTask`**: Spring runs the work on an **`AsyncTaskExecutor`**. **`DeferredResult`**: you call **`setResult`** (or **`setErrorResult`**) later from **any** thread. Streams: **`ResponseBodyEmitter`**, **`SseEmitter`**, **`StreamingResponseBody`**. This is **Servlet 3 `request.startAsync()`**, not WebFlux and not `@Async`.

## Release the container thread

Spring MVC *Asynchronous Requests*: `startAsync()` lets the servlet and filters **return**; the response remains open. When the result is ready, Spring issues an **`ASYNC` dispatch** to the same URL. The controller is mapped again but **not re-invoked**; the produced value is used as if the method had returned it.

```java
@GetMapping("/quote")
@ResponseBody
public DeferredResult<String> quote() {
    DeferredResult<String> deferred = new DeferredResult<>(5_000L);
    quoteService.onComplete(deferred::setResult);
    return deferred;
}

@PostMapping("/upload")
public Callable<String> processUpload(MultipartFile file) {
    return () -> store(file);
}
```

**Listing 1.** Conceptual Spring Framework 7 pattern. `Callable` is submitted to the configured executor; `DeferredResult` is completed from your own thread. Full return-type list: [[What return types can a Spring MVC controller method have]]. Vs WebFlux: [[What is the difference between Spring MVC async and WebFlux]].

```java
@GetMapping(path = "/events", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public SseEmitter events() {
    SseEmitter emitter = new SseEmitter();
    broker.subscribe(event -> {
        try {
            emitter.send(event);
        } catch (IOException ignored) {
            // container drives completeWithError on disconnect
        }
    });
    return emitter;
}
```

**Listing 2.** Conceptual SSE. `SseEmitter` extends `ResponseBodyEmitter`. Do not call `complete` after an `IOException` from a gone client — the container already starts error completion.

```d2
direction: down
ctrl: "Controller returns\nCallable / DeferredResult" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
start: "request.startAsync()\nservice + filters exit" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
work: "Executor or your thread\nproduces the value" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
dispatch: "ASYNC dispatch\nresume as if returned" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}

ctrl -> start
start -> work
work -> dispatch
```

**Fig. 1.** One pass through the filter chain exits; a later ASYNC dispatch finishes the response.

Configure timeouts and the executor on `WebMvcConfigurer.configureAsyncSupport`. Java servlet initializers (`AbstractAnnotationConfigDispatcherServletInitializer`) set **`asyncSupported=true`** by default. Boot `DynamicRegistrationBean` also defaults async to **true**. Custom `FilterRegistrationBean` mappings still need **`DispatcherType.ASYNC`**.

> [!warning] Default `AsyncTaskExecutor` is not production-ready
> Official MVC config: the executor used for **`Callable`** (and **blocking writes** of reactive/`SseEmitter` streams) is **not suitable under load**. Set one via `configureAsyncSupport.setTaskExecutor`. Timeout, if unset, is **the servlet container’s** default.

> [!warning] Not WebFlux and not `@Async`
> MVC async is still **blocking writes** on a helper thread. Method **arguments** (`@RequestBody`, model attributes) stay synchronous. `@Async` is a scheduling annotation; it does not start Servlet async. Same-app stack choice: [[Can you use Spring MVC and WebFlux in the same application]].

> [!warning] Interceptors skip `postHandle` on the first pass
> Use **`AsyncHandlerInterceptor.afterConcurrentHandlingStarted`**. `setResult` returns **`false`** if the result was already set or the request **expired**.

> [!warning] Detect disconnects with heartbeats
> The Servlet API does not notify when the client drops. Periodic SSE comments (or WebSocket heartbeats) make the next write fail so you can stop producing.

> [!tip] Interview answer
> **Return `Callable` so Spring runs the job on a task executor, or `DeferredResult` so some other thread calls `setResult`.** Either way the servlet thread is released via `startAsync` and processing resumes on an ASYNC dispatch. For streams use `SseEmitter`. Configure a real `AsyncTaskExecutor` — the default is not for production — and do not confuse this with WebFlux or `@Async`.
