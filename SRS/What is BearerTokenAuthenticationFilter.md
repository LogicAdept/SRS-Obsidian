<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #Security/JWT #Java/Spring/Security/OAuth2 #SRS

# What is `BearerTokenAuthenticationFilter`?

> [!abstract] Short answer
> The OAuth2 **resource-server** filter (`OncePerRequestFilter`) that reads a **Bearer** token (default **`Authorization: Bearer …`**), converts it to a **`BearerTokenAuthenticationToken`**, and calls **`AuthenticationManager`** (`JwtAuthenticationProvider` or opaque introspection). Success sets `SecurityContext` (typically **request-attribute**, not session) and **`filterChain.doFilter`**. **`http.oauth2ResourceServer((o) -> o.jwt(Customizer.withDefaults()))`** installs it. It is **not** a subclass of `AbstractAuthenticationProcessingFilter`.

## Every request with a token — or skip

```d2
direction: down
hdr: "AuthenticationConverter\nBearer token?" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
am: "AuthenticationManager\nJwtAuthenticationProvider" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
ctx: "SecurityContextHolder\nthen FilterChain.doFilter" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
skip: "no token → continue\nAnonymousAuthenticationFilter" {
  width: 280
  height: 50
  style.fill: "#fce4ec"
}

hdr -> am: "token"
hdr -> skip: "null"
am -> ctx: "JwtAuthenticationToken"
```

**Fig. 1.** Missing header is **not** 401 from this filter — it continues; `AuthorizationFilter` then sees **anonymous**. Invalid token → `BearerTokenAuthenticationEntryPoint` (`WWW-Authenticate: Bearer …`). See [[What is AnonymousAuthenticationFilter]] and [[What is AuthorizationFilter in Spring Security]].

Default resolver: **`Authorization`** header. Customize with `BearerTokenResolver` / `BearerTokenAuthenticationConverter` (header name, form body). DSL: **`oauth2ResourceServer`**. Order table places it **before** `BasicAuthenticationFilter`, still **before** `ExceptionTranslationFilter` and `AuthorizationFilter`.

```java
http.authorizeHttpRequests((a) -> a.anyRequest().authenticated())
    .oauth2ResourceServer((oauth2) -> oauth2.jwt(Customizer.withDefaults()));
```

**Listing 1.** Prefer the DSL over a home-grown `OncePerRequestFilter`. A second `@Order(1)` chain needs **`securityMatcher("/api/**")`** or form-login’s catch-all **matches first** and this filter **never runs** — Bearer header, still anonymous. See [[How do you configure JWT and form login as two SecurityFilterChain beans]] and [[What happens if no SecurityFilterChain matches a request]].

Provider: JWT → `JwtDecoder` + `JwtAuthenticationConverter` → **`JwtAuthenticationToken`** (principal `Jwt`, at least `FACTOR_BEARER`). Opaque → introspection. Do not extend `AbstractAuthenticationProcessingFilter` for this — that is form POST `/login`. See [[What is AbstractAuthenticationProcessingFilter]] and [[What is BasicAuthenticationFilter]].

> [!warning] No token means skip, not challenge
> The filter **`doFilter`s** when conversion returns `null`. 401 comes later from **`AuthorizationFilter` + ETF**, or immediately if the token is **present and invalid**. A custom JWT filter after `AuthorizationFilter` is too late.

> [!tip] Interview answer
> BearerTokenAuthenticationFilter is the resource-server OncePerRequestFilter: convert the Bearer token, AuthenticationManager, set SecurityContext, continue the chain. oauth2ResourceServer.jwt() adds it. If the chain matcher misses the URL you get anonymous despite the header. It is not form login’s abstract processing filter.
