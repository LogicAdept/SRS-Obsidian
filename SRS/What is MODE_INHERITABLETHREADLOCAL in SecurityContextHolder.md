<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SecurityContext #SRS

# What is MODE_INHERITABLETHREADLOCAL in SecurityContextHolder?

> [!abstract] Short answer
> **`SecurityContextHolder.MODE_INHERITABLETHREADLOCAL`** is a **JVM-wide** `SecurityContextHolderStrategy`: it stores **`SecurityContext` in an `InheritableThreadLocal`**, so a **child thread created from** a secure thread **starts with the same identity**. Set it **at startup** with **`setStrategyName(...)`** or the **`spring.security.strategy`** system property — **before** any thread uses the holder. It does **not** re-copy per task on a **reused pool worker**. For async work prefer **`DelegatingSecurityContextExecutor`**.

## What the mode changes

**`SecurityContextHolder`** is a static façade over a **`SecurityContextHolderStrategy`**. Default is **`MODE_THREADLOCAL`**: the context stays on **that** thread only ([[Why does SecurityContextHolder use ThreadLocal]]).

**`MODE_INHERITABLETHREADLOCAL`** is for apps that **spawn child threads** and want them to **assume the same security identity**. Java **`InheritableThreadLocal`** copies the parent’s value when the **child `Thread` is constructed**. A Swing-style **`MODE_GLOBAL`** (one context for the whole JVM) is a different mode and is **not for servers**.

Most applications should **keep the default**. The architecture guide presents inheritable mode as an opt-in for that spawn-child pattern, not as the way to drive **`@Async`** or a **`ThreadPoolExecutor`**.

## How you enable it

Two equivalent switches, both **process-wide**:

```java
SecurityContextHolder.setStrategyName(
		SecurityContextHolder.MODE_INHERITABLETHREADLOCAL);
```

**Listing 1.** Static call — must run at startup, before `getContext()` / filters / any other thread uses the holder.

Or set system property **`spring.security.strategy`** to **`MODE_INHERITABLETHREADLOCAL`**. Changing the strategy **after** threads are already running does **not** retrofit them: workers created under **`MODE_THREADLOCAL`** do not start inheriting.

## Why it is the wrong tool for pools

A pool **creates workers once and reuses them**. Inheritance runs at **thread creation**, not at **`execute()`**. So:

1. A worker created at startup may inherit **empty** context and never see the request user.
2. A worker created **while handling user X** keeps **X** on that thread. User **Y**’s later task on the same worker can still see **X**.

Submit-time wrapping copies the **current** holder and **`clearContext()` in `finally`**: [[What is DelegatingSecurityContextExecutor]], [[How do you propagate SecurityContext to async threads]].

```d2
direction: right
parent: "Request thread\nMODE_INHERITABLETHREADLOCAL" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
child: "new Thread(...) child\ninherits at construction" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
pool: "Reused pool worker\nno copy at execute()" {
  width: 240
  height: 70
  style.fill: "#fce4ec"
}

parent -> child
parent -> pool
```

**Fig. 1.** Inheritable mode follows **spawned** children; it does not wrap **`Executor.execute`**.

> [!warning] Set the strategy before the holder is used
> **`setStrategyName` is not a per-request switch.** Call it (or set the system property) **at JVM startup**. Flipping it later leaves existing threads on the old strategy and does not install inheritance on threads already started. On a server, inheritable mode can also leak identity into **unrelated** child threads a library spawns.

> [!tip] Interview answer
> MODE_INHERITABLETHREADLOCAL stores SecurityContext in an InheritableThreadLocal so child threads created from the secure thread start with the same Authentication. Set it at startup (setStrategyName or spring.security.strategy); it is JVM-wide and does not retrofit running threads. Do not use it for thread pools — workers are reused and can leak user X onto user Y. Keep MODE_THREADLOCAL and wrap the executor with DelegatingSecurityContextExecutor.
