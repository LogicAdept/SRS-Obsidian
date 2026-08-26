<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS

# What is `SecurityWebFilterChain`?

> [!abstract] Short answer
> **`SecurityWebFilterChain`** is the WebFlux security chain: a **`Flux` of `WebFilter`s** that **`matches(ServerWebExchange)`** to decide if it applies. You build it with **`ServerHttpSecurity.build()`** (not servlet **`HttpSecurity` / `SecurityFilterChain`**). Several beans are allowed: **`@Order` + `securityMatcher`**; **the first match wins**.

## WebFilter chain, matched per exchange

Javadoc (since **5.0**): the interface can be matched against a `ServerWebExchange`. Implementation: **`MatcherSecurityWebFilterChain`**. Methods: **`matches`** → `Mono<Boolean>`; **`getWebFilters()`** → `Flux<WebFilter>`.

`ServerHttpSecurity` is **`HttpSecurity` for WebFlux**. Default matcher is **all requests**; narrow with **`securityMatcher(ServerWebExchangeMatcher)`**. Finish with **`http.build()`**.

Enable: **`@EnableWebFluxSecurity`**, then a `@Bean SecurityWebFilterChain` — [[What is EnableWebFluxSecurity]], [[How does Spring Security work with WebFlux]]. Inside one chain, **`authorizeExchange` / `pathMatchers`** are authorization rules, not the servlet `authorizeHttpRequests` / `requestMatchers` APIs — [[What is ServerHttpSecurity]], [[What is authorizeExchange in WebFlux security]], [[What is pathMatchers in WebFlux security]].

```java
@Bean
public SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
    http.authorizeExchange(ex -> ex.anyExchange().authenticated())
            .httpBasic(withDefaults())
            .formLogin(withDefaults());
    return http.build();
}
```

**Listing 1.** Conceptual explicit chain from Spring Security *WebFlux Security* (lambda DSL).

```d2
direction: down
ex: "ServerWebExchange" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
pick: "First matching\nSecurityWebFilterChain" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
filters: "getWebFilters()\nWebFilter Flux" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

ex -> pick -> filters
```

**Fig. 1.** Same idea as servlet `FilterChainProxy` picking one `SecurityFilterChain` — here the filters are **`WebFilter`s**. Pipeline: [[What is a WebFilter in WebFlux]].

## Several chains

Spring Security selects **one** `SecurityWebFilterChain` bean per request, in **`@Order`**, by each chain’s **`securityMatcher`**. A chain without a matcher matches **everything** (typical catch-all, lowest precedence).

```java
@Order(Ordered.HIGHEST_PRECEDENCE)
@Bean
SecurityWebFilterChain apiHttpSecurity(ServerHttpSecurity http) {
    http.securityMatcher(new PathPatternParserServerWebExchangeMatcher("/api/**"))
            .authorizeExchange(ex -> ex.anyExchange().authenticated())
            .oauth2ResourceServer(OAuth2ResourceServerSpec::jwt);
    return http.build();
}

@Bean
SecurityWebFilterChain webHttpSecurity(ServerHttpSecurity http) {
    http.authorizeExchange(ex -> ex.anyExchange().authenticated())
            .httpBasic(withDefaults());
    return http.build();
}
```

**Listing 2.** Conceptual multi-chain sample — `/api/**` first; implied any-request matcher on the second bean.

> [!warning] `HttpSecurity.build()` is the wrong type
> Servlet `@EnableWebSecurity` produces **`SecurityFilterChain`**. A WebFlux app needs **`ServerHttpSecurity` → `SecurityWebFilterChain`**. Mixing them does not configure reactive filters.

> [!warning] `pathMatchers` do not pick the chain
> They authorize **inside** a chain. Which chain runs is **`securityMatcher`** (and `@Order`). A more specific chain **without** a high `@Order` can lose to a catch-all.

> [!warning] `@WebFluxTest` does not load your chain bean
> Import it or use `@SpringBootTest` — [[How do you test a WebFlux endpoint]].

> [!tip] Interview answer
> **`SecurityWebFilterChain` is the reactive `SecurityFilterChain`: `WebFilter`s plus `matches(exchange)`.** Build it from `ServerHttpSecurity`. Multiple beans: first `@Order` + `securityMatcher` wins. Do not return servlet `HttpSecurity`.
