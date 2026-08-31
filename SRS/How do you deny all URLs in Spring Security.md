<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# How do you deny all URLs in Spring Security?

> [!abstract] Short answer
> Use **`anyRequest().denyAll()`** (XML: `<intercept-url pattern="/**" access="denyAll"/>`). That rule **refuses every matching request** and does **not** look up `Authentication`. Put it **last** as an allow-list catch-all, or on a **last** `SecurityFilterChain` with no `securityMatcher` so leftover URLs are closed.

## `denyAll` is a rule, not a second chain

```java
http.authorizeHttpRequests((authorize) -> authorize.anyRequest().denyAll());
```

**Listing 1.** Spring Security 6 lambda DSL. Opposite of `permitAll()`: always refuse, skip session `Authentication` lookup. The dump’s `.and().httpBasic()` form is the old chained DSL; it does not change `denyAll`.

```java
@Bean
SecurityFilterChain web(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests((authorize) -> authorize
            .dispatcherTypeMatchers(DispatcherType.FORWARD, DispatcherType.ERROR).permitAll()
            .requestMatchers("/login", "/css/**").permitAll()
            .anyRequest().denyAll());
    return http.build();
}
```

**Listing 2.** Official allow-list shape: public matchers **first**, then `anyRequest().denyAll()` so anything you forgot is **403**, not open. XML is the same order of `<intercept-url>` lines. See [[How do you configure authorizeHttpRequests in Spring Security 6]] and [[Does intercept-url order matter in Spring Security]].

A **second** bean with no `securityMatcher` and `anyRequest().denyAll()` is how you close URLs that never hit a more specific chain (scoped `/api/**` or `/secured/**` first). That is “deny the rest of the app,” not “deny inside one matcher.”

```d2
direction: down
req: "GET /anything" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
list: "authorizeHttpRequests\nfirst match" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
pub: "requestMatchers /login\npermitAll" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
deny: "anyRequest().denyAll()" {
  width: 220
  height: 45
  style.fill: "#fce4ec"
}

req -> list
list -> pub: "/login"
list -> deny: "else"
```

**Fig. 1.** `denyAll` on `anyRequest()` is the last pair. First-match means a `denyAll` **above** `/login` also blocks login.

> [!warning] `denyAll` first locks login, static, and error dispatches
> `AuthorizationFilter` applies **only the first** match. `anyRequest().denyAll()` at the top matches **every** URL, including `formLogin`’s `/login` and MVC `FORWARD`/`ERROR` dispatches. Permit those explicitly, then deny the rest. See [[Why does authorization matcher order matter in Spring Security]].

> [!tip] Interview answer
> Deny everything with anyRequest().denyAll() — it rejects the request without even loading Authentication. Use it last as an allow-list, or as a catch-all SecurityFilterChain after more specific matchers. Put it first and you also deny /login and error pages.
