<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SecurityContext #SRS

# How do you propagate SecurityContext to async threads?

> [!abstract] Short answer
> **Wrap the executor** so each task is a **`DelegatingSecurityContextRunnable`**: the **`SecurityContext` is copied when the task is submitted**, installed on the worker, then **`SecurityContextHolder.clearContext()` in a `finally`**. Use **`DelegatingSecurityContextExecutor`** (or **`DelegatingSecurityContextAsyncTaskExecutor`** for **`@Async`**). **`MODE_INHERITABLETHREADLOCAL`** only copies onto **true child threads at creation** — not onto reused pool workers. Spring MVC **`Callable`** async is a **different** path ([[What is WebAsyncManagerIntegrationFilter]]).

## Default holder does not follow the worker

**`SecurityContextHolder`** defaults to **`MODE_THREADLOCAL`**. Filters populate **`Authentication`** on the **request thread**; a pool thread, a `new Thread(...)`, or an **`@Async`** worker is a **different `ThreadLocal`**, so **`getContext().getAuthentication()`** is empty and **`@PreAuthorize`** on that worker does not see the caller. Why the default is ThreadLocal: [[Why does SecurityContextHolder use ThreadLocal]].

## Copy at submit: `DelegatingSecurityContextExecutor`

The concurrency support’s primitive is **`DelegatingSecurityContextRunnable`**. Conceptually it is:

```java
public void run() {
	try {
		SecurityContextHolder.setContext(securityContext);
		delegate.run();
	} finally {
		SecurityContextHolder.clearContext();
	}
}
```

**Listing 1.** Official pattern — set the captured context, run the task, always clear.

**`DelegatingSecurityContextExecutor`** wraps a delegate **`Executor`** and wraps every **`execute(Runnable)`** that way. Construct it **without** a `SecurityContext` argument and it reads **`SecurityContextHolder` at submit time** (the user who called `execute`), not later when the worker runs. Inject that executor so callers stay unaware of Spring Security. A one-off task can use **`DelegatingSecurityContextRunnable`** / **`DelegatingSecurityContextCallable`** directly.

For **`@Async`**, wrap the **`TaskExecutor`** with **`DelegatingSecurityContextAsyncTaskExecutor`** (same family: **`DelegatingSecurityContextTaskExecutor`**, **`DelegatingSecurityContextExecutorService`**, **`DelegatingSecurityContextScheduledExecutorService`**, **`DelegatingSecurityContextTaskScheduler`**). A plain **`@EnableAsync`** executor does **not** copy the holder.

```java
Executor delegate = Executors.newFixedThreadPool(8);
Executor executor = new DelegatingSecurityContextExecutor(delegate);

executor.execute(() -> {
	Authentication auth = SecurityContextHolder.getContext().getAuthentication();
	// same principal as at executor.execute(...)
});
```

**Listing 2.** Capture-at-submit wrapper around a JDK pool — not `MODE_INHERITABLETHREADLOCAL`.

Pass an explicit **`SecurityContext`** into the constructor when every task should run as a **fixed** principal (elevated background jobs), instead of the submitting user.

## `MODE_INHERITABLETHREADLOCAL` is not a pool fix

**`SecurityContextHolder.setStrategyName(MODE_INHERITABLETHREADLOCAL)`** (or the **`spring.security.strategy`** system property) uses Java **`InheritableThreadLocal`**: a **newly spawned child thread** inherits the parent’s identity. Set the strategy **at startup**, before any thread touches the holder — it is **JVM-wide**. Pooled workers are **created once and reused**; they do not re-inherit per task, so this mode does **not** replace submit-time wrapping. Details: [[What is MODE_INHERITABLETHREADLOCAL in SecurityContextHolder]].

```d2
direction: right
submit: "Submit thread\ngetContext() at execute()" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
wrap: "DelegatingSecurityContextExecutor\nwrap Runnable / Callable" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
worker: "Pool worker\nsetContext → run → clearContext" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
inherit: "MODE_INHERITABLETHREADLOCAL\nonly at child Thread creation" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

submit -> wrap -> worker
submit -> inherit
```

**Fig. 1.** Executor wrappers copy per submission and clear after the task; inheritable mode only runs when a child thread is created.

## MVC `Callable` is not your `Executor`

With **no extra configuration**, Spring Security copies the holder onto the thread that runs a **controller-returned `Callable`**, via **`WebAsyncManager`** (context taken when **`startCallableProcessing`** runs). That is **[[What is WebAsyncManagerIntegrationFilter]]**, not **`@Async`** and not **`Executors.newFixedThreadPool`**. **`DeferredResult`** has **no** automatic integration — use the concurrency wrappers if that worker must see **`Authentication`**.

> [!warning] `@Async` and raw pools skip `WebAsyncManagerIntegrationFilter`
> A default-chain **`WebAsyncManagerIntegrationFilter`** does **not** wrap **`Executors.newFixedThreadPool`** or **`@Async`**. Those see an **empty `SecurityContextHolder`** unless you wrap the executor (or a single `Runnable`) with the **`DelegatingSecurityContext*`** types. Forgetting **`clearContext()`** on a pooled worker leaks the previous user’s **`Authentication`**.

> [!tip] Interview answer
> SecurityContextHolder is ThreadLocal, so async workers start empty. Wrap the Executor (or @Async TaskExecutor) with DelegatingSecurityContextExecutor / DelegatingSecurityContextAsyncTaskExecutor so the context is copied at submit and cleared in finally. MODE_INHERITABLETHREADLOCAL only helps true child threads, not reused pool workers. WebAsyncManagerIntegrationFilter covers MVC Callable on the request, not your own executors.
