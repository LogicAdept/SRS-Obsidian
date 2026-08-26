<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Annotations #Java/Spring/Framework/WebFlux #SRS

# What is `EnableWebFluxSecurity`?

> [!abstract] Short answer
> **`@EnableWebFluxSecurity`** turns on **Spring Security for WebFlux**: it imports reactive security configuration so you can declare **`ServerHttpSecurity` / `SecurityWebFilterChain`** beans. It is the **reactive twin of `@EnableWebSecurity`**, not a substitute — servlet `HttpSecurity` is a different stack.

## What the annotation imports

`@EnableWebFluxSecurity` javadoc (since 5.0): put it on a `@Configuration` class to add **Spring Security WebFlux support**. You may then create one or more **`ServerHttpSecurity`** beans.

It `@Import`s `ServerHttpSecurityConfiguration`, `WebFluxSecurityConfiguration`, plus OAuth2-client / observation import selectors.

Spring Security *WebFlux Security* works via a **`WebFilter`** (same for annotated WebFlux and WebFlux.fn). Minimal config: the annotation plus a **`MapReactiveUserDetailsService`** — defaults include form + HTTP Basic, authenticated-any-exchange, login/logout pages, security headers, CSRF.

Explicit config: a `@Bean SecurityWebFilterChain` that receives `ServerHttpSecurity`, calls `authorizeExchange` / `httpBasic` / `formLogin`, then **`http.build()`**.

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
        http.authorizeExchange(ex -> ex.anyExchange().authenticated())
                .httpBasic(withDefaults())
                .formLogin(withDefaults());
        return http.build();
    }
}
```

**Listing 1.** Explicit WebFlux security from Spring Security reference. Chain details: [[What is SecurityWebFilterChain]]; DSL: [[What is ServerHttpSecurity]].

```d2
direction: down
ann: "@EnableWebFluxSecurity\non @Configuration" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
cfg: "WebFluxSecurityConfiguration\nServerHttpSecurity beans" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
chain: "SecurityWebFilterChain\nWebFilter" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

ann -> cfg -> chain
```

**Fig. 1.** Servlet `@EnableWebSecurity` wires `HttpSecurity` / servlet filters — not this path. Overview: [[How does Spring Security work with WebFlux]].

Spring Boot *Spring Security*: `ReactiveWebSecurityAutoConfiguration` **switches on `@EnableWebFluxSecurity` if you did not add it**, and backs off if a `WebFilterChainProxy` is already defined. You can still declare a custom `SecurityWebFilterChain` without repeating the annotation in Boot apps.

Multiple chains: `@Order` + `securityMatcher` (for example `/api/**` vs the rest).

> [!warning] `@EnableWebSecurity` does not configure `ServerHttpSecurity`
> That annotation is servlet-stack (`HttpSecurity`, `SecurityFilterChain`). In a WebFlux app it will not build the reactive filter chain.

> [!warning] `withDefaultPasswordEncoder()` is demo-only
> Spring’s samples use it for illustrations. Production needs a real `PasswordEncoder`.

> [!warning] Defaults authenticate everything
> Minimal `@EnableWebFluxSecurity` + user details still requires an authenticated user for **any** exchange unless you customize `authorizeExchange`.

> [!tip] Interview answer
> **`@EnableWebFluxSecurity` enables reactive Spring Security** — `ServerHttpSecurity` and `SecurityWebFilterChain` as `WebFilter`s. It is `@EnableWebSecurity` for WebFlux, not for MVC. Boot may apply it for you; you still declare the chain bean to change rules.
