<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `FilterSecurityInterceptor`?

> [!abstract] Short answer
> The **legacy** last-ish servlet filter that **authorized HTTP URIs**. It is a concrete **`AbstractSecurityInterceptor`**: `FilterInvocation` + `FilterInvocationSecurityMetadataSource` + **`AccessDecisionManager`** (voters). **Deprecated** — use [[What is AuthorizationFilter in Spring Security]] (`http.authorizeHttpRequests`, `AuthorizationManager`) instead. It **throws** `AuthenticationException` / `AccessDeniedException`; [[What is ExceptionTranslationFilter in Spring Security]] **above** it turns those into 401/403 or login. Spring Security **6** default chains list `AuthorizationFilter`, not this class.

## Old URI enforcer, wrapped by ETF

```d2
direction: down
etf: "ExceptionTranslationFilter" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
fsi: "FilterSecurityInterceptor\nAccessDecisionManager" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
az: "AuthorizationFilter\n(SS 5.5+ / SS6 default)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}

etf -> fsi: "authorizeRequests / XML false"
etf -> az: "authorizeHttpRequests"
```

**Fig. 1.** `FilterOrderRegistration` still reserves a slot for FSI **then** `AuthorizationFilter`. Architecture’s default TRACE is ETF → **`AuthorizationFilter`**. See [[How do you configure authorizeHttpRequests in Spring Security 6]] and [[What is FilterOrderRegistration]].

Workflow (parent javadoc): read `Authentication` from `SecurityContextHolder` → look up `ConfigAttribute`s → **`AccessDecisionManager.decide`** (XML default `AffirmativeBased` + `RoleVoter` + `AuthenticatedVoter`) → proceed `FilterChain` or throw. Secure object type is **`FilterInvocation`**. `observeOncePerRequest` defaults **`true`** (skips extra JSP `FORWARD`s unless you turn it off). `AuthorizationFilter` instead runs **all dispatcher types** by default.

```java
http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated());
// SS6: AuthorizationFilter — not FilterSecurityInterceptor

// legacy (removed from SS6 DSL): http.authorizeRequests((a) -> a.anyRequest().authenticated());
```

**Listing 1.** Migration docs: `authorizeHttpRequests` → `AuthorizationFilter`; `authorizeRequests` → FSI. XML: `use-authorization-manager` defaults **`true`** (AuthorizationManager / not `SecurityMetadataSource`). `<http>` historically always created FSI + ETF.

> [!warning] Deprecated, and ETF must wrap it
> Do not add a new FSI in SS6. Missing or **after**-enforcer ETF → those throws become **500**, not 401/403. `web.ignoring()` skips **both** this filter and `AuthorizationFilter`. FSI **once-per-request** is **not** the SS6 dispatcher-type behavior.

> [!tip] Interview answer
> FilterSecurityInterceptor was the old URI authorization filter, a FilterInvocation AbstractSecurityInterceptor with AccessDecisionManager and voters. Spring Security 6 uses AuthorizationFilter and AuthorizationManager via authorizeHttpRequests. ExceptionTranslationFilter still has to sit in front so denials become 401 or 403 instead of 500.
