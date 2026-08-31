<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SessionManagement #SRS

# What is maxSessionsPreventsLogin?

> [!abstract] Short answer
> **`maxSessionsPreventsLogin`** is the concurrent-session switch for **what happens when `maximumSessions` is already reached**. **`true`**: keep the existing sessions and **fail the new authentication** (`SessionAuthenticationException`). **`false` (default)**: allow the new login and **expire the least-recently used** extra session; `ConcurrentSessionFilter` invalidates it on the next request.

## The flag, not the cap

`maximumSessions(n)` is **how many** authenticated servlet sessions a principal may hold. `maxSessionsPreventsLogin` is **which side loses** when that number is exceeded. You set it on the same `ConcurrencyControlConfigurer` (XML: `error-if-maximum-exceeded`). See [[What is maximumSessions in Spring Security]].

It maps to `ConcurrentSessionControlAuthenticationStrategy.setExceptionIfMaximumExceeded`. Default **`false`**.

| Value | At the extra login | Existing session |
|---|---|---|
| **`false` (default)** | New login **succeeds**. Extra sessions are **marked expired** (least recently used first). | Still works until the next request; then [[What is ConcurrentSessionFilter]] logs it out and can redirect to `expiredUrl`. |
| **`true`** | New login **fails**. Strategy throws **`SessionAuthenticationException`** (`AuthenticationException`). | Unchanged. |

The configurer’s rationale for the default: if someone **forgot to log out** (another browser, another device), they can still get in without an administrator clearing the old session.

```d2
direction: right
cap: "Already at maximumSessions" {
  width: 180
  height: 55
  style.fill: "#fff3e0"
}
flag: "maxSessionsPreventsLogin" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
reject: "true → SessionAuthenticationException\n(old session kept)" {
  width: 230
  height: 70
  style.fill: "#fce4ec"
}
expire: "false → expire LRU\nConcurrentSessionFilter later" {
  width: 230
  height: 70
  style.fill: "#e8f5e9"
}

cap -> flag
flag -> reject
flag -> expire
```

**Fig. 1.** The cap counts sessions; this boolean chooses reject-new versus expire-old.

```java
@Bean
public HttpSessionEventPublisher httpSessionEventPublisher() {
    return new HttpSessionEventPublisher();
}

@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .sessionManagement((session) -> session
            .maximumSessions(1)
            .maxSessionsPreventsLogin(true)
        );
    return http.build();
}
```

**Listing 1.** Second form login is **rejected**; the first session stays authenticated. Same `HttpSessionEventPublisher` requirement as any concurrent-session setup.

## How “rejected” shows up

Official servlet docs:

- **Form login**: the user is sent to the **`authentication-failure-url`**.
- **Non-interactive** mechanisms (for example **remember-me**): **401 Unauthorized**.
- XML can add **`session-authentication-error-url`** if you want an error page instead of that 401. On Spring Security 6’s default chain, `sessionAuthenticationErrorUrl` / `sessionAuthenticationFailureHandler` on the `sessionManagement` DSL **throw** — put the failure handler on the authenticating filter. See [[How do you configure session management in Spring Security]] and [[What is SessionAuthenticationStrategy]].

```xml
<session-management>
    <concurrency-control max-sessions="1" error-if-maximum-exceeded="true" />
</session-management>
```

**Listing 2.** Namespace equivalent of `maxSessionsPreventsLogin(true)`.

> [!warning] `maximumSessions(1)` alone does not prevent the second login
> Dumps that only show `maximumSessions(1)` are describing the **default `false` path**: the new browser wins; the old one dies on the next request. You must set **`maxSessionsPreventsLogin(true)`** to keep the first session. The registry is still **`SessionRegistryImpl` in this JVM** — a second instance does not see the first’s sessions unless you share a `SessionRegistry` (Spring Session). Timed-out sessions never leave that map without **`HttpSessionEventPublisher`**. This flag is meaningless on **`STATELESS`** JWT chains that never create a servlet session.

> [!tip] Interview answer
> maxSessionsPreventsLogin is the overflow policy for maximumSessions. false, the default, lets the new login succeed and expires the least-recently used session, which ConcurrentSessionFilter invalidates later. true throws SessionAuthenticationException so form login hits the failure URL or remember-me gets 401, and the existing session stays.
