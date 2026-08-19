<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

SecurityWebFilterChain is the WebFlux equivalent of SecurityFilterChain: a reactive chain built from ServerHttpSecurity. @EnableWebFluxSecurity plus a @Bean SecurityWebFilterChain is the dump setup.

authorizeExchange / pathMatchers replace authorizeHttpRequests / requestMatchers. You can declare several chains with different matchers, same idea as multiple servlet SecurityFilterChain beans.
> [!warning] Unverified traps from the dump
> - Returning HttpSecurity.build() in a WebFlux app is the wrong type. Use ServerHttpSecurity.
