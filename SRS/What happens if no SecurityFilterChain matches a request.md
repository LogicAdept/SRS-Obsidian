<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What happens if no `SecurityFilterChain` matches a request?

> [!abstract] Short answer
> **`FilterChainProxy` skips Spring Security’s security filters** and calls the rest of the servlet `FilterChain`. The request is **unsecured**: no CSRF, no security headers, no `AuthorizationFilter`, no form-login endpoints from that chain. That is **not** a 401/403 from Spring Security. `@EnableWebSecurity` / Boot **usually** install a chain that matches **everything**; the hole appears when you **replace** that default with beans that all use a **narrow `securityMatcher`**.

## First match, or nothing

`FilterChainProxy` walks its `SecurityFilterChain` list in order and runs **only the first** whose `RequestMatcher` accepts the request. Patterns that should be serviced **must be listed**; it does **not** keep scanning for extra filters. A chain **without** `securityMatcher` matches **any** request (put it **last**). See [[What is FilterChainProxy and DelegatingFilterProxy]] and [[How do you configure a SecurityFilterChain bean in Spring Security 6]].

```d2
direction: down
req: "GET /home" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
fcp: "FilterChainProxy" {
  width: 200
  height: 40
  style.fill: "#fff3e0"
}
api: "@Order(1) /api/**" {
  width: 200
  height: 40
  style.fill: "#eceff1"
}
none: "no chain matches" {
  width: 200
  height: 40
  style.fill: "#fce4ec"
}
svc: "servlet FilterChain\ncontroller as-is" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}

req -> fcp
fcp -> api: "no"
api -> none
none -> svc
```

**Fig. 1.** Miss every `securityMatcher` and Spring Security’s filters never run. `FilterChainProxy` itself still wraps the request (`HttpFirewall`) and still clears `SecurityContext` after the call.

```java
@Bean
@Order(1)
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http.securityMatcher("/api/**")
        .authorizeHttpRequests((a) -> a.anyRequest().authenticated());
    return http.build();
}
// no second bean without securityMatcher → GET /home is unsecured
```

**Listing 1.** One matching chain for `/api/**` only. Boot’s `defaultSecurityFilterChain` and `WebSecurityConfiguration`’s **synthesized** default both **stay off** once you publish your own `SecurityFilterChain` beans. Add a **catch-all** bean (no `securityMatcher`, lowest `@Order`) so `/home` is still protected. See [[Can Spring Security run with zero SecurityFilterChain beans]].

`@EnableWebSecurity(debug = true)` prints **`Security filter chain: no match`**. That is **not** the `[] empty (bypassed by security='none')` line from `WebSecurity.ignoring()`. Empty-filter chains **matched**; no-match means **no** chain. End result is the same for CSRF/headers/authorization. See [[What does an empty Security filter chain debug log mean]].

`anyRequest().authenticated()` / `permitAll()` / `denyAll()` never run on a miss — those rules live **inside** a chain that already matched. `requestMatchers` cannot “reach outside” a `securityMatcher`. A `/login` page on a `/api/**`-only chain is often a **404**: `UsernamePasswordAuthenticationFilter` was never installed for that URL.

> [!warning] A matcher hole is not denyAll
> Unmatched URLs are **open**, not forbidden. `denyAll()` only applies when a chain **matched** and `AuthorizationFilter` ran. After you write **any** `SecurityFilterChain` `@Bean`, do not assume Boot still covers `/**`.

> [!tip] Interview answer
> FilterChainProxy uses the first matching SecurityFilterChain; if none match it continues the servlet chain with no security filters, so the URL is unprotected. The default any-request chain usually hides this until you replace it with securityMatcher-only beans. Put a catch-all chain last; do not confuse a miss with permitAll or denyAll.
