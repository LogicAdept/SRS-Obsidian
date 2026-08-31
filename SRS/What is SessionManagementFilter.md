<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `SessionManagementFilter`?

> [!abstract] Short answer
> A **`GenericFilterBean`** (since **2.0**) that, **after** the rest of the chain, notices **“just authenticated this request”** (repository empty, holder has a **non-anonymous** `Authentication` — typically remember-me / pre-auth) and runs **`SessionAuthenticationStrategy`** (session-fixation, concurrent logins). If the user is **not** authenticated and the session id is **invalid** (timeout), it runs **`InvalidSessionStrategy`** (often redirect). Spring Security **6 does not add this filter by default**; login filters invoke the strategy **themselves** so the session is not read on every request.

## Detect new auth; optional invalid-session

```d2
direction: down
cmp: "repo vs SecurityContextHolder" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
sas: "SessionAuthenticationStrategy\nfixation / max sessions" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
inv: "InvalidSessionStrategy\nredirect" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}

cmp -> sas: "new non-anonymous Authentication"
cmp -> inv: "no auth + invalid session id"
```

**Fig. 1.** Form-login **redirects** on the authenticating request, so this filter **does not run** then — footnote in the session-management chapter. [[What is RememberMeAuthenticationFilter]] **is** the typical “detected here” path. See [[What is ConcurrentSessionFilter]], [[What is SecurityContextHolderFilter]], and [[What is AnonymousAuthenticationFilter]] (anonymous is ignored).

`FilterOrderRegistration` still lists it **before** `ExceptionTranslationFilter`. SS6: `sessionAuthenticationStrategy` / `sessionAuthenticationFailureHandler` / `sessionAuthenticationErrorUrl` on the **`sessionManagement` DSL throw** — wire the strategy on the **authentication mechanism**. `maximumSessions` still goes through `sessionManagement.sessionConcurrency`. See [[What is FilterOrderRegistration]].

```java
http.sessionManagement((session) -> session
        .sessionConcurrency((c) -> c.maximumSessions(1).expiredUrl("/login?expired")));
```

**Listing 1.** `HttpSecurity.sessionManagement` concurrency example. JWT APIs: `SessionCreationPolicy.STATELESS` (null context repo) plus usually `csrf.disable()` — [[How do you configure JWT and form login as two SecurityFilterChain beans]]. TRACE in SS6 typically **has no** `SessionManagementFilter`.

> [!warning] Not in the SS6 default TRACE
> You will not see this filter after `http.build()` unless you opt back into the SS5 model. Invalid-session URL / some DSL methods **need** this filter and **do nothing** (or throw) on a default SS6 chain. STATELESS is a **repository** choice, not “SMF still sitting there until you disable it.”

> [!tip] Interview answer
> SessionManagementFilter used to compare the session repository to the ThreadLocal and, on a new remember-me style login, run SessionAuthenticationStrategy for fixation and concurrent sessions. It also handled invalid session ids. Spring Security 6 dropped it from the default chain so HttpSession is not read every request; form login and Bearer call the strategy themselves.
