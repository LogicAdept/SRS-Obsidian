<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `ConcurrentSessionFilter`?

> [!abstract] Short answer
> The servlet filter for **concurrent session control**. On **every** request it **`SessionRegistry.refreshLastRequest`**, then if that session is **marked expired** it runs **logout handlers** (like `LogoutFilter`) and **`SessionInformationExpiredStrategy`**. `sessionManagement.maximumSessions(...)` installs it **together with** `SessionManagementFilter`’s **`ConcurrentSessionControlAuthenticationStrategy`** (the strategy expires or rejects a login). **`HttpSessionEventPublisher`** is required so destroyed sessions leave the registry. **JWT `STATELESS`** resource-server chains do **not** use this.

## Two jobs: refresh, then expire

```d2
direction: down
login: "login success\nConcurrentSessionControlAuthenticationStrategy" {
  width: 320
  height: 50
  style.fill: "#e3f2fd"
}
csf: "ConcurrentSessionFilter\nrefreshLastRequest" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
ok: "session still valid\ncontinue chain" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
exp: "expired → LogoutHandler +\nSessionInformationExpiredStrategy" {
  width: 300
  height: 50
  style.fill: "#fce4ec"
}

login -> csf: "later requests"
csf -> ok
csf -> exp
```

**Fig. 1.** Namespace: `concurrency-control` creates **`ConcurrentSessionFilter`**, wires the strategy into **`SessionManagementFilter`** (and form-login), and a **`SessionRegistryImpl`** unless you supply `session-registry-ref`. See [[What is FilterChainProxy and DelegatingFilterProxy]].

Default `maximumSessions(1)`: a **second login invalidates the first**. `maxSessionsPreventsLogin(true)` **rejects** the second instead. `expiredUrl("/login?expired")` is the usual `SessionInformationExpiredStrategy`. `maximumSessions` can be a function of `Authentication` (admins unlimited).

```java
@Bean
HttpSessionEventPublisher httpSessionEventPublisher() {
    return new HttpSessionEventPublisher();
}

@Bean
SecurityFilterChain app(HttpSecurity http) throws Exception {
    http.sessionManagement((session) -> session.maximumSessions(1));
    return http.build();
}
```

**Listing 1.** DSL creates the registry and filters. The bean you must not forget is **`HttpSessionEventPublisher`** (or `AbstractSecurityWebApplicationInitializer.enableHttpSessionEventPublisher()`). Without it, expired sessions are **not cleaned up**. See [[What is AbstractSecurityWebApplicationInitializer]].

`STATELESS` JWT (`oauth2ResourceServer`) has **no** `HttpSession` to register. Do not copy `maximumSessions` onto that chain. See [[How do you configure JWT and form login as two SecurityFilterChain beans]] and [[What is BearerTokenAuthenticationFilter]].

> [!warning] Publisher, not a missing SessionRegistry
> `maximumSessions` without **`HttpSessionEventPublisher`** is the incomplete recipe. XML/Java already create **`SessionRegistryImpl`**. A custom `SessionRegistry` is optional (`session-registry-ref`). Constructor `(SessionRegistry, String expiredUrl)` is **deprecated** — use **`SessionInformationExpiredStrategy`**.

> [!tip] Interview answer
> ConcurrentSessionFilter refreshes SessionRegistry last-request time and logs out sessions already marked expired. The max-sessions limit is applied at login by ConcurrentSessionControlAuthenticationStrategy. You need HttpSessionEventPublisher. It is a servlet-session feature, not JWT stateless.
