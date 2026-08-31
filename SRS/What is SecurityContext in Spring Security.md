<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SecurityContext #SRS

# What is SecurityContext in Spring Security?

> [!abstract] Short answer
> **`SecurityContext`** is the object that holds the **`Authentication`** for the **current thread of execution** — principal, credentials, authorities, and authenticated-or-not live **on that `Authentication`**, not as extra fields on the context. You **do not look it up from the request**. You get it from **`SecurityContextHolder.getContext()`**, then **`getAuthentication()`**. **`SecurityContextHolder`** is the accessor (default **`ThreadLocal`**); **`SecurityContext`** is the value it stores.

## Minimum security information for this thread

`org.springframework.security.core.context.SecurityContext` is a **`Serializable`** interface. Javadoc: **minimum security information associated with the current thread**. Default implementation is **`SecurityContextImpl`**.

The interface is only two methods:

| Method | Role |
|--------|------|
| **`getAuthentication()`** | Current **`Authentication`**, or **`null`** if none is stored |
| **`setAuthentication(Authentication)`** | Replace it, or pass **`null`** to clear authentication information |

Username, credentials, authorities, and `isAuthenticated()` are **`Authentication`** members. Spring Security’s model is: **`SecurityContextHolder` → `SecurityContext` → `Authentication`**. The framework does not care how the holder was populated; if a context with an `Authentication` is there, that is the current user.

```java
SecurityContext context = SecurityContextHolder.getContext();
Authentication auth = context.getAuthentication();
```

**Listing 1.** Read path — holder is the accessor; context is the store; `Authentication` is the principal.

An **empty** context (`getAuthentication() == null`) is not the same as **anonymous**: **`AnonymousAuthenticationFilter`** still installs an **`AnonymousAuthenticationToken`**. **`null`** means nothing was stored yet.

## Holder vs context

**`SecurityContextHolder`** is a static façade over a **`SecurityContextHolderStrategy`**. It **creates, stores, and clears** `SecurityContext` instances. **`SecurityContext`** is the object you **get and mutate**. Mixing the names is the usual interview slip: you never “set the holder to an Authentication”; you **`getContext().setAuthentication(...)`** (or use a repository/filter that does).

Default strategy is **`MODE_THREADLOCAL`**, so the context is **per thread**. Servlet filters load it for the request thread and **`FilterChainProxy`** clears it afterward ([[Why does SecurityContextHolder use ThreadLocal]]). Another thread does **not** see it unless you propagate ([[How do you propagate SecurityContext to async threads]], [[What is DelegatingSecurityContextExecutor]]).

```d2
direction: right
holder: "SecurityContextHolder\n(strategy / ThreadLocal)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
ctx: "SecurityContext\n(SecurityContextImpl)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
auth: "Authentication\nprincipal + authorities" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}

holder -> ctx -> auth
```

**Fig. 1.** Holder stores a context; the context’s only payload is `Authentication`.

> [!warning] `getAuthentication()` may be null — or anonymous
> **`null`** means no token in the context. **`anonymousUser` / `ROLE_ANONYMOUS`** is still an **`Authentication`**. Casting `getPrincipal()` without checking type or using **`@AuthenticationPrincipal`** on the wrong type fails either way. Do not treat “we have a SecurityContext” as “the user logged in.”

> [!tip] Interview answer
> SecurityContext is the per-thread object that holds Authentication (principal, credentials, authorities). You obtain it from SecurityContextHolder.getContext(), then getAuthentication(). The holder is the accessor (ThreadLocal by default); the context is what it stores. Empty Authentication is null; anonymous is a real token, not an empty context.
