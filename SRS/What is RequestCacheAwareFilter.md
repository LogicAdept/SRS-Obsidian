<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `RequestCacheAwareFilter`?

> [!abstract] Short answer
> A **`GenericFilterBean`** (since **3.0**) that **replays** a **saved** `HttpServletRequest` after login. It calls **`RequestCache.getMatchingRequest`**: a wrapper → that is what the rest of the chain sees; **`null`** → no-op. [[What is ExceptionTranslationFilter in Spring Security]] **saves** the request (default **`HttpSessionRequestCache`**) before the login redirect. Default TRACE: **after** Basic, **before** `SecurityContextHolderAwareRequestFilter`. Dump “~1100” is **wrong** (`FilterOrderRegistration` **3300**).

## ETF saves; this filter wraps

```d2
direction: down
deny: "unauthenticated GET/POST /checkout" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
etf: "ExceptionTranslationFilter\nRequestCache.saveRequest" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
login: "form login success\nredirect to saved URL" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
rcaf: "RequestCacheAwareFilter\ngetMatchingRequest wrapper" {
  width: 300
  height: 50
  style.fill: "#fce4ec"
}

deny -> etf
etf -> login
login -> rcaf
```

**Fig. 1.** Architecture: this filter **gets** the saved request; ETF **puts** it there. `http.requestCache` is on with `@EnableWebSecurity`. See [[What is FilterOrderRegistration]] and [[What is HttpSecurity in Spring Security]].

Always send users **home** after login: **`NullRequestCache`** or **`requestCache.disable()`**. Match only when `continue` is present: `HttpSessionRequestCache.setMatchingRequestParameterName("continue")`. Default login page ([[What is DefaultLoginPageGeneratingFilter]] / [[What is UsernamePasswordAuthenticationFilter]]) is the usual round-trip.

```java
http.requestCache((cache) -> cache.disable());
```

**Listing 1.** `HttpSecurity.requestCache`: protected `/protected` → login → back to `/protected`. Disable when you do not want session-stored original URLs (APIs, always-home).

> [!warning] Session cache, not Bearer
> Default cache lives in the **HTTP session**. [[What is BearerTokenAuthenticationFilter]] / `STATELESS` chains usually want **`NullRequestCache`**. Without a save, a **POST** that triggered login is **not** replayed (body/method lost). Saving also stores the **URL** an unauthenticated user asked for — do not cache it if that is sensitive.

> [!tip] Interview answer
> RequestCacheAwareFilter reconstitutes the saved request after the user logs in. ExceptionTranslationFilter saved it when it sent them to login. Default is HttpSessionRequestCache so form-login apps return to /checkout. JWT APIs should disable it. It is not the filter that redirects to the login page.
