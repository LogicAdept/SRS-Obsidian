<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SessionManagement #SRS

# What is maximumSessions in Spring Security?

> [!abstract] Short answer
> **`maximumSessions`** is the `sessionManagement` knob that caps how many **authenticated servlet sessions** one principal may hold at once. The DSL default is **unlimited**. `maximumSessions(1)` means a second login **expires the least-recently used existing session** unless you also set `maxSessionsPreventsLogin(true)`. It counts **HTTP sessions** via a `SessionRegistry`, so it does not apply to a **`STATELESS`** token API.

## What the DSL actually installs

Calling `maximumSessions(n)` on `SessionManagementConfigurer` does three things:

1. Builds a `ConcurrentSessionControlAuthenticationStrategy` with that limit (and `RegisterSessionAuthenticationStrategy` to put the new session in the registry).
2. Adds **`ConcurrentSessionFilter`** to the chain.
3. Uses in-memory **`SessionRegistryImpl`** unless you supply another `sessionRegistry`.

On login, the strategy compares **already active sessions for that principal** with the configured maximum. If the cap is exceeded and `maxSessionsPreventsLogin` is **false** (the default), it **expires the least-recently used** extra sessions. Those sessions stay usable until the next request, when `ConcurrentSessionFilter` sees they are marked expired, runs logout handlers (typically **invalidates** the session), and runs `SessionInformationExpiredStrategy` (`expiredUrl` if you set one). See [[What is ConcurrentSessionFilter]] and [[What is SessionAuthenticationStrategy]].

The filter also calls `SessionRegistry.refreshLastRequest` on every request so “least recently used” is accurate.

```d2
direction: right
login: "Successful login" {
  width: 150
  height: 50
  style.fill: "#e3f2fd"
}
csc: "ConcurrentSessionControl\nAuthenticationStrategy" {
  width: 210
  height: 70
  style.fill: "#fff3e0"
}
reg: "SessionRegistry" {
  width: 150
  height: 50
  style.fill: "#e8f5e9"
}
csf: "ConcurrentSessionFilter\n(next request)" {
  width: 190
  height: 70
  style.fill: "#fce4ec"
}

login -> csc: "count vs max"
csc -> reg: "expire LRU extras"
csf -> reg: "refresh + invalidate if expired"
```

**Fig. 1.** The cap is enforced at authentication; `ConcurrentSessionFilter` is what actually kills an expired session on the next hit.

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
        );
    return http.build();
}
```

**Listing 1.** One session per user: the second form login succeeds and the **first** session is expired. `HttpSessionEventPublisher` is required so timeouts and logouts leave the registry.

`HttpSecurity`’s own note: when you use `SessionManagementConfigurer.maximumSessions(int)`, configure **`HttpSessionEventPublisher`** so expired sessions are cleaned up. Without it, `SessionRegistryImpl` never hears `SessionDestroyedEvent`s and the count **drifts upward**.

## Defaults, `-1`, and per-user limits

| Setting | Meaning |
|---|---|
| **Do not call `maximumSessions`** | Configurer default: **any number** of sessions. |
| **`maximumSessions(1)`** | At most one; extra sessions expired (LRU) unless prevent-login is on. |
| **`-1`** | Unlimited for that principal (`getMaximumSessionsForThisUser` documents **-1 = unlimited**, a **positive** integer to limit, **never zero**). |
| **`maximumSessions(SessionLimit)`** (6.5+) | Limit as a function of `Authentication` — e.g. admins `-1`, everyone else `1`. |

```java
AuthorizationManager<?> isAdmin = AuthorityAuthorizationManager.hasRole("ADMIN");
http.sessionManagement((session) -> session
    .maximumSessions((authentication) ->
        isAdmin.authorize(() -> authentication, null).isGranted() ? -1 : 1));
```

**Listing 2.** Official pattern: administrators unlimited, others one session. This is still cookie-session concurrency, not JWT.

If you **construct `ConcurrentSessionControlAuthenticationStrategy` yourself**, that class’s `setMaximumSessions(int)` default is **`1`**, not unlimited. The unlimited default is a **configurer** behaviour, not the strategy bean’s.

When the cap should **reject the new login** instead of expiring the old one, use [[What is maxSessionsPreventsLogin]]. That is a separate flag; `maximumSessions` only sets the number. Full wiring: [[How do you configure session management in Spring Security]].

## What it cannot count

`SessionRegistryImpl` is a **per-JVM map** keyed by principal. A second app instance does not see the first’s sessions — use a clustered registry (Spring Session’s `SpringSessionBackedSessionRegistry`) if the cap must hold across nodes; see [[How does Spring Session with Redis enable horizontal scaling]]. Custom `UserDetails` must override **`equals` and `hashCode`** or two logins of the same user look like two principals.

> [!warning] `maximumSessions(1)` is not “block the second login”
> The default is **expire the old session**, not fail the new one. Form login on a second browser **succeeds**; the first browser is unauthenticated on the next request. `maxSessionsPreventsLogin(true)` is the reject-new-login switch. `STATELESS` / Bearer JWT has **no servlet session to register**, so this cap does nothing useful — it is cookie-session concurrency. Also wire **`HttpSessionEventPublisher`**; dumps that only set `maximumSessions(1)` leave a leaking in-memory registry.

> [!tip] Interview answer
> maximumSessions on sessionManagement caps how many HttpSessions one user may have; the DSL default is unlimited. With maximumSessions(1) the second login expires the least-recently used session unless maxSessionsPreventsLogin is true. ConcurrentSessionFilter enforces the expiry on the next request, and you need HttpSessionEventPublisher plus a registry that actually sees all nodes.
