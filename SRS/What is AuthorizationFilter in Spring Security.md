<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `AuthorizationFilter` in Spring Security?

> [!abstract] Short answer
> The servlet filter that **enforces URL authorization**. `http.authorizeHttpRequests(...)` installs it. It reads `Authentication` from `SecurityContextHolder` (as a `Supplier`), asks an **`AuthorizationManager`** (usually `RequestMatcherDelegatingAuthorizationManager` over your `requestMatchers` rules), then either **`FilterChain.doFilter`** or throws **`AccessDeniedException`**. It is **last** in the default chain, **after** `ExceptionTranslationFilter`. It replaced **`FilterSecurityInterceptor` + `AccessDecisionManager`** (`authorizeRequests`) starting in **5.5**; Spring Security **6** DSL is `authorizeHttpRequests`.

## Last filter, wrapped by `ExceptionTranslationFilter`

```d2
direction: down
authn: "authentication filters +\nAnonymousAuthenticationFilter" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
etf: "ExceptionTranslationFilter" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
az: "AuthorizationFilter\nAuthorizationManager" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
app: "DispatcherServlet / rest of app" {
  width: 260
  height: 40
  style.fill: "#fce4ec"
}

authn -> etf
etf -> az
az -> app: "granted"
az -> etf: "AccessDeniedException"
```

**Fig. 1.** ETF **around** authorization so anonymous denial becomes login/401, not a raw 403. See [[What is ExceptionTranslationFilter in Spring Security]] and [[What is AnonymousAuthenticationFilter]].

If `Authentication` is **`null`**, `AuthorizationFilter` throws **`AuthenticationCredentialsNotFoundException`**. That is why the anonymous filter exists. First-match rules: no matching `requestMatchers` line **denies**. `permitAll` / `authenticated` / `hasRole` / `denyAll` all run **here**, not in `FilterChainProxy` matching. See [[How do you configure authorizeHttpRequests in Spring Security 6]].

```java
http.authorizeHttpRequests((authorize) -> authorize
        .requestMatchers("/css/**").permitAll()
        .anyRequest().authenticated());
```

**Listing 1.** This DSL **is** the `AuthorizationFilter`. MVC controllers sit **after** it (`DispatcherServlet`), so every endpoint must be permitted or it never runs. The filter runs on **every dispatch** by default (`REQUEST`, `FORWARD`, `ERROR`, `INCLUDE`) — JSP/Thymeleaf `FORWARD` often needs `dispatcherTypeMatchers(FORWARD, ERROR).permitAll()`.

It is last so **authentication, CSRF, headers** do not themselves need a URL rule. Add custom work **before** it (`addFilterBefore` / `addFilterAfter(..., AnonymousAuthenticationFilter.class)`). A filter **after** `AuthorizationFilter` runs only if access was **already granted** — too late to set `Authentication` for this request. If `AuthorizationFilter` is moved **before** login filters, every caller looks anonymous. See [[What is addFilterAfter in Spring Security]].

> [!warning] After this filter is too late for login
> `addFilterAfter(jwt, AuthorizationFilter.class)` authenticates **after** the decision. JWT/Basic/form belong **before** `AnonymousAuthenticationFilter`. Architecture: filters you add **before** `AuthorizationFilter` skip URL authorization; filters **after** it do not.

> [!tip] Interview answer
> AuthorizationFilter is the last default security filter and enforces authorizeHttpRequests through an AuthorizationManager. Deny throws AccessDeniedException for ExceptionTranslationFilter. It replaced FilterSecurityInterceptor. Put authentication before it; MVC sits after it so every URL needs a rule, including forwards.
