<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Spring/Framework/WebMvc #SRS

# What is the difference between Spring MVC async and WebFlux?

> [!abstract] Short answer
> **MVC async** (`DeferredResult`, `Callable`, `SseEmitter`, even **reactive return types**) still sits on the **Servlet** model: **`startAsync()`**, later **`ASYNC` dispatch**, and **blocking writes** on an **`AsyncTaskExecutor`**. **WebFlux** is **asynchronous in every contract** — no servlet async feature, **non-blocking I/O**, no extra thread **per write**. MVC **does not** take reactive **`@RequestBody`**; WebFlux **does**. This is **not** `@Async` and **not** virtual threads.

## Servlet async vs designed-async

Spring MVC *Async Spring MVC compared to WebFlux*:

- Servlet API was **one pass** through Filter–Servlet. Async lets the chain **exit** while the **response stays open**. `DeferredResult`: release the container thread, later **dispatch** the same URL and **skip re-invoking** the controller.
- WebFlux is **not built on the Servlet API** and **does not need** that feature. Async is **intrinsic** at every stage.
- Both can return **reactive types** and stream with **back pressure**. MVC **writes remain blocking** on a **separate thread**. WebFlux writes are **non-blocking**.
- MVC: **no** async/reactive **method arguments** (`@RequestBody`, `@RequestPart`, model attrs). WebFlux: **yes**.
- Servlet async must be **enabled** on the container (`asyncSupported`).

Dump lumping **`@Async`** with this is wrong. `@Async` runs a method on an executor; **Servlet 3 async** is request lifecycle. Offload: [[How do you implement asynchronous request processing in Spring MVC]].

```java
@GetMapping("/quotes")
@ResponseBody
public DeferredResult<String> quotes() {
    DeferredResult<String> deferredResult = new DeferredResult<>();
    // another thread later: deferredResult.setResult(result);
    return deferredResult;
}
```

**Listing 1.** Framework MVC async sample — container thread is released; **I/O to the client can still block**. WebFlux: return `Mono`/`Flux` — [[How do you implement a reactive REST controller in WebFlux]].

```d2
direction: down
mvc: "MVC async\nstartAsync + ASYNC dispatch\nblocking write on executor" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
wf: "WebFlux\nnon-blocking all the way\nevent-loop workers" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** SSE: MVC `SseEmitter` vs WebFlux `Flux<ServerSentEvent>` — [[How do you implement Server-Sent Events in WebFlux]]. Broader MVC vs WebFlux: [[What is the difference between Spring MVC and Spring WebFlux]].

Current Framework servers for WebFlux: **Netty, Tomcat, Jetty, Servlet container** — **not** a live Undertow row.

> [!warning] Reactive return type on MVC ≠ WebFlux
> A `Mono` from an MVC controller is adapted like `DeferredResult`. **Request body** is still blocking. Writes still use the async executor.

> [!warning] Not virtual threads
> `spring.threads.virtual.enabled` keeps **blocking** MVC style — [[When should you use WebFlux versus Spring MVC versus virtual threads]].

> [!tip] Interview answer
> **MVC async releases the servlet thread but still uses Servlet async + blocking writes.** WebFlux is non-blocking end-to-end and accepts reactive **arguments**. `@Async` is a different feature.

## See also

- [[How do you implement asynchronous request processing in Spring MVC]]
- [[What is the difference between Spring MVC and Spring WebFlux]]
- [[What is Spring WebFlux]]
- [[How does the WebFlux event loop work]]
- [[How do you implement Server-Sent Events in WebFlux]]
- [[When should you use WebFlux versus Spring MVC versus virtual threads]]
