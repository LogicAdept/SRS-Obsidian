<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS

# What is `authorizeExchange` in WebFlux security?

> [!abstract] Short answer
> **`authorizeExchange`** is the WebFlux **authorization DSL** on **`ServerHttpSecurity`** — servlet **`authorizeHttpRequests`**. You declare **`pathMatchers` / `matchers` / `anyExchange`**, then **`permitAll` / `authenticated` / `hasRole` / `denyAll` / `access(...)`**. **First matching rule wins.** Default if you configure nothing extra: **every exchange must be authenticated**.

## Rules on `AuthorizeExchangeSpec`

`ServerHttpSecurity.authorizeExchange(Customizer<AuthorizeExchangeSpec>)` (since **5.0**). Spring Security *Authorize ServerHttpRequest*: by default authorization **requires an authenticated user**. Explicit form:

```java
@Bean
SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
    http.authorizeExchange(ex -> ex.anyExchange().authenticated())
            .httpBasic(withDefaults())
            .formLogin(withDefaults());
    return http.build();
}
```

**Listing 1.** Conceptual default-equivalent from the reference.

More rules, **in declaration order**:

```java
http.authorizeExchange(ex -> ex
        .pathMatchers("/resources/**", "/signup", "/about").permitAll()
        .pathMatchers("/admin/**").hasRole("ADMIN")
        .pathMatchers("/db/**").access((authentication, context) ->
                hasRole("ADMIN").check(authentication, context)
                        .filter(d -> !d.isGranted())
                        .switchIfEmpty(hasRole("DBA").check(authentication, context)))
        .anyExchange().denyAll());
```

**Listing 2.** Conceptual multi-rule sample. `hasRole("ADMIN")` means authority **`ROLE_ADMIN`** (do not prefix `ROLE_` yourself). Custom logic: **`ReactiveAuthorizationManager` via `access`**. Catch-all **`anyExchange().denyAll()`** so unmatched URLs are not accidentally open.

Javadoc also shows **`pathMatchers(HttpMethod.POST, "/users")`**, **`matchers(customMatcher)`**, and **`access`** that reads URI variables from the exchange.

| Servlet | WebFlux |
| --- | --- |
| `authorizeHttpRequests` | **`authorizeExchange`** |
| `requestMatchers` / `anyRequest` | **`pathMatchers` / `anyExchange`** |

DSL object: [[What is ServerHttpSecurity]]. URL patterns: [[What is pathMatchers in WebFlux security]]. Chain type: [[What is SecurityWebFilterChain]]. **`securityMatcher`** on the HTTP object picks **which chain**; **`pathMatchers`** authorize **inside** it.

`oauth2Login` / `oauth2ResourceServer` are **sibling** methods on `ServerHttpSecurity` (how you **authenticate**), not extra `authorizeExchange` clauses. You still write `authorizeExchange` for **who may call** `/api/**`.

```d2
direction: down
ex: "ServerWebExchange" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
rules: "authorizeExchange rules\nfirst match wins" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
dec: "permit / authenticated /\nhasRole / denyAll / access" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

ex -> rules -> dec
```

**Fig. 1.** Later `pathMatchers` never run if an earlier pattern already matched.

> [!warning] `authorizeRequests()` is the wrong API
> That is servlet (`HttpSecurity`). On WebFlux there is **`authorizeExchange`**.

> [!warning] Put `anyExchange()` last
> It matches **everything left**. A leading `anyExchange().authenticated()` makes later `pathMatchers` **dead**. A leading `pathMatchers("/**")` does the same.

> [!warning] `hasRole` vs `hasAuthority`
> `hasRole("ADMIN")` → **`ROLE_ADMIN`**. `hasAuthority("USER_POST")` uses the string **as-is**.

> [!tip] Interview answer
> **`authorizeExchange` is reactive `authorizeHttpRequests`:** `pathMatchers` then `permitAll` / `hasRole` / `authenticated`, **`anyExchange()` last**. Rules are first-match. OAuth2 login/resource-server config is separate DSL on the same `ServerHttpSecurity`.
