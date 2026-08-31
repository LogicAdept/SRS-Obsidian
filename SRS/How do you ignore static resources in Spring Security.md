<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# How do you ignore static resources in Spring Security?

> [!abstract] Short answer
> **Prefer `permitAll`**, not ignore. `requestMatchers("/css/**").permitAll()` still runs the chain so **security headers** (and CSRF, logging) apply. `WebSecurity.ignoring()` / a `WebSecurityCustomizer` **drops those requests out of Spring Security entirely** (empty-filter chain, no `SecurityContext`). Spring Security 6 recommends `permitAll` for static assets; the old session cost is gone.

## Permit in the chain (preferred)

```java
http.authorizeHttpRequests((authorize) -> authorize
        .requestMatchers("/css/**", "/js/**", "/images/**").permitAll()
        .anyRequest().authenticated());
```

**Listing 1.** Spring Security 6 DSL (`requestMatchers`, not `antMatchers` / `authorizeRequests`). First-match: static patterns **before** `anyRequest()`. See [[How do you configure authorizeHttpRequests in Spring Security 6]] and [[What is the difference between permitAll and web ignoring]].

Boot’s `PathRequest.toStaticResources().atCommonLocations()` is a `RequestMatcher` for the usual static locations; use it the same way as the string patterns.

## Ignore (leave the chain)

```java
@Bean
WebSecurityCustomizer skipStatics() {
    return (web) -> web.ignoring()
            .requestMatchers("/resources/**", "/static/**");
}
```

**Listing 2.** `WebSecurity.ignoring()` (XML `filters="none"` / a `DefaultSecurityFilterChain` with **zero** filters). `SecurityContext` is **not** available on those requests. Use only for truly static files; for anything dynamic, **allow all users** in `HttpSecurity` instead.

```d2
direction: down
req: "GET /css/app.css" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
perm: "permitAll in HttpSecurity\nheaders · CSRF · then 200" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
ign: "web.ignoring()\nno security filters" {
  width: 240
  height: 55
  style.fill: "#fce4ec"
}

req -> perm: "preferred"
req -> ign: "filters gone"
```

**Fig. 1.** Same URL, two meanings of “public”: authorized-anonymous vs never entered `FilterChainProxy`’s security filters.

> [!warning] `ignoring()` skips headers, CSRF, and security logs
> Spring Security **cannot** write secure headers on an ignored request. That is why `permitAll` is the documented default for `/css/**`. Do not ignore `/actuator/**` either: that is not a static tree. Boot’s `EndpointRequest` (and the default health-only rule) is how you open **selected** actuator endpoints — `permitAll("/actuator/**")` exposes env and the rest.

> [!tip] Interview answer
> For static files use authorizeHttpRequests requestMatchers("/css/**").permitAll() so HeaderWriterFilter still runs. WebSecurityCustomizer ignoring() bypasses the whole chain — no CSRF, no headers, no SecurityContext. Since Spring Security 6 there is no session-performance reason to ignore; keep ignoring for assets you truly want Spring Security to never see.
