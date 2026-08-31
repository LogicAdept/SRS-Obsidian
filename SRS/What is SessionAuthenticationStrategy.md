<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SessionManagement #SRS

# What is SessionAuthenticationStrategy?

> [!abstract] Short answer
> **`SessionAuthenticationStrategy`** is the hook Spring Security runs **when a user has just authenticated**, for **`HttpSession` work**: change the session id (fixation), cap concurrent sessions, or register the session. One method: `onAuthentication(...)`. It may throw **`SessionAuthenticationException`** (typically “too many sessions”). It does **not** handle idle timeouts — that is `InvalidSessionStrategy` on `SessionManagementFilter`.

## When it runs

`AbstractAuthenticationProcessingFilter` (form login, OAuth2 login, and the other browser login filters) calls the strategy **immediately after a successful `attemptAuthentication()`**, then `successfulAuthentication`. If you never set a strategy, the filter uses a **null** implementation (no session work). `RememberMeAuthenticationFilter` can take one too (since 6.4).

From Spring Security 6, that **explicit call on the authenticating filter** is the default. `SessionManagementFilter` is **not** on the chain, so it is no longer the thing that “notices” a new `Authentication` and runs the strategy. Historically the filter **anyway missed form login**, because the authenticating request ends in a redirect and the filter never sees that request. See [[What is SessionManagementFilter]] and [[How do you configure session management in Spring Security]].

Calling `http.sessionManagement(sm -> sm.sessionAuthenticationStrategy(...))` on that default chain **throws**. Set the strategy on the login filter, or use `sessionFixation` / `maximumSessions` / `addSessionAuthenticationStrategy`, which the configurer still wires onto the authenticating mechanisms.

```d2
direction: right
auth: "attemptAuthentication\nsucceeds" {
  width: 170
  height: 60
  style.fill: "#e3f2fd"
}
sas: "SessionAuthenticationStrategy\n.onAuthentication" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
ok: "successfulAuthentication" {
  width: 180
  height: 50
  style.fill: "#e8f5e9"
}
fail: "SessionAuthenticationException\n(e.g. max sessions)" {
  width: 210
  height: 70
  style.fill: "#fce4ec"
}

auth -> sas
sas -> ok: "ok"
sas -> fail: "throw"
```

**Fig. 1.** Session work is a **post-login** callback, not a per-request timeout filter.

```java
public interface SessionAuthenticationStrategy {
    void onAuthentication(Authentication authentication,
            HttpServletRequest request, HttpServletResponse response)
            throws SessionAuthenticationException;
}
```

**Listing 1.** The whole contract. Typical uses in the JavaDoc: ensure a session exists, or change the session id against fixation.

## What the configurer actually installs

`SessionManagementConfigurer` default is **`ChangeSessionIdAuthenticationStrategy`**. A custom `sessionAuthenticationStrategy(...)` **replaces** that fixation default.

If you set [[What is maximumSessions in Spring Security]], it builds a **`CompositeSessionAuthenticationStrategy`** that calls delegates **in order**, and **stops** on `SessionAuthenticationException`:

1. **`ConcurrentSessionControlAuthenticationStrategy`** — may reject the login (`maxSessionsPreventsLogin`) or expire extras. Put this **first** so a rejected login does not create a new `HttpSession`.
2. **Fixation** (`ChangeSessionIdAuthenticationStrategy` or `SessionFixationProtectionStrategy`) — **after** the cap, so a rejected login does not rotate the id for nothing.
3. **`RegisterSessionAuthenticationStrategy`** — **after** fixation so the registry stores the **new** session id.

See [[How do you handle session fixation in Spring Security]], [[What is SessionFixationProtectionStrategy]], and [[What is maxSessionsPreventsLogin]]. `none()` turns protection off. `addSessionAuthenticationStrategy` appends another delegate to that composite. If the login filter has no strategy, it uses a **null** implementation (no session work).

| Implementation | Role |
|---|---|
| **`ChangeSessionIdAuthenticationStrategy`** | Default fixation: `changeSessionId()`, keep attributes. |
| **`SessionFixationProtectionStrategy`** | Invalidate and create; migrate or drop application attributes. |
| **`ConcurrentSessionControlAuthenticationStrategy`** | Enforce `maximumSessions`. |
| **`RegisterSessionAuthenticationStrategy`** | Put the session in `SessionRegistry` (needs `HttpSessionEventPublisher`). |
| **`CompositeSessionAuthenticationStrategy`** | Run several, short-circuit on exception. |
| **`NullAuthenticatedSessionStrategy`** | No-op `onAuthentication` — the “do nothing” strategy. |

> [!warning] This is not timeouts, and `migrateSession` is not the default
> Dumps lump **timeouts**, concurrency, and fixation into “SessionManagementFilter + SessionAuthenticationStrategy”. Idle/invalid session ids are **`InvalidSessionStrategy`** (`invalidSessionUrl`). Concurrent caps and fixation **are** this interface. The fixation default on Servlet 3.1+ is **`changeSessionId`**, not `newSession` or `migrateSession`. A custom strategy **wipes** the default fixation strategy. `migrateSession` in a cluster does **not** officially mean “users see each other’s data”; the documented migrate pitfall is **`HttpSessionBindingListener` / session-scoped beans** unbind-and-rebind.

> [!tip] Interview answer
> SessionAuthenticationStrategy is the callback after a successful login for HttpSession work — mainly changing the session id and enforcing maximumSessions. AbstractAuthenticationProcessingFilter calls onAuthentication right after attemptAuthentication; from Security 6 that is the default path, not SessionManagementFilter. The configurer default is ChangeSessionIdAuthenticationStrategy; with a session cap it becomes a composite of concurrent-control, then fixation, then register.
