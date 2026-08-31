<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `WebSecurityCustomizer`?

> [!abstract] Short answer
> A **`@FunctionalInterface`** (since **5.4**) whose **`@Bean`s** `WebSecurityConfiguration` applies to **`WebSecurity`**. The usual lambda is **`web.ignoring().requestMatchers(...)`**: those URLs are **dropped out of Spring Security** — empty-filter chain, **no `SecurityContext`**, no headers, no CORS, no CSRF. Prefer **`permitAll`** on `HttpSecurity` except for true static files. This is **not** a `SecurityFilterChain` and **not** `permitAll()`.

## Customize `WebSecurity`, not `HttpSecurity`

```d2
direction: down
bean: "@Bean WebSecurityCustomizer" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
ws: "WebSecurity.ignoring()" {
  width: 220
  height: 40
}
empty: "empty SecurityFilterChain\nsecurity='none'" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}

bean -> ws
ws -> empty
```

**Fig. 1.** `WebSecurity` builds `FilterChainProxy`. `ignoring()` registers matchers Spring Security should skip. DEBUG: `[] empty (bypassed by security='none')`. Multiple customizer beans are **additive**. See [[What is the difference between permitAll and web ignoring]], [[How do you ignore static resources in Spring Security]], and [[What does an empty Security filter chain debug log mean]].

String `requestMatchers` here share the same `PathPattern` builder as `securityMatcher` / `authorizeHttpRequests`. XML twin: `security="none"`.

```java
@Bean
WebSecurityCustomizer skipStatic() {
    return (web) -> web.ignoring().requestMatchers("/static/**", "/favicon.ico");
}
```

**Listing 1.** Javadoc example shape. Pair with `@EnableWebSecurity` / a [[How do you configure a SecurityFilterChain bean in Spring Security 6]] for everything else. Public JSON that needs [[What is CorsFilter in Spring Security]] or [[What is HeaderWriterFilter]] belongs on **`permitAll`**, not here. See [[What is the purpose of EnableWebSecurity]].

> [!warning] `ignoring()` is not `permitAll()`
> No CSRF, no security headers, no CORS, no `SecurityContext`. Use it only for assets that must never see Security. An API path here is an unauthenticated hole with none of the exploit filters.

> [!tip] Interview answer
> WebSecurityCustomizer is a bean, since Spring Security 5.4, that customizes WebSecurity. The common use is web.ignoring for static paths so those requests skip the whole filter chain. That is not permitAll: you lose headers, CORS, and CSRF. Prefer permitAll on HttpSecurity unless the resource is truly static.
