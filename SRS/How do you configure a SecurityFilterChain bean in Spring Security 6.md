<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# How do you configure a `SecurityFilterChain` bean in Spring Security 6?

> [!abstract] Short answer
> Expose a `@Bean SecurityFilterChain` that takes `HttpSecurity`, configure it with the **lambda DSL**, and `return http.build()`. Pair that with `@Configuration` and `@EnableWebSecurity`. This **replaced** `WebSecurityConfigurerAdapter` (deprecated in 5.7, gone in 6). Several beans plus `securityMatcher` and `@Order` give you multiple chains; `FilterChainProxy` runs the **first match**.

## One bean from `HttpSecurity`

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain app(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests((authorize) -> authorize
                .requestMatchers("/css/**", "/login").permitAll()
                .anyRequest().authenticated()
            )
            .formLogin(Customizer.withDefaults());
        return http.build();
    }
}
```

**Listing 1.** Spring Security 6 shape: inject `HttpSecurity`, declare `authorizeHttpRequests` + `requestMatchers`, finish with `anyRequest()`, enable form login, **build** the chain. `@EnableWebSecurity` still publishes `springSecurityFilterChain` (`FilterChainProxy`); your bean is one [[What is SecurityFilterChain]] inside it. See [[What is HttpSecurity in Spring Security]] and [[Why was WebSecurityConfigurerAdapter removed]].

That is the same default the framework synthesizes when you declare **no** chain bean: `anyRequest().authenticated()`, form login, HTTP Basic — then `http.build()`.

Use **`authorizeHttpRequests`**, not `authorizeRequests`. The former installs `AuthorizationFilter` and `AuthorizationManager` rules; the latter is the old `FilterSecurityInterceptor` path. Match paths with **`requestMatchers`** (and `anyRequest()`), not `antMatchers` / `mvcMatchers`.

## Several beans

```java
@Bean
@Order(1)
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http.securityMatcher("/api/**")
        .authorizeHttpRequests((authorize) -> authorize.anyRequest().hasRole("ADMIN"))
        .httpBasic(Customizer.withDefaults());
    return http.build();
}

@Bean
SecurityFilterChain ui(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
        .formLogin(Customizer.withDefaults());
    return http.build();
}
```

**Listing 2.** First matching chain wins. `@Order(1)` is tried first; no `@Order` is last. `securityMatcher` scopes **which requests enter this chain**. `requestMatchers` / `anyRequest` are **authorization rules inside** that chain. A chain with no `securityMatcher` matches every remaining request — keep one of those as a catch-all. See [[What is securityMatcher in Spring Security]].

```d2
direction: down
cfg: "@EnableWebSecurity\n@Bean SecurityFilterChain" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
http: "HttpSecurity lambda DSL\nauthorizeHttpRequests · formLogin · …" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
build: "http.build()\n→ SecurityFilterChain" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
fcp: "FilterChainProxy\nfirst matching chain" {
  width: 260
  height: 60
  style.fill: "#fce4ec"
}

cfg -> http
http -> build
build -> fcp
```

**Fig. 1.** Component configuration: DSL on `HttpSecurity`, `build()`, then `FilterChainProxy` selects among beans.

Boot’s default `SecurityFilterChain` **backs off** as soon as you publish your own. You then own every matcher and filter on that bean.

> [!warning] No matching chain is unsecured — missing `anyRequest()` is not
> If **no** `SecurityFilterChain` matches (every bean used a narrow `securityMatcher`), Spring Security does **not** protect the request. End with a catch-all chain (no `securityMatcher`). Inside a chain, if **no** `requestMatchers` line matches, `RequestMatcherDelegatingAuthorizationManager` **denies** (`Denying request since did not find matching RequestMatcher`) — it does **not** leave the URL public. Still put `anyRequest().authenticated()` or `anyRequest().denyAll()` last so the list is an explicit allow-list and first-match stays obvious. See [[Why does authorization matcher order matter in Spring Security]].

> [!tip] Interview answer
> In Spring Security 6 you drop WebSecurityConfigurerAdapter and expose a SecurityFilterChain bean: take HttpSecurity, use the lambda DSL, return http.build(). authorizeHttpRequests plus requestMatchers replaced authorizeRequests and antMatchers. Multiple beans use securityMatcher and @Order; first match wins, and a chain with no matcher is the catch-all.
