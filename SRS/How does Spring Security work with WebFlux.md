<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS

# How does Spring Security work with WebFlux?

> [!abstract] Short answer
> Reactive Security is a **`WebFilter` chain**, not servlet **`Filter`s**. You enable it with **`@EnableWebFluxSecurity`** (Boot may add that) and a **`SecurityWebFilterChain`** built from **`ServerHttpSecurity`**: **`authorizeExchange`**, **`pathMatchers`**, then **`httpBasic` / `formLogin` / OAuth2**. Users live behind **`ReactiveUserDetailsService`** (for example **`MapReactiveUserDetailsService`**), not servlet `UserDetailsService`.

## WebFilter, not FilterChainProxy

Spring Security *WebFlux Security*: support **relies on a `WebFilter`** and works for annotated WebFlux and WebFlux.fn. Servlet **`HttpSecurity` / `SecurityFilterChain`** do not configure this stack.

`ServerHttpSecurity` javadoc: it is **`HttpSecurity` for WebFlux**. Default applies to all requests; narrow with **`securityMatcher`**. Finish with **`http.build()`** → **`SecurityWebFilterChain`**.

Enable: **`@EnableWebFluxSecurity`** on `@Configuration` — [[What is EnableWebFluxSecurity]]. Chain type: [[What is SecurityWebFilterChain]]. DSL: [[What is ServerHttpSecurity]], [[What is authorizeExchange in WebFlux security]], [[What is pathMatchers in WebFlux security]].

```java
@Configuration
@EnableWebFluxSecurity
public class HelloWebfluxSecurityConfig {

    @Bean
    public MapReactiveUserDetailsService userDetailsService() {
        UserDetails user = User.withDefaultPasswordEncoder()
                .username("user")
                .password("user")
                .roles("USER")
                .build();
        return new MapReactiveUserDetailsService(user);
    }

    @Bean
    public SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
        http.authorizeExchange(ex -> ex
                        .pathMatchers("/public/**").permitAll()
                        .anyExchange().authenticated())
                .httpBasic(withDefaults())
                .formLogin(withDefaults());
        return http.build();
    }
}
```

**Listing 1.** Conceptual mix of Spring Security’s explicit WebFlux sample and `pathMatchers` (lambda DSL, not the old `.and()` chain).

```d2
direction: down
ex: "ServerWebExchange" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
wf: "Security WebFilters\nSecurityWebFilterChain" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
app: "DispatcherHandler /\nRouterFunction" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

ex -> wf -> app
```

**Fig. 1.** Same `WebFilter` pipeline as the rest of WebFlux — [[What is a WebFilter in WebFlux]]. Authentication: [[What is ReactiveAuthenticationManager]], [[What is MapReactiveUserDetailsService]].

Multiple chains: `@Order` + `securityMatcher` (for example `/api/**` vs the rest).

> [!warning] Do not use servlet `HttpSecurity` in a WebFlux app
> `@EnableWebSecurity` and `SecurityFilterChain` target servlet filters. They will not build `ServerHttpSecurity`.

> [!warning] `User.withDefaultPasswordEncoder()` is demo-only
> Spring samples use it for illustrations. Production needs a real `PasswordEncoder`.

> [!warning] `@WebFluxTest` skips custom `SecurityWebFilterChain`
> Import that `@Bean` or use `@SpringBootTest` — [[How do you test a WebFlux endpoint]].

> [!tip] Interview answer
> **WebFlux Security is `WebFilter` + `ServerHttpSecurity` → `SecurityWebFilterChain`.** `@EnableWebFluxSecurity`, `authorizeExchange` / `pathMatchers`, reactive user details. Servlet `Filter` / `HttpSecurity` is the other stack.
