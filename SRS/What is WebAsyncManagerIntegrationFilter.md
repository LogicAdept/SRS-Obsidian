<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `WebAsyncManagerIntegrationFilter`?

> [!abstract] Short answer
> An **`OncePerRequestFilter`** that hooks Spring MVC **`WebAsyncManager`** (`Callable` / deferred MVC async) so the **worker thread** still has **`SecurityContext`**. It registers **`SecurityContextCallableProcessingInterceptor`**: **`beforeConcurrentHandling`** copies the holder, **`preProcess`** restores it on the async thread, **`postProcess`** **clears**. Default TRACE **`(2/15)`**, after [[What is DisableEncodeUrlFilter]], before [[What is SecurityContextHolderFilter]]. Dump “~0” is **wrong**. It does **not** wrap `@Async` or `Executors.newFixedThreadPool()`.

## MVC `Callable`, not `@Async`

```d2
direction: down
req: "REQUEST thread\nSecurityContextHolder" {
  width: 240
  height: 50
}
f: "WebAsyncManagerIntegrationFilter" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
w: "MVC async worker\npreProcess restores context" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

req -> f
f -> w: "WebAsyncManager Callable"
```

**Fig. 1.** Spring MVC async (`WebAsyncTask`, `Callable` return). `@Async` on a `@Service` is a **different** interceptor/executor — use [[What is DelegatingSecurityContextExecutor]] / [[How do you propagate SecurityContext to async threads]]. See [[What is OncePerRequestFilter]], [[What is FilterOrderRegistration]], and [[How do you implement asynchronous request processing in Spring MVC]].

`FilterChainProxy` still iterates this filter on [[What is VirtualFilterChain in Spring Security]]; it does not start the MVC worker by itself.

```text
TRACE FilterChainProxy : Invoking WebAsyncManagerIntegrationFilter (2/15)
```

**Listing 1.** Always-on default (HttpSecurity / namespace). No DSL switch. `setSecurityContextHolderStrategy` since **5.8**.

> [!warning] Your `Executor` is not `WebAsyncManager`
> `Executors.newFixedThreadPool()` / `@Async` do **not** get this interceptor. The worker’s `SecurityContextHolder` is empty unless you wrap with `DelegatingSecurityContextRunnable` / `DelegatingSecurityContextExecutor`. Mixing that up is why a controller `Callable` is authenticated and a `@Async` mailer is anonymous.

> [!tip] Interview answer
> WebAsyncManagerIntegrationFilter sits near the front of the default chain and copies SecurityContext onto Spring MVC async Callables via SecurityContextCallableProcessingInterceptor. It is TRACE slot 2, not the first filter. It does not help @Async or a raw thread pool — those need DelegatingSecurityContextExecutor.
