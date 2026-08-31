<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# How do you disable form login on a `SecurityFilterChain`?

> [!abstract] Short answer
> On a chain you configure yourself, **do not call `formLogin()`** — once any servlet `HttpSecurity` config exists, form login is **opt-in**. To strip it when it would still be registered (Boot default, or you already called `formLogin(withDefaults())`), use **`http.formLogin((form) -> form.disable())`**. That drops `UsernamePasswordAuthenticationFilter` and the generated `/login` page.

## Opt-in after you write a chain

By default (no `SecurityFilterChain` bean), Spring Security **enables** form login. As soon as you provide servlet security config, you must **turn it on explicitly**:

```java
http.formLogin(Customizer.withDefaults());
```

**Listing 1.** Adds `UsernamePasswordAuthenticationFilter` (and usually `DefaultLoginPageGeneratingFilter` for `/login`). XML is `<form-login />`. See [[How do you configure a SecurityFilterChain bean in Spring Security 6]].

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http.securityMatcher("/api/**")
        .authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
        .oauth2ResourceServer((oauth2) -> oauth2.jwt(Customizer.withDefaults()))
        .formLogin((form) -> form.disable());
    return http.build();
}
```

**Listing 2.** JWT/API chain: **disable** form login so this chain has no username/password filter and no `/login`. Omitting `.formLogin(...)` entirely does the same once this `HttpSecurity` is your configuration. `httpBasic((basic) -> basic.disable())` is the same DSL for Basic. See [[How do you configure JWT and form login as two SecurityFilterChain beans]].

Keep `formLogin` on a **UI** catch-all bean if browsers still need a login page. `formLogin()` is what publishes `GET`/`POST /login`; a `securityMatcher` that does not include those URLs yields **404**, not a disabled filter.

```d2
direction: down
cfg: "Your SecurityFilterChain" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
on: "formLogin(withDefaults())\nUsernamePasswordAuthenticationFilter" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
off: "omit formLogin or form.disable()\nno /login filter" {
  width: 300
  height: 55
  style.fill: "#fce4ec"
}

cfg -> on: "opt in"
cfg -> off: "API / Bearer chain"
```

**Fig. 1.** Form login is not implied by `authorizeHttpRequests` alone after you declare a chain.

If you `addFilterAt(..., UsernamePasswordAuthenticationFilter.class)` **and** still call `formLogin()`, Spring Security tries to add that filter **twice** and fails. Remove `formLogin` or `formLogin((form) -> form.disable())`, then add your filter — same as the documented `httpBasic` + `addFilterAt` case. Architecture’s `addFilterAt` “replaces” wording is the intended slot; it does **not** mean you can leave `formLogin()` enabled.

> [!warning] Disabling form login removes `/login` on that chain
> That is what an API chain wants. A **browser** app whose **only** bean calls `form.disable()` (or never calls `formLogin()`) has no login page and no `UsernamePasswordAuthenticationFilter`. Put form login on a second, last chain, or you will bounce unauthenticated HTML users to HTTP Basic/Bearer/401 instead of a form.

> [!tip] Interview answer
> After you write a SecurityFilterChain, form login is opt-in — skip formLogin() or call formLogin(form -> form.disable()) so UsernamePasswordAuthenticationFilter is not registered. Boot’s default chain still has form login until you replace it. Disable it on the JWT chain; keep it on the UI catch-all if you still need /login.
