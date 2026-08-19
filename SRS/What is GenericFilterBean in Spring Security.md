<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: implement org.springframework.web.filter.GenericFilterBean (a Spring-aware Filter) for a custom security filter. Override doFilter, then register it on SecurityFilterChain with addFilterAfter / addFilterBefore.

OncePerRequestFilter is the other dump base class; GenericFilterBean is the simpler Spring Filter adapter.
> [!warning] Unverified traps from the dump
> - A Filter that is only a servlet FilterRegistrationBean may run outside Spring Security’s order.
