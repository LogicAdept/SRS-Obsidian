<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Reactive apps use spring-security-webflux, not servlet Filter. Dumps configure SecurityWebFilterChain with ServerHttpSecurity: authorizeExchange, pathMatchers, httpBasic / formLogin / oauth2.

ReactiveAuthenticationManager (often UserDetailsRepositoryReactiveAuthenticationManager) plus MapReactiveUserDetailsService replace AuthenticationManager and InMemoryUserDetailsManager. @EnableWebFluxSecurity is the dump annotation.

```java
@Bean
SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
    return http.authorizeExchange()
        .pathMatchers("/public/**").permitAll()
        .anyExchange().authenticated()
        .and().httpBasic().and().build();
}
```
> [!warning] Unverified traps from the dump
> - HttpSecurity and FilterChainProxy do not apply to WebFlux. Mixing them is the usual mistake.
> - User.withDefaultPasswordEncoder() in dumps is demo-only and unsafe.
