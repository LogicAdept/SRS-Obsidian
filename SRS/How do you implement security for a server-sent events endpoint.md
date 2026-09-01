<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/SecurityContext #SRS

# How do you implement security for a server-sent events endpoint?

> [!abstract] Short answer
> Treat the stream as a **long-lived HTTP GET**. Authorize it with **`authorizeHttpRequests`** (for example **`authenticated()`**) so the **filter chain** runs **before** the controller returns **`SseEmitter`**. **`CsrfFilter` ignores GET** by default — do not disable CSRF “for SSE”. After **`startAsync()`**, filters exit while the response stays open; **`send` on another thread** needs **`DelegatingSecurityContextRunnable`** (unlike **`Callable`**).

## The GET is the security boundary

Spring MVC SSE is **`SseEmitter`** (`ResponseBodyEmitter`) with **`produces = TEXT_EVENT_STREAM`**. Spring MVC calls **`request.startAsync()`**, the **filter–servlet chain exits**, and the **response stays open** for later **`emitter.send(...)`**.

Authorization therefore happens **once**, on the initial GET, in **`AuthorizationFilter`**. There is no per-event re-check of **`authenticated()`**.

```java
@Bean
SecurityFilterChain sse(HttpSecurity http) throws Exception {
	http
		.authorizeHttpRequests(authorize -> authorize
			.requestMatchers("/events").authenticated()
			.anyRequest().authenticated())
		.httpBasic(Customizer.withDefaults()); // one option; session cookies work too
	return http.build();
}

@GetMapping(path = "/events", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
SseEmitter events() {
	SseEmitter emitter = new SseEmitter(); // timeout: MVC config, else container default
	Runnable push = () -> { /* emitter.send(...); emitter.complete(); */ };
	new Thread(new DelegatingSecurityContextRunnable(push)).start();
	return emitter;
}
```

**Listing 1.** Conceptual chain rule plus a worker that restores **`SecurityContextHolder`**. **`httpBasic()`** is optional — the GET still needs **some** authentication mechanism.

`CsrfFilter.DEFAULT_CSRF_MATCHER` **ignores GET, HEAD, TRACE, OPTIONS**. A browser GET for `text/event-stream` does not need a CSRF token. Do not treat SSE as a reason to **`csrf.disable()`**.

Spring Security **auto-copies `SecurityContext` onto `Callable`** via **`WebAsyncManager`**. **`SseEmitter` is like `DeferredResult`**: your thread, **no automatic integration**. Wrap the worker with **`DelegatingSecurityContextRunnable`** / **`DelegatingSecurityContextExecutor`**. **`AsyncContext.start(Runnable)`** is overridden to propagate context; a **raw `new Thread`** is not. XML setups need **`async-supported`** and dispatcher **`ASYNC`** on **`springSecurityFilterChain`**.

```d2
direction: down
get: "GET /events" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
chain: "SecurityFilterChain\nauthenticated()" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
ctrl: "SseEmitter +\nstartAsync()" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
worker: "DelegatingSecurityContextRunnable\nemitter.send" {
  width: 280
  height: 50
  style.fill: "#c8e6c9"
}

get -> chain
chain -> ctrl
ctrl -> worker
```

**Fig. 1.** Filters authorize the **open**. Later writes run **off** the filter chain ([[How do you propagate SecurityContext to async threads]], [[What is CsrfFilter in Spring Security]], [[How do you implement Server-Sent Events in WebFlux]]).

Set **`SseEmitter(Long timeout)`** if the container default is too short. Send **comment heartbeats**; the Servlet API does **not** notify you when the client drops. **`HttpSession` invalidation / `invalidSessionUrl`** apply to a **later request** with an expired session id, not to each SSE write on an already-started async response ([[How do you configure HTTP Basic authentication in Spring Security]]).

> [!warning] CSRF is not the SSE problem
> **`CsrfFilter` skips GET**. Turning CSRF off for `/sse/**` does not authenticate the stream. The trap is an **unauthenticated GET**, not a missing token.

> [!warning] The open stream is not re-authorized
> **`AuthorizationFilter` does not run per `send`**. Worker threads do not see **`SecurityContextHolder`** unless you propagate it. **`SseEmitter` timeout** is the MVC/container async timeout, not Spring Security session expiry. Capture the principal on subscribe if later events must stay user-scoped.

> [!tip] Interview answer
> Secure SSE the same way as any other GET: authorizeHttpRequests before the controller returns SseEmitter. CSRF is off for GET by default. After startAsync the filter chain is gone, so wrap emitter workers with DelegatingSecurityContextRunnable — Callable is the only return type Spring Security wires automatically. Session invalid-session handling is for the next HTTP request, not each event write.
