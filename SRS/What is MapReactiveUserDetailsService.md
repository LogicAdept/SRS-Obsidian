<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump WebFlux in-memory users: MapReactiveUserDetailsService holding UserDetails built with User.withDefaultPasswordEncoder() (demo). It is the reactive stand-in for InMemoryUserDetailsManager.

UserDetailsRepositoryReactiveAuthenticationManager then loads from that service.
> [!warning] Unverified traps from the dump
> - withDefaultPasswordEncoder is dump demo-only and unsafe.
