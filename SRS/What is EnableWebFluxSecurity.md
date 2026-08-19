<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Annotations #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump annotation @EnableWebFluxSecurity on a @Configuration class that exposes SecurityWebFilterChain(ServerHttpSecurity). It is the reactive twin of @EnableWebSecurity.

Without it, WebFlux dumps still expect you to define the chain bean; mixing servlet @EnableWebSecurity in a WebFlux app is wrong.
> [!warning] Unverified traps from the dump
> - @EnableWebSecurity does not configure ServerHttpSecurity.
