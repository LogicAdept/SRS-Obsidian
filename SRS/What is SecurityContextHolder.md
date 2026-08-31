<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SecurityContext #SRS

# What is SecurityContextHolder?

> [!abstract] Short answer
> **`SecurityContextHolder`** is a **static façade** that **associates a `SecurityContext` with the current thread**. All methods delegate to a JVM-wide **`SecurityContextHolderStrategy`**. Default is **`MODE_THREADLOCAL`**. **`getContext()` never returns null**; **`getAuthentication()`** on that context might. Spring Security does not care how the holder was filled — if a context with an **`Authentication`** is there, that is the current user. **`FilterChainProxy`** **`clearContext()`**s after the request.

## Static accessor, not the context itself

`org.springframework.security.core.context.SecurityContextHolder` stores **who is authenticated** for this execution. The value it stores is a **`SecurityContext`** ([[What is SecurityContext in Spring Security]]), which in turn holds **`Authentication`**. Mixing the names: you do not “put an Authentication in the holder”; you put a **context** in the holder (or mutate the context the holder already has).

```java
Authentication auth = SecurityContextHolder.getContext().getAuthentication();
String username = auth.getName();
```

**Listing 1.** Read path — holder → context → `Authentication`. `getContext()` is never `null`; `auth` may be.

Documented write path (avoid mutating a context you did not create):

```java
SecurityContext context = SecurityContextHolder.createEmptyContext();
context.setAuthentication(authentication);
SecurityContextHolder.setContext(context);
```

**Listing 2.** `createEmptyContext()` + `setContext` — `setContext` rejects `null`. Custom filters use this (or `getContext().setAuthentication(...)`) so downstream `@PreAuthorize` / `SecurityContextHolder` reads see the user.

**`clearContext()`** drops the value on **this** thread. **`createEmptyContext()`** asks the strategy for a new empty instance without installing it.

## Strategy is JVM-wide

Modes: **`MODE_THREADLOCAL`** (default — servers), **`MODE_INHERITABLETHREADLOCAL`** ([[What is MODE_INHERITABLETHREADLOCAL in SecurityContextHolder]]), **`MODE_GLOBAL`** (standalone / Swing — **not** for servers). You can also pass a fully qualified **`SecurityContextHolderStrategy`** class with a public no-arg constructor.

Set the mode **before anything uses the class**: system property **`spring.security.strategy`** (`SYSTEM_PROPERTY`) or **`setStrategyName(String)`**. Javadoc: **do not call `setStrategyName` more than once** in a JVM — it re-initializes the strategy and **breaks threads still on the old one**. Why ThreadLocal is the default: [[Why does SecurityContextHolder use ThreadLocal]].

```d2
direction: right
code: "Application / filter\ngetContext / setContext" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
holder: "SecurityContextHolder\n(static façade)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
strategy: "SecurityContextHolderStrategy\nMODE_THREADLOCAL by default" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
ctx: "SecurityContext\non this thread" {
  width: 200
  height: 70
  style.fill: "#fce4ec"
}

code -> holder -> strategy -> ctx
```

**Fig. 1.** Every `getContext()` / `setContext()` / `clearContext()` call hits the process-wide strategy.

> [!warning] Other threads and pooled workers
> **`MODE_THREADLOCAL`** does not follow **`@Async`** or a raw **`Executor`**. Propagate with **`DelegatingSecurityContextRunnable`** / **`DelegatingSecurityContextExecutor`**, not by assuming the holder is global ([[How do you propagate SecurityContext to async threads]]). If **`clearContext()`** is skipped on a pooled thread, the **next** task can still see the **previous** user's `Authentication`. Filters normally clear the servlet thread; **your** workers must clear too.

> [!tip] Interview answer
> SecurityContextHolder is the static, JVM-wide accessor for the current SecurityContext (Authentication lives on that context). Default MODE_THREADLOCAL so the same request thread can call getContext() anywhere. getContext() is never null; Authentication may be. FilterChainProxy clears after the request. Change strategy only at startup. Async threads need DelegatingSecurityContextExecutor, not a global holder.
