<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What does an empty Security filter chain debug log mean?

> [!abstract] Short answer
> Under **`@EnableWebSecurity(debug = true)`**, `DebugFilter` prints **`Security filter chain:`** for that request. **`[] empty (bypassed by security='none')`** means a `SecurityFilterChain` **matched** and its filter list is **empty** — `WebSecurity.ignoring()` / XML **`security="none"`**. That URL is **not** running headers, CSRF, or `AuthorizationFilter`. **`no match`** is the other line: **no** chain’s `RequestMatcher` accepted the request, so `FilterChainProxy` applies **no** Spring Security filters either. Neither line is `permitAll()`.

## Three lines people mix up

```d2
direction: down
dbg: "DebugFilter\n@EnableWebSecurity(debug=true)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
full: "full filter list\npermitAll still here" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
empty: "[] empty (security='none')\nignoring() matched" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
nomatch: "no match\nsecurityMatcher miss" {
  width: 260
  height: 50
  style.fill: "#fce4ec"
}

dbg -> full
dbg -> empty
dbg -> nomatch
```

**Fig. 1.** Same prefix, three meanings. Only the empty-list and no-match paths skip Spring Security features.

`DebugFilter` walks `FilterChainProxy.getFilterChains()` and returns the **first** matching chain’s `getFilters()`, or **`null`** if none match:

| Log after `Security filter chain:` | What matched | Security applied |
| --- | --- | --- |
| named filters (`CsrfFilter`, `AuthorizationFilter`, …) | A normal `HttpSecurity` chain | Yes — including **`permitAll`** |
| `[] empty (bypassed by security='none')` | Chain with **zero** filters | **No** |
| `no match` | No `SecurityFilterChain` | **No** |

Startup **`DEBUG`** on `DefaultSecurityFilterChain` is the same split: **`Will not secure <matcher>`** when the list is empty; **`Will secure <matcher> with filters: …`** when it is not. Architecture’s example list (`DisableEncodeUrlFilter`, … `AuthorizationFilter`) is that second case.

```java
@Bean
WebSecurityCustomizer skipCss() {
    return (web) -> web.ignoring().requestMatchers("/css/**");
}

@Bean
@Order(1)
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http.securityMatcher("/api/**")
        .authorizeHttpRequests((a) -> a.anyRequest().authenticated());
    return http.build();
    // no catch-all chain → GET /home → DebugFilter: no match
}
```

**Listing 1.** `ignoring()` registers an **empty** chain (the `[]` log). A **`securityMatcher`** that never covers the URL is **`no match`**, not `[]`. Put a catch-all `SecurityFilterChain` last if `/home` should still be secured. See [[How do you ignore static resources in Spring Security]] and [[How do you configure a SecurityFilterChain bean in Spring Security 6]].

`logging.level.org.springframework.security=TRACE` does **not** print `Security filter chain: []`. `FilterChainProxy` then logs **`Securing …`** and **`Invoking SomeFilter (n/m)`**. **`Did not match request to …`** is almost always a **single filter’s** matcher (`LogoutFilter` skipping `/home`) — **normal**, not “every chain rejected the request.” See [[How do you enable Spring Security debug logging for the filter chain]].

> [!warning] Empty chain is not permitAll
> `requestMatchers("/css/**").permitAll()` still installs the **full** filter list (`HeaderWriterFilter`, CSRF, `SecurityContext`, `AuthorizationFilter`). The debug output is a long bracketed list, not `[]`. `[]` / `Will not secure` means Spring Security **opted out** for that pattern.

> [!tip] Interview answer
> If debug equals true and you see an empty security filter chain, a chain matched but it has no filters — ignoring or security none — so that request is unprotected. No match means securityMatcher never hit, which is also unprotected. permitAll still prints the whole filter list; TRACE Did not match on LogoutFilter is just that filter skipping the URL.
