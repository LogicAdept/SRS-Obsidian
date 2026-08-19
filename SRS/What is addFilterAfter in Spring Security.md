<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: http.addFilterAfter(new CustomFilter(), BasicAuthenticationFilter.class) inserts your filter immediately after that known filter.

addFilterBefore is the JWT-dump twin (before UsernamePasswordAuthenticationFilter). addFilterAt replaces a slot. Wrong landmark → wrong phase.
> [!warning] Unverified traps from the dump
> - The target class must already be in that SecurityFilterChain. After a filter that is not registered, registration fails at startup.
