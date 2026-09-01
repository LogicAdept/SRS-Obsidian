<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS

# What are the core components of Spring Security?

> [!abstract] Short answer
> Servlet Security is a **`FilterChainProxy`** that picks a **`SecurityFilterChain`**. **Authentication** fills a **`SecurityContext`** on **`SecurityContextHolder`** (usually via **`AuthenticationManager` / `ProviderManager` / `AuthenticationProvider`**). **Authorization** is **`AuthorizationManager`** (web: **`AuthorizationFilter`**; methods: interceptors). **`GrantedAuthority`** values on **`Authentication`** are what those managers read. **`AccessDecisionManager` is legacy.**

## Architecture types, not a shopping list

The authentication architecture page names the pieces explicitly:

| Component | Role |
| --- | --- |
| **`SecurityContextHolder`** | Where the current principal lives (default **`ThreadLocal`**). **`FilterChainProxy`** clears it after the request. |
| **`SecurityContext`** | Holds the **`Authentication`**. |
| **`Authentication`** | Unauthenticated **input** to the manager (`isAuthenticated() == false`) **or** the current user after success. **`principal`**, **`credentials`**, **`authorities`**. |
| **`GrantedAuthority`** | High-level permission (roles, scopes). From **`Authentication.getAuthorities()`**. Not a per-row ACL. |
| **`AuthenticationManager`** | How filters authenticate. Return value is stored on the holder. |
| **`ProviderManager`** | Usual manager: a list of **`AuthenticationProvider`**s (DAO vs JWT vs SAML, …). |
| **`AuthenticationEntryPoint`** | Ask the client for credentials (login redirect, **`WWW-Authenticate`**). |
| **`AbstractAuthenticationProcessingFilter`** | Base filter: build a token → manager → success/failure handlers. |

Authorization is a **second** phase, **after** authentication filters. **`AuthorizationManager` supersedes `AccessDecisionManager` and `AccessDecisionVoter`**. **`AuthorizationFilter`** (from **`authorizeHttpRequests`**) calls it for HTTP; method security uses interceptors with the same interface.

```java
SecurityContext context = SecurityContextHolder.getContext();
Authentication authentication = context.getAuthentication();
String name = authentication.getName();
Collection<? extends GrantedAuthority> authorities = authentication.getAuthorities();
```

**Listing 1.** Once authentication succeeded, authorization reads **this** object — not a second user store.

```d2
direction: down
req: "HttpServletRequest" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
proxy: "FilterChainProxy\nSecurityFilterChain" {
  width: 220
  height: 48
  style.fill: "#fff3e0"
}
am: "AuthenticationManager\nProviderManager" {
  width: 220
  height: 48
  style.fill: "#fff3e0"
}
ctx: "SecurityContextHolder" {
  width: 200
  height: 40
  style.fill: "#c8e6c9"
}
az: "AuthorizationManager\nAuthorizationFilter" {
  width: 230
  height: 48
  style.fill: "#c8e6c9"
}

req -> proxy
proxy -> am
am -> ctx
ctx -> az
```

**Fig. 1.** Authenticate, stash, then authorize. Exploit filters (CSRF, headers) sit on the **same** chain, earlier or around these steps ([[What is SecurityContextHolder]], [[What is AuthenticationManager and AuthenticationProvider in Spring Security]], [[What is GrantedAuthority in Spring Security]], [[What is SecurityFilterChain]], [[What is AuthorizationManager in method security]]).

Servlet wiring: container **`DelegatingFilterProxy`** → Spring bean **`FilterChainProxy`** (`springSecurityFilterChain`) → first matching **`SecurityFilterChain`**. Authentication filters run **before** **`AuthorizationFilter`**. That order is **`FilterOrderRegistration`**, not this type list.

> [!warning] `AccessDecisionManager` is the old dump
> Security 5.6+ web and method authorization use **`AuthorizationManager`**. A custom **`AccessDecisionManager`** is a migration answer, not the current core type ([[How do you implement a custom AccessDecisionManager]]).

> [!warning] This list is not filter order
> Naming **`AuthenticationManager`** does not tell you whether **`UsernamePasswordAuthenticationFilter`** sits before **`AuthorizationFilter`**. Debug **`FilterChainProxy`** / the DEBUG chain listing. **`GrantedAuthority`** is also not object-level ACL — that is **`PermissionEvaluator` / `hasPermission`**.

> [!tip] Interview answer
> Core Servlet pieces are FilterChainProxy plus SecurityFilterChain, SecurityContextHolder holding Authentication, AuthenticationManager (usually ProviderManager) to authenticate, and AuthorizationManager to authorize. GrantedAuthority values on the Authentication are the permissions. AccessDecisionManager is superseded. Authentication is who; authorization is whether that Authentication may do this request or method.
