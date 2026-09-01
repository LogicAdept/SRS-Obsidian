<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/WebFlux #Java/Spring/Framework/WebFlux #SRS

# What is `pathMatchers` in WebFlux security?

> [!abstract] Short answer
> **`pathMatchers`** selects **which exchanges** an **`authorizeExchange` rule** applies to. It builds **`PathPatternParserServerWebExchangeMatcher`s** (Spring **`PathPattern`**, path within the app). That is WebFlux’s stand-in for servlet **`requestMatchers`**, not a call on `HttpSecurity`. **`anyExchange()`** is the catch-all. **First matching rule wins.**

## Patterns on `AuthorizeExchangeSpec`

Inherited from **`AbstractServerWebExchangeMatcherRegistry`**:

| Overload | Meaning |
| --- | --- |
| **`pathMatchers(String... patterns)`** | Path only; any HTTP method |
| **`pathMatchers(HttpMethod, String... patterns)`** | Path **and** method (`POST` + `/users`) |
| **`pathMatchers(HttpMethod)`** | That method, any path |
| **`matchers(ServerWebExchangeMatcher…)`** | Custom matcher |

Javadoc still names the strings **`antPatterns`**, but the matchers are **`PathPatternParserServerWebExchangeMatcher`**: match if the **`PathPattern`** matches **the path within the application**. Syntax looks familiar (`/admin/**`, `{username}`), but it is **not** servlet **`AntPathRequestMatcher`**.

```java
http.authorizeExchange(ex -> ex
        .pathMatchers("/resources/**", "/signup", "/about").permitAll()
        .pathMatchers("/admin/**").hasRole("ADMIN")
        .pathMatchers(HttpMethod.POST, "/users").hasAuthority("USER_POST")
        .pathMatchers("/users/{username}").access((authentication, context) ->
                authentication.map(Authentication::getName)
                        .map(name -> name.equals(context.getVariables().get("username")))
                        .map(AuthorizationDecision::new))
        .anyExchange().authenticated());
```

**Listing 1.** Conceptual mix of Spring Security authorize + `ServerHttpSecurity` javadoc samples. `{username}` is available on the match **context**. Parent DSL: [[What is authorizeExchange in WebFlux security]], [[What is ServerHttpSecurity]].

**`anyExchange()`** — every exchange **not yet matched**. Put it **last**.

**`securityMatcher`** on `ServerHttpSecurity` chooses **which `SecurityWebFilterChain`** runs. **`pathMatchers`** only authorize **inside** that chain — [[What is SecurityWebFilterChain]].

```d2
direction: down
url: "GET /admin/users" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
pm: "pathMatchers in order" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
hit: "first PathPattern hit\n→ permit / hasRole / …" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

url -> pm -> hit
```

**Fig. 1.** A first `pathMatchers("/**")` or `anyExchange()` makes later lines **dead**.

> [!warning] Not servlet `requestMatchers`
> WebFlux: **`pathMatchers` on `authorizeExchange`**. MVC: **`requestMatchers` on `authorizeHttpRequests`**. Mixing the names in a WebFlux config does not compile.

> [!warning] `/**` first shadows everything
> Rules are **declaration order**. Specific `/admin/**` must come **before** a greedy pattern or `anyExchange()`.

> [!warning] `securityMatcher("/api/**")` ≠ `pathMatchers("/api/**")`
> The first limits the **chain**. The second is an **authorization** line. You often want both: matcher on the bean, then `pathMatchers` for public vs authenticated API routes.

> [!tip] Interview answer
> **`pathMatchers` is reactive `requestMatchers`: PathPattern on the application path, then `permitAll` / `hasRole`.** Optional `HttpMethod`. **`anyExchange()` last.** First match wins. Do not confuse it with `securityMatcher` on the chain.
