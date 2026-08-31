<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Annotations #SRS

# What is `securityMatcher` in Spring Security?

> [!abstract] Short answer
> **`http.securityMatcher(...)`** sets the **`RequestMatcher`** on this **`HttpSecurity` / `SecurityFilterChain`**: which requests **enter this chain**. Default is **any request**. [[What is FilterChainProxy and DelegatingFilterProxy]] tries chains in **`@Order`**; **first match wins**. **`authorizeHttpRequests` / `requestMatchers`** are **rules inside** the chosen chain — not another chain selector. No matching chain → **unprotected**.

## Chain picker, not an authorization rule

```d2
direction: down
fcp: "FilterChainProxy" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
api: "@Order(1)\nsecurityMatcher(/api/**)" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
ui: "no matcher\nformLogin catch-all" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}

fcp -> api: "/api/x"
fcp -> ui: "else"
```

**Fig. 1.** Java-config: recommend **one** chain **without** `securityMatcher` so the rest of the app is still protected. See [[What happens if no SecurityFilterChain matches a request]] and [[What happens if two SecurityFilterChain beans have no Order]].

`securityMatcher(String...)` / `securityMatcher(RequestMatcher)` **replace** prior matchers. `securityMatchers { requestMatchers(...) }` **adds** (does not wipe). Patterns follow **`PathPattern`**. `anyRequest()` inside `authorizeHttpRequests` means “everything else **this chain already matched**,” not the whole application. See [[How do you configure authorizeHttpRequests in Spring Security 6]] and [[What is HttpSecurity in Spring Security]].

```java
@Bean
@Order(1)
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http.securityMatcher("/api/**")
        .authorizeHttpRequests((a) -> a.anyRequest().hasRole("ADMIN"))
        .httpBasic(Customizer.withDefaults());
    return http.build();
}

@Bean
SecurityFilterChain ui(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests((a) -> a.anyRequest().authenticated())
        .formLogin(Customizer.withDefaults());
    return http.build();
}
```

**Listing 1.** Documented split: JWT/Basic on `/api/**`, form login elsewhere. `formLogin`’s `/login` must live on a chain whose matcher **includes** `/login`. See [[How do you configure JWT and form login as two SecurityFilterChain beans]] and [[How do you configure a SecurityFilterChain bean in Spring Security 6]].

> [!warning] Matcher vs requestMatchers; catch-all first
> Interview slip: `securityMatcher` **selects the chain**; `requestMatchers` **authorize inside it**. `@Order(1)` with **no** matcher is a **catch-all** — later chains never run. A **lone** `securityMatcher("/secured/**")` bean leaves `/` **open**.

> [!tip] Interview answer
> securityMatcher is how one SecurityFilterChain opts into a subset of URLs. FilterChainProxy uses first match by @Order. Without a matcher the chain takes every request. requestMatchers inside authorizeHttpRequests are not the same thing — they only apply after this chain was chosen.
