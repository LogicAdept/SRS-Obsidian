<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is the difference between `permitAll` and web ignoring?

> [!abstract] Short answer
> **`permitAll()`** is an **`authorizeHttpRequests` rule** on a matching `SecurityFilterChain`. The request still runs **CORS, headers, CSRF, `ExceptionTranslationFilter`**. **`web.ignoring()`** / a **`WebSecurityCustomizer`** registers matchers Spring Security **skips entirely** — empty-filter chain, **no `SecurityContext`**, no headers. Official guidance: **prefer `permitAll`**. Use ignore only for true static files. A public API that still needs CORS belongs on `permitAll`, not `ignoring()`.

## Inside the chain vs out of Spring Security

```d2
direction: down
req: "GET /css/app.css" {
  width: 180
  height: 40
}
permit: "permitAll\nHeaderWriter, Cors, Csrf still run" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
ignore: "web.ignoring()\nno Security filters" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}

req -> permit: "preferred"
req -> ignore: "static-only"
```

**Fig. 1.** `AuthorizationFilter` grants `permitAll` without looking up `Authentication` (Spring Security 6). Other filters still run. `WebSecurity.ignoring()`: “Web Security … (including the `SecurityContext`) will not be available.” DEBUG: `[] empty (bypassed by security='none')`. See [[How do you ignore static resources in Spring Security]], [[What does an empty Security filter chain debug log mean]], and [[What is HeaderWriterFilter]].

XML analogue of ignore is `security="none"`. XML analogue of `permitAll` is `<intercept-url … access="permitAll"/>` on a real `<http>` chain.

```java
http.authorizeHttpRequests((authorize) -> authorize
        .requestMatchers("/css/**", "/actuator/health").permitAll()
        .anyRequest().authenticated());

@Bean
WebSecurityCustomizer skipStatic() {
    return (web) -> web.ignoring().requestMatchers("/static/**");
}
```

**Listing 1.** Permit public HTTP endpoints (health, CORS APIs, login page). Ignore only assets that must not see Security at all. First-match still applies: `requestMatchers("/admin/**").permitAll()` **before** `authenticated()` opens admin. See [[How do you configure authorizeHttpRequests in Spring Security 6]], [[What is CorsFilter in Spring Security]], and [[Why does authorization matcher order matter in Spring Security]].

> [!warning] `ignoring()` on an API drops CORS and headers
> A public JSON endpoint that browsers call **cross-origin** needs [[What is CorsFilter in Spring Security]] in the chain — that is `permitAll`, not ignore. `permitAll` also does **not** turn off CSRF: a POST that is permitted still needs a token unless you disable CSRF for that API.

> [!tip] Interview answer
> permitAll is an authorization rule: anonymous is allowed, but the Security filters still run, so you keep headers, CORS, and CSRF. web.ignoring or WebSecurityCustomizer takes the request out of Spring Security completely — no SecurityContext, no headers. Since Spring Security 6 there is no session penalty, so prefer permitAll except for pure static files.
