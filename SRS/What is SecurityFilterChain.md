<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `SecurityFilterChain`?

> [!abstract] Short answer
> A **`SecurityFilterChain`** is one **ordered list of Spring Security `Filter`s** plus a **`RequestMatcher`** that decides whether that list applies to the current request. **`FilterChainProxy`** holds zero or more of these beans and runs **only the first matching chain**. You usually create one with **`HttpSecurity` … `return http.build()`**.

## Not the same as `FilterChainProxy`

| Type | Role |
|---|---|
| **`DelegatingFilterProxy`** | Servlet-container filter; looks up a Spring bean |
| **`FilterChainProxy`** (`springSecurityFilterChain`) | Chooses which `SecurityFilterChain` matches |
| **`SecurityFilterChain`** | The selected chain’s filters for that request |

See [[What is FilterChainProxy and DelegatingFilterProxy]] and the end-to-end flow in [[How does the Spring Security filter chain work]].

The interface exposes matching + the filter list (conceptually `matches(request)` and `getFilters()`). Implementations such as **`DefaultSecurityFilterChain`** are what `http.build()` returns.

## Declaring chains

```java
@Bean
@Order(1)
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http.securityMatcher("/api/**")
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .httpBasic(Customizer.withDefaults());
    return http.build();
}

@Bean
SecurityFilterChain ui(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .formLogin(Customizer.withDefaults());
    return http.build();
}
```

**Listing 1.** Separate chains for `/api/**` (Basic) vs the rest (form login). `@Order(1)` is tried first; no `@Order` defaults to **last**.

Each chain can enable a different filter set (JWT, form login, Basic, actuator). A chain may even have **zero** security filters when Spring Security should ignore those requests.

```d2
direction: down
fcp: "FilterChainProxy" {
  width: 200
  height: 45
  style.fill: "#fff3e0"
}
c1: "SecurityFilterChain @Order(1)\n/api/**" {
  width: 220
  height: 55
  style.fill: "#e8f5e9"
}
c2: "SecurityFilterChain (default)\n/**" {
  width: 220
  height: 55
  style.fill: "#e3f2fd"
}
filters: "That chain's Filters only" {
  width: 200
  height: 45
  style.fill: "#fce4ec"
}

fcp -> c1: "first match"
fcp -> c2: "else"
c1 -> filters
c2 -> filters
```

**Fig. 1.** First matching `SecurityFilterChain` wins; later chains are not merged.

> [!warning] Catch-all order
> A broad matcher (or a chain without `securityMatcher`) with a **low `@Order`** starves every later chain. Put **specific** chains first. Inside a chain, `authorizeHttpRequests` rules also use first-match — [[Why does authorization matcher order matter in Spring Security]].

> [!tip] Interview answer
> SecurityFilterChain is the bean you build from HttpSecurity: a request matcher plus an ordered list of security filters. FilterChainProxy picks the first matching chain per request. Multiple beans + @Order let /api use JWT while the UI uses form login.
