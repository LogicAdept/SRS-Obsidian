<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SessionManagement #SRS

# How do you configure session management in Spring Security?

> [!abstract] Short answer
> On the servlet `SecurityFilterChain`, call `http.sessionManagement(Customizer)` and set three knobs: **`SessionCreationPolicy`** (default **`IF_REQUIRED`**), **session-fixation** protection (default **`changeSessionId`** on Servlet 3.1+), and optional **concurrent-session** limits via **`maximumSessions`**. Token APIs typically switch to **`SessionCreationPolicy.STATELESS`**. Concurrent limits also need an **`HttpSessionEventPublisher`** bean so the registry sees create/destroy events.

## Where the DSL wires in

`SessionManagementConfigurer` is how you declare the policy. It can populate a `SessionManagementFilter` and, when you cap how many sessions a user may hold, a `ConcurrentSessionFilter`.

From Spring Security 6 onward, **`SessionManagementFilter` is not on the default chain**. Form login and other authentication mechanisms invoke `SessionAuthenticationStrategy` themselves, so the filter no longer has to read `HttpSession` on every request just to notice a new `Authentication`. Calling `sessionAuthenticationStrategy(...)`, `sessionAuthenticationErrorUrl(...)`, or `sessionAuthenticationFailureHandler(...)` on the DSL **throws** — wire those on the authentication mechanism instead. Session-fixation and `maximumSessions` still work because the configurer installs a composite strategy on the authenticating filters. See [[What is SessionManagementFilter]].

The default strategy is `ChangeSessionIdAuthenticationStrategy` (`HttpServletRequest.changeSessionId()`). If you set a session cap, the configurer wraps a `CompositeSessionAuthenticationStrategy` that delegates to `ConcurrentSessionControlAuthenticationStrategy`, the fixation strategy, and `RegisterSessionAuthenticationStrategy`.

```d2
direction: right
dsl: "sessionManagement(Customizer)" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
policy: "SessionCreationPolicy\nIF_REQUIRED default" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
sas: "SessionAuthenticationStrategy\nchangeSessionId default" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
csc: "maximumSessions\n+ ConcurrentSessionFilter" {
  width: 220
  height: 70
  style.fill: "#fce4ec"
}

dsl -> policy
dsl -> sas
dsl -> csc
```

**Fig. 1.** Servlet session management is one DSL: creation policy, post-login strategy (fixation), optional concurrency.

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .sessionManagement((session) -> session
            .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
            .sessionFixation((fixation) -> fixation.changeSessionId())
            .invalidSessionUrl("/invalidSession")
            .maximumSessions(1)
            .maxSessionsPreventsLogin(true)
        );
    return http.build();
}

@Bean
public HttpSessionEventPublisher httpSessionEventPublisher() {
    return new HttpSessionEventPublisher();
}
```

**Listing 1.** Conceptual Spring Security 6+ chain: keep a session when needed, change the id on login, reject a second concurrent login, redirect when the submitted session id is already invalid. `HttpSessionEventPublisher` is required for the concurrent-session registry to stay accurate.

## SessionCreationPolicy

`SessionCreationPolicy` controls whether Spring Security creates or consults an `HttpSession` for the security context — not whether some other filter in the app can still call `getSession()`.

| Policy | Effect |
|---|---|
| **`IF_REQUIRED`** | Create a session only when Spring Security needs one. Default (`create-session="ifRequired"`). |
| **`ALWAYS`** | Always create a session (`ForceEagerSessionCreationFilter`). |
| **`NEVER`** | Spring Security never creates a session, but **will use** one that already exists. |
| **`STATELESS`** | Never create a session **and never read** `SecurityContext` from one. Switches the repository to `NullSecurityContextRepository` and skips saving the request into the session. Typical for JWT / HTTP Basic APIs. |

See [[What is SessionCreationPolicy in Spring Security]]. `ALWAYS` is how you force eager session creation; `STATELESS` is the usual pairing with `csrf.disable()` on a Bearer-token API — see [[Why do you disable CSRF for a JWT REST API]].

```java
http.sessionManagement((session) -> session
    .sessionCreationPolicy(SessionCreationPolicy.STATELESS));
```

**Listing 2.** `STATELESS` — no `JSESSIONID` for the security context; each request must carry its own credentials.

## Concurrent sessions

By default **any number of sessions** is allowed. `maximumSessions(1)` means a second successful login **expires the least-recently used existing session**; `ConcurrentSessionFilter` invalidates that session on the next request. `maxSessionsPreventsLogin(true)` **rejects the new login instead**: form login is sent to the authentication-failure URL; a non-interactive mechanism such as remember-me gets **401**. The default of `maxSessionsPreventsLogin` is **`false`**. From 6.5 you can pass a `SessionLimit` (for example admins unlimited, others `1`). Details: [[What is maximumSessions in Spring Security]] and [[What is maxSessionsPreventsLogin]].

The configurer’s default registry is in-memory `SessionRegistryImpl`. For a cluster, replace it (Spring Session’s `SpringSessionBackedSessionRegistry`); see [[How does Spring Session with Redis enable horizontal scaling]]. If `UserDetails` is a custom type, override **`equals` and `hashCode`** — the registry keys principals with those methods.

## Session fixation and expired sessions

On login, Spring Security **changes the session id** (or creates a new session) so an attacker who planted an id cannot keep the authenticated session. Configure `sessionFixation()` as `changeSessionId` (default on Servlet 3.1+), `migrateSession`, `newSession`, or `none` (leaves the app open to fixation). See [[How do you handle session fixation in Spring Security]] and [[What is SessionAuthenticationStrategy]].

`invalidSessionUrl` / `invalidSessionStrategy` run when the client presents an **already invalid** session id (timeout is the usual cause). Idle timeout itself is the servlet container’s session timeout, not this DSL. `expiredUrl` is different: it fires when **this** user’s session was expired **because of** the concurrent-session cap.

> [!warning] Concurrent control is more than `maximumSessions(1)`
> Without **`HttpSessionEventPublisher`**, destroyed sessions never leave `SessionRegistryImpl`, so limits drift. The default registry is **per JVM** — a second node does not see the first node’s sessions. Custom `UserDetails` without `equals`/`hashCode` makes the same user look like two principals. `maxSessionsPreventsLogin` defaults to **false** (kick the old session), not “reject the new login”.

> [!warning] `NEVER` is not `STATELESS`, and timeout redirects can lie
> `NEVER` still **uses** an existing session; `RequestCache` saving the original request after login often **creates** an `HttpSession` anyway. `STATELESS` is the policy that also **ignores** the session for `SecurityContext`. `invalidSessionUrl` can fire after a logout-then-login in the same browser if **`JSESSIONID` was not deleted** (`logout.deleteCookies("JSESSIONID")` or `Clear-Site-Data: cookies`).

> [!tip] Interview answer
> Configure it on HttpSecurity.sessionManagement: SessionCreationPolicy (IF_REQUIRED by default, STATELESS for JWT), session-fixation via ChangeSessionIdAuthenticationStrategy, and optional maximumSessions. From Spring Security 6 the SessionManagementFilter is not default — authenticating filters call the strategy themselves. Concurrent limits need HttpSessionEventPublisher; maxSessionsPreventsLogin(true) rejects the new login instead of expiring the old one.
