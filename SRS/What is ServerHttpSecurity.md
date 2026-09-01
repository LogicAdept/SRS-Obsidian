<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/WebFlux #Java/Spring/Framework/WebFlux #SRS

# What is `ServerHttpSecurity`?

> [!abstract] Short answer
> **`ServerHttpSecurity`** is Spring Security’s **WebFlux DSL** — **`HttpSecurity` for reactive HTTP**. You inject it into a `@Bean`, call **`authorizeExchange`**, **`httpBasic` / `formLogin` / OAuth2**, optionally **`csrf`**, then **`build()`** to a **`SecurityWebFilterChain`**. Default: **all requests**. Narrow the chain with **`securityMatcher`**. Servlet **`HttpSecurity`** is the other type.

## HttpSecurity for `ServerWebExchange`

Javadoc (since **5.0**): similar to **`HttpSecurity`**, but for **WebFlux**. Configures web security for HTTP requests. Applied to **every** exchange unless you set **`securityMatcher(ServerWebExchangeMatcher)`**.

You do not return `ServerHttpSecurity`. You return **`http.build()`** → [[What is SecurityWebFilterChain]]. Enable with **`@EnableWebFluxSecurity`** — [[What is EnableWebFluxSecurity]], [[How does Spring Security work with WebFlux]].

| Servlet (`HttpSecurity`) | WebFlux (`ServerHttpSecurity`) |
| --- | --- |
| `authorizeHttpRequests` / `requestMatchers` / `anyRequest` | **`authorizeExchange`** / **`pathMatchers`** / **`anyExchange`** |
| `SecurityFilterChain` | **`SecurityWebFilterChain`** |
| servlet `Filter` | **`WebFilter`** |

Authorization rules: [[What is authorizeExchange in WebFlux security]], [[What is pathMatchers in WebFlux security]]. **`pathMatchers` is not `securityMatcher`:** the first picks URLs **inside** the chain; the second picks **which chain** runs.

```java
@Bean
public SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
    http.authorizeExchange(ex -> ex
                    .pathMatchers("/public/**").permitAll()
                    .anyExchange().authenticated())
            .httpBasic(withDefaults())
            .formLogin(withDefaults());
    return http.build();
}
```

**Listing 1.** Conceptual mix of Spring Security’s explicit WebFlux sample and `pathMatchers` (lambda `Customizer` DSL).

Same class also exposes **`oauth2Login`**, **`oauth2ResourceServer`**, **`oauth2Client`**, **`csrf`**, headers, logout, CORS, HTTPS redirect. Minimal `@EnableWebFluxSecurity` + user details already turns on form + Basic, authenticated-any-exchange, CSRF, headers.

```d2
direction: down
dsl: "ServerHttpSecurity\nauthorizeExchange / httpBasic / …" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
build: "http.build()" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
chain: "SecurityWebFilterChain\nWebFilter Flux" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

dsl -> build -> chain
```

**Fig. 1.** The DSL object is a **builder**. The runtime type is the chain.

Modular config: `Customizer<ServerHttpSecurity>` beans run **before** the `SecurityWebFilterChain` `@Bean` sees `http`.

> [!warning] Do not inject servlet `HttpSecurity` in a WebFlux app
> `@EnableWebSecurity` + `SecurityFilterChain` never produce this type. `http.build()` would be the **wrong chain**.

> [!warning] `authorizeRequests()` is not this DSL
> That is the old servlet API. On WebFlux use **`authorizeExchange`**.

> [!warning] `formLogin()` without a `Customizer` still exists in samples
> Prefer **`formLogin(withDefaults())` / `httpBasic(withDefaults())`** like current reference listings. `User.withDefaultPasswordEncoder()` stays **demo-only**.

> [!tip] Interview answer
> **`ServerHttpSecurity` is WebFlux `HttpSecurity`.** `authorizeExchange` + `pathMatchers`/`anyExchange`, then `http.build()` → `SecurityWebFilterChain`. `securityMatcher` selects the chain; `pathMatchers` authorize inside it. Never mix servlet `HttpSecurity` into a Netty/WebFlux app.
