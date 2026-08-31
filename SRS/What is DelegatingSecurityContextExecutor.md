<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SecurityContext #SRS

# What is DelegatingSecurityContextExecutor?

> [!abstract] Short answer
> **`DelegatingSecurityContextExecutor`** (`org.springframework.security.concurrent`) is an **`Executor`** that wraps another **`Executor`** and wraps each **`Runnable`** in a **`DelegatingSecurityContextRunnable`**. That copies a **`SecurityContext` onto the worker**, runs the task, then **`SecurityContextHolder.clearContext()` in a `finally`**. The one-arg constructor captures **`SecurityContextHolder` at `execute()`** (submit time). It is **not** a global ThreadLocal — only tasks submitted **through this executor** see the context.

## Wrapper around an `Executor`

Spring Security stores **`Authentication`** in a **`ThreadLocal`** by default ([[Why does SecurityContextHolder use ThreadLocal]]), so a pool thread does not see the submitter’s context. **`DelegatingSecurityContextExecutor`** is the concurrency-support type that hides that from callers: you inject an **`Executor`**, submit ordinary **`Runnable`s**, and the wrapper does the Security work.

It delegates execution to the inner executor. On **`execute(Runnable)`** it wraps the task, then calls the delegate. **`DelegatingSecurityContextRunnable`** is the actual transfer:

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

**Listing 1.** What every submitted task becomes — set, run, always clear.

## Two constructors

**Fixed context** — `new DelegatingSecurityContextExecutor(delegate, securityContext)`: every task runs as **that** `SecurityContext`. Useful for background work that should always run as a **privileged** user, independent of who submitted the task.

**Submitter’s context** — `new DelegatingSecurityContextExecutor(delegate)`: at each **`execute(Runnable)`**, the wrapper reads **`SecurityContextHolder.getContext()`** and binds **that** snapshot to the worker. The task runs as the user who **submitted** it, even if the request thread has moved on.

```java
Executor delegate = new SimpleAsyncTaskExecutor();
Executor executor = new DelegatingSecurityContextExecutor(delegate);

executor.execute(() -> {
	// SecurityContextHolder matches the submitter
});
```

**Listing 2.** One-arg constructor — capture at submit, not at run. Callers need not mention Spring Security if this `Executor` is injected.

Same idea exists for the rest of the concurrency family: **`DelegatingSecurityContextExecutorService`**, **`DelegatingSecurityContextAsyncTaskExecutor`** (for **`@Async`**), **`DelegatingSecurityContextTaskExecutor`**, scheduled variants. How to apply them: [[How do you propagate SecurityContext to async threads]].

```d2
direction: right
caller: "Caller thread\nexecute(runnable)" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
wrapper: "DelegatingSecurityContextExecutor\nwrap + capture context" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
delegate: "Delegate Executor\n(pool / SimpleAsyncTaskExecutor)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
worker: "Worker\nsetContext → run → clearContext" {
  width: 240
  height: 70
  style.fill: "#fce4ec"
}

caller -> wrapper -> delegate -> worker
```

**Fig. 1.** Only the wrap-and-delegate path gets a SecurityContext; the inner pool is unaware of Spring Security.

> [!warning] Unwrapped submissions stay empty
> Wrapping one executor does **not** change **`MODE_THREADLOCAL`** for the JVM. **`Executors.newFixedThreadPool`**, a raw **`@Async`** `TaskExecutor`, or `new Thread(runnable).start()` still see an **empty holder**. **`MODE_INHERITABLETHREADLOCAL`** is a different mechanism ([[What is MODE_INHERITABLETHREADLOCAL in SecurityContextHolder]]) and is not what this class does.

> [!tip] Interview answer
> DelegatingSecurityContextExecutor wraps an Executor and wraps each Runnable in DelegatingSecurityContextRunnable so SecurityContext is set on the worker and cleared in finally. The one-arg constructor copies SecurityContextHolder at submit time; the two-arg form uses a fixed context. Tasks not submitted through it still see an empty ThreadLocal holder.
