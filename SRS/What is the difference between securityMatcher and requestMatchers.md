<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is the difference between `securityMatcher` and `requestMatchers`?

> [!abstract] Short answer
> **`http.securityMatcher(...)`** decides whether **this `HttpSecurity` / `SecurityFilterChain` runs at all**. **`FilterChainProxy`** picks the **first** matching chain (`@Order`). **`authorizeHttpRequests(...).requestMatchers(...)`** are **authorization rules inside** that chain. **`AuthorizationFilter`** uses them **after** the chain is selected. Same `RequestMatcher` / `PathPattern` types; **different layer**. A request that matches **no** chain is **unsecured**. A request that matches a chain but **no** rule is **denied** (until `anyRequest()`).

## Chain picker vs rule picker

```d2
direction: down
fcp: "FilterChainProxy" {
  width: 200
  height: 40
}
sm: "securityMatcher\nthis chain?" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
rm: "requestMatchers\nwhich AccessDecision?" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

fcp -> sm
sm -> rm: "if this chain won"
```

**Fig. 1.** Official wording: `securityMatchers` decide if a given `HttpSecurity` applies; `requestMatchers` decide which authorization rule applies. See [[What is securityMatcher in Spring Security]], [[What is FilterChainProxy and DelegatingFilterProxy]], and [[What is AuthorizationFilter in Spring Security]].

No `securityMatcher` means the chain matches **every** request (catch-all). `securityMatcher(String...)` **replaces** earlier matchers; `securityMatchers(Customizer)` **adds**. Put a **narrow** `@Order(1)` chain **before** the catch-all.

```java
http
    .securityMatcher("/api/**")
    .authorizeHttpRequests((authorize) -> authorize
        .requestMatchers("/api/admin/**").hasRole("ADMIN")
        .anyRequest().authenticated());
```

**Listing 1.** `/api/**` is the **chain** gate. `/api/admin/**` is a **rule** inside it. `/` never enters this chain. `requestMatchers("/api/**")` on a **catch-all** bean does **not** create a second chain — JWT vs form login still needs **two** beans, `securityMatcher`, and `@Order`. See [[How do you configure JWT and form login as two SecurityFilterChain beans]], [[How do you configure authorizeHttpRequests in Spring Security 6]], and [[What happens if no SecurityFilterChain matches a request]].

> [!warning] `requestMatchers` never splits chains
> `/api/**` only in `requestMatchers` still runs **one** filter list (form login, CSRF, sessions) for `/` and `/api`. The API is not a resource-server chain until `securityMatcher("/api/**")` is on a **separate**, **higher-priority** `SecurityFilterChain`. A lone `securityMatcher("/api/**")` with **no** catch-all bean leaves `/` **unprotected**.

> [!tip] Interview answer
> securityMatcher is the chain selector: FilterChainProxy asks whether this HttpSecurity applies. requestMatchers are the authorization rules AuthorizationFilter uses after that chain is chosen. Missing chain match is unsecured; missing rule match is deny. Two authentication styles need two chains with securityMatcher and Order, not two requestMatchers on one bean.
