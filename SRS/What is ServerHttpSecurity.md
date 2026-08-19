<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

ServerHttpSecurity is the WebFlux DSL (not HttpSecurity). Dumps call authorizeExchange, pathMatchers, httpBasic, formLogin, oauth2Login / oauth2ResourceServer, then http.build() to a SecurityWebFilterChain.

Mixing HttpSecurity in a WebFlux app is the usual dump mistake.
> [!warning] Unverified traps from the dump
> - pathMatchers / anyExchange replace requestMatchers / anyRequest.
