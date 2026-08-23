<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# How does the Spring Security filter chain work?

> [!abstract] Short answer
> Spring Security sits in the **Servlet `Filter` layer** (before `DispatcherServlet`). The container calls **`DelegatingFilterProxy`**, which forwards to the **`springSecurityFilterChain`** bean — a **`FilterChainProxy`**. That proxy picks the **first matching** **`SecurityFilterChain`** and runs its ordered security filters (context → headers/CORS/CSRF → authentication → `ExceptionTranslationFilter` → `AuthorizationFilter`).

## End-to-end path

1. **Servlet container** builds a `FilterChain` for the request URI.
2. **`DelegatingFilterProxy`** resolves the Spring bean named **`springSecurityFilterChain`**.
3. **`FilterChainProxy`** chooses the **first** `SecurityFilterChain` whose `RequestMatcher` matches (later chains are ignored for that request).
4. That chain’s filters run in **registered order**, then the rest of the app (`DispatcherServlet`, …).

Details of the proxy bridge: [[What is FilterChainProxy and DelegatingFilterProxy]]. The chain bean itself: [[What is SecurityFilterChain]].

## Building a chain (`HttpSecurity`)

In modern Spring Security (5.7+ / 6.x, including Boot 3) you declare one or more `@Bean` **`SecurityFilterChain`** methods — **not** `WebSecurityConfigurerAdapter`:

```java
@Bean
@Order(1)
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http.securityMatcher("/api/**")
        .csrf(csrf -> csrf.disable())
        .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated());
    return http.build();
}
```

**Listing 1.** `securityMatcher` scopes the chain; `@Order` decides which chain `FilterChainProxy` tries first. Stateless APIs typically disable sessions (and often CSRF).

## Filter order (what interviewers sketch)

Exact order lives in **`FilterOrderRegistration`**. A typical debug line looks like:

`SecurityContextHolderFilter` → `HeaderWriterFilter` → `CorsFilter` → `CsrfFilter` → auth filters (`UsernamePasswordAuthenticationFilter`, Bearer/JWT custom, …) → `AnonymousAuthenticationFilter` → **`ExceptionTranslationFilter`** → **`AuthorizationFilter`**.

- **Authentication before authorization** — always.
- Custom JWT: usually **`OncePerRequestFilter`** + **`addFilterBefore(..., UsernamePasswordAuthenticationFilter.class)`** (or before **`AnonymousAuthenticationFilter`**) — [[Why does addFilterBefore target filter choice matter]], [[Why must a JWT filter run before AnonymousAuthenticationFilter]].

```d2
direction: right
req: "HTTP request" {
  width: 110
  height: 45
  style.fill: "#e3f2fd"
}
dfp: "DelegatingFilterProxy" {
  width: 150
  height: 45
  style.fill: "#fff3e0"
}
fcp: "FilterChainProxy\nspringSecurityFilterChain" {
  width: 180
  height: 55
  style.fill: "#fff3e0"
}
sfc: "First matching\nSecurityFilterChain" {
  width: 150
  height: 55
  style.fill: "#e8f5e9"
}
mvc: "DispatcherServlet" {
  width: 130
  height: 45
  style.fill: "#f3e5f5"
}

req -> dfp -> fcp -> sfc -> mvc
```

**Fig. 1.** One container entry point; `FilterChainProxy` selects and runs a single matching `SecurityFilterChain`.

> [!warning] First match wins
> With multiple chains, only the **first** matching `SecurityFilterChain` runs. A broad `/api/**` chain at `@Order(1)` can steal traffic from a more specific chain declared later — [[Why does authorization matcher order matter in Spring Security]] (same “first match” idea for `authorizeHttpRequests` rules inside a chain).

> [!tip] Interview answer
> SecurityFilterChain is an ordered list of Servlet filters owned by FilterChainProxy (bean springSecurityFilterChain), reached via DelegatingFilterProxy. Filters run before MVC: load SecurityContext, CSRF/CORS/headers, authenticate, translate exceptions, then AuthorizationFilter. Multiple chains use securityMatcher + @Order; custom filters use addFilterBefore/After against a known neighbor.
