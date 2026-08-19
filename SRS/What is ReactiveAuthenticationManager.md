<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

ReactiveAuthenticationManager authenticates in a non-blocking way. The key method is Mono<Authentication> authenticate(Authentication).

Dumps use UserDetailsRepositoryReactiveAuthenticationManager wrapping a ReactiveUserDetailsService, or a custom implementation that returns Mono.just(authenticatedToken) / Mono.error(...).
> [!warning] Unverified traps from the dump
> - Blocking inside authenticate (JDBC on the event loop) defeats WebFlux. Use a reactive store or subscribeOn a bounded elastic pool.
