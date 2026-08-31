<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `ExceptionTranslationFilter` in Spring Security?

> [!abstract] Short answer
> The filter that **translates** `AuthenticationException` and `AccessDeniedException` from **downstream** (including [[What is AuthorizationFilter in Spring Security]] and method security) into HTTP: **`AuthenticationEntryPoint`** (login redirect / `WWW-Authenticate` / 401) or **`AccessDeniedHandler`** (usually **403**). It **does not enforce** rules. Default chain: immediately **before** `AuthorizationFilter`. Spring Security 6’s URI enforcer is `AuthorizationFilter`, not `FilterSecurityInterceptor`.

## Catch, then commence or deny

```d2
direction: down
etf: "ExceptionTranslationFilter\ntry { chain.doFilter }" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
down: "AuthorizationFilter /\nmethod security" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
ep: "AuthenticationEntryPoint\nlogin or 401" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
adh: "AccessDeniedHandler\n403" {
  width: 200
  height: 40
  style.fill: "#fce4ec"
}

etf -> down
down -> ep: "unauthenticated, anonymous,\nor AuthenticationException"
down -> adh: "AccessDeniedException\nand fully authenticated"
```

**Fig. 1.** Architecture pseudocode. Anonymous deny uses the **entry point**, not 403 — [[What is AnonymousAuthenticationFilter]] tokens are not “logged in” for this test. No those two exceptions → ETF is a no-op.

`sendStartAuthentication` **clears** `SecurityContextHolder`, **saves** the request (`HttpSessionRequestCache`; `RequestCacheAwareFilter` replays it after login), then **`AuthenticationEntryPoint.commence`**. Form login → redirect to `/login`; HTTP Basic → `WWW-Authenticate`. Configure via `http.exceptionHandling(...)`. See [[How does Spring Security authenticate an HTTP request end to end]].

```java
http.exceptionHandling((ex) -> ex
        .accessDeniedPage("/errors/access-denied"));
```

**Listing 1.** `HttpSecurity.exceptionHandling` (on with `@EnableWebSecurity`) sets the handler `ExceptionTranslationFilter` uses. Default `AccessDeniedHandlerImpl` sends **403**.

> [!warning] Outer wrapper, not the enforcer
> ETF must sit **before** `AuthorizationFilter` so `doFilter` wraps it. Missing or **after** the enforcer → those exceptions become **500**. Filters **before** ETF (for example [[What is CsrfFilter in Spring Security]]) handle `AccessDeniedException` themselves. `FilterSecurityInterceptor` is the pre-6 URI enforcer.

> [!tip] Interview answer
> ExceptionTranslationFilter does not decide access. It catches AuthenticationException and AccessDeniedException from later filters and method security, then runs the entry point or AccessDeniedHandler. Anonymous users get the login/401 path, not 403. Put it before AuthorizationFilter or you see 500s instead of 401/403.
