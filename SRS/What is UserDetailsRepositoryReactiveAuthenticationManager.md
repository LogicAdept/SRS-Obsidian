<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump default reactive username/password manager: UserDetailsRepositoryReactiveAuthenticationManager wrapping a ReactiveUserDetailsService (MapReactiveUserDetailsService in samples). authenticate() returns Mono<Authentication>.

It is DaoAuthenticationProvider for WebFlux.
> [!warning] Unverified traps from the dump
> - Blocking JDBC inside authenticate on the event loop is the dump’s performance trap. Use a reactive store or a bounded elastic scheduler.
