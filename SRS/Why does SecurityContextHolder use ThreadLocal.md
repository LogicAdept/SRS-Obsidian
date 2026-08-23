<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS

# Why does SecurityContextHolder use ThreadLocal?

> [!abstract] Short answer
> **`SecurityContextHolder` defaults to `MODE_THREADLOCAL`**, storing the current **`SecurityContext`** (and its **`Authentication`**) in a **`ThreadLocal`**. Any code on the **same request thread** can call **`SecurityContextHolder.getContext()`** without passing the context through every method parameter — the pattern servlet containers already use (one thread per HTTP request).

## How the default strategy works

Spring Security treats **`SecurityContextHolder`** as a static façade over a pluggable **`SecurityContextHolderStrategy`**. Unless you change it at JVM startup, the strategy is **`MODE_THREADLOCAL`**.

With that default:

1. Filters such as **`SecurityContextHolderFilter`** load or create a **`SecurityContext`** at the start of the request.
2. Authentication filters set **`Authentication`** on that context.
3. Services, repositories, and **`@PreAuthorize`** advice read **`SecurityContextHolder.getContext().getAuthentication()`** on the same thread.
4. At the end of the request, Spring Security **clears** the holder so the worker thread is clean for the next request.

The servlet authentication architecture guide states that **`ThreadLocal` is appropriate on servers** and that **`FilterChainProxy` ensures the context is always cleared** after the request — provided you stay on the request thread and let the filter chain finish normally.

```java
SecurityContext context = SecurityContextHolder.getContext();
Authentication authentication = context.getAuthentication();
String username = authentication.getName();
```

**Listing 1.** Typical read path — no explicit `SecurityContext` parameter needed on the call stack.

## Alternative strategies (when ThreadLocal is not enough)

| Strategy | Use case |
|----------|----------|
| **`MODE_THREADLOCAL`** (default) | Servlet / MVC: one thread handles one request |
| **`MODE_INHERITABLETHREADLOCAL`** | Child threads spawned **from** the request thread should inherit the parent's context |
| **`MODE_GLOBAL`** | Single-user desktop / Swing apps — **not for web servers** |

**`MODE_INHERITABLETHREADLOCAL`** copies context into **new** child threads via Java's **`InheritableThreadLocal`**. That does **not** solve arbitrary thread pools: a pooled worker may still carry a stale context from a **previous** task if clearing and propagation are wrong.

For async or background work, the concurrency guide recommends **`DelegatingSecurityContextRunnable`** / **`DelegatingSecurityContextExecutor`**, which copy the context at **submit time** and **`clearContext()` in a `finally` block** on the worker thread — safer than flipping the global strategy for pooled executors.

```d2
direction: right
request: "HTTP request thread\nSecurityContext in ThreadLocal" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
service: "Service / @PreAuthorize\ngetContext() on same thread" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
pool: "Thread pool worker\n(no context unless wrapped)" {
  width: 220
  height: 70
  style.fill: "#fce4ec"
}
clear: "Filter chain end\nclearContext()" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}

request -> service -> clear
request -> pool
```

**Fig. 1.** ThreadLocal fits the request thread; other threads need explicit propagation or delegation wrappers.

> [!warning] Thread pools leak identities when context is not cleared
> If **`SecurityContextHolder` is not cleared** after a request, the next task on that pooled thread can still see the **previous user's `Authentication`**. Spring Security's filters normally prevent this on the servlet thread, but **custom async code** that touches the holder without **`DelegatingSecurityContextExecutor`** (or without clearing in `finally`) can leak or drop the wrong principal. See [[How do you propagate SecurityContext to async threads]] and [[What is WebAsyncManagerIntegrationFilter]].

> [!tip] Interview answer
> SecurityContextHolder uses ThreadLocal by default so Authentication is available anywhere on the same request thread without threading SecurityContext through every method. FilterChainProxy clears it after the request. Async or pooled threads do not get it automatically — wrap executors with DelegatingSecurityContextExecutor rather than blindly switching to MODE_INHERITABLETHREADLOCAL.
