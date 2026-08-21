<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS

# How does Spring Security work with WebFlux?

> [!abstract] Short answer
> On WebFlux, Spring Security is a stack of reactive **`WebFilter`**s, not servlet `Filter`s. You enable it with [[What is EnableWebFluxSecurity]], configure a [[What is SecurityWebFilterChain]] via **`ServerHttpSecurity`**, and authentication goes through [[What is ReactiveAuthenticationManager]] plus a `ReactiveUserDetailsService` such as [[What is MapReactiveUserDetailsService]].

Servlet apps hang off `DelegatingFilterProxy` → `FilterChainProxy` → `SecurityFilterChain` / `HttpSecurity`. WebFlux has **no** servlet filter chain. Spring Security’s WebFlux support registers a `WebFilter` that is a **`WebFilterChainProxy`**: it picks the first matching `SecurityWebFilterChain` and runs that chain’s `WebFilter`s before the rest of the Netty/WebFlux pipeline.

```d2
direction: down
exchange: "ServerWebExchange\n(WebFlux request)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
proxy: "WebFilterChainProxy\n(WebFilter)" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
chain: "First matching\nSecurityWebFilterChain" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
filters: "Ordered security\nWebFilters" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
handler: "WebHandler /\nRouter / Controller" {
  width: 260
  height: 70
  style.fill: "#f3e5f5"
}

exchange -> proxy
proxy -> chain
chain -> filters
filters -> handler
```

**Fig. 1.** Reactive path: exchange → `WebFilterChainProxy` → one `SecurityWebFilterChain` → handlers. Parallel to servlet `FilterChainProxy`, different types.

## Configuration surface (Spring Security 6+)

`@EnableWebFluxSecurity` imports the reactive security configuration. You declare one or more `SecurityWebFilterChain` beans built from `ServerHttpSecurity`. Authorization uses **`authorizeExchange`** (not `authorizeHttpRequests`). Path rules use **`pathMatchers`** / exchange matchers. Authentication DSLs include `httpBasic`, `formLogin`, and OAuth2 variants on the same builder.

```java
@Configuration
@EnableWebFluxSecurity
public class HelloWebfluxSecurityConfig {

    @Bean
    MapReactiveUserDetailsService userDetailsService() {
        UserDetails user = User.withUsername("user")
            .password("{bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG")
            .roles("USER")
            .build();
        return new MapReactiveUserDetailsService(user);
    }

    @Bean
    SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
        http
            .authorizeExchange(exchanges -> exchanges
                .pathMatchers("/public/**").permitAll()
                .anyExchange().authenticated()
            )
            .httpBasic(Customizer.withDefaults())
            .formLogin(Customizer.withDefaults());
        return http.build();
    }
}
```

**Listing 1.** Conceptual explicit WebFlux config: `ServerHttpSecurity` → `SecurityWebFilterChain`; users via `MapReactiveUserDetailsService`. Prefer a pre-encoded password in real apps.

For username/password, the reactive counterpart of `DaoAuthenticationProvider` wiring is typically **`UserDetailsRepositoryReactiveAuthenticationManager`** over a **`ReactiveUserDetailsService`**. `MapReactiveUserDetailsService` is the in-memory map implementation (think reactive `InMemoryUserDetailsManager`).

Multiple chains work like the servlet side: `@Order` plus `securityMatcher` (e.g. `PathPatternParserServerWebExchangeMatcher("/api/**")`). Spring Security selects **one** `SecurityWebFilterChain` per request by matcher order.

## Servlet types do not apply here

| Servlet stack | WebFlux stack |
| --- | --- |
| `HttpSecurity` | `ServerHttpSecurity` |
| `SecurityFilterChain` | `SecurityWebFilterChain` |
| `FilterChainProxy` | `WebFilterChainProxy` |
| `AuthenticationManager` | `ReactiveAuthenticationManager` |
| `UserDetailsService` | `ReactiveUserDetailsService` |

> [!warning] Do not wire `HttpSecurity` into a WebFlux app
> `HttpSecurity`, servlet `FilterChainProxy`, and `@EnableWebSecurity` belong to the servlet stack. Mixing them with WebFlux is the usual misconfiguration. Use `@EnableWebFluxSecurity` and `ServerHttpSecurity`.

> [!warning] `User.withDefaultPasswordEncoder()` is demo-only
> Official samples still show it, but the API is **deprecated** and documented as **unsafe for production** (password material can still be recovered from the running process). Hash ahead of time with a `PasswordEncoder`, then pass the encoded string to `User.withUsername(...).password(...)`.

> [!tip] Interview answer
> **WebFlux security is `WebFilter`-based:** `@EnableWebFluxSecurity` plus `ServerHttpSecurity` builds a `SecurityWebFilterChain`, orchestrated by `WebFilterChainProxy`. Use `authorizeExchange` / `pathMatchers` and reactive auth (`ReactiveAuthenticationManager`, `MapReactiveUserDetailsService`). Leave servlet `HttpSecurity` / `FilterChainProxy` for MVC apps.
