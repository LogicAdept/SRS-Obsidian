<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: SecurityFilterChain is the ordered list of servlet filters that actually run for a matching request. FilterChainProxy holds several of these beans and picks the first whose matches(request) is true.

The interface is matches(HttpServletRequest) plus getFilters(). Each chain can carry a different set — JWT for /api/**, form login for the UI, Basic for actuator.

You expose one as a @Bean: take HttpSecurity, configure the lambda DSL, return http.build().
> [!warning] Unverified traps from the dump
> - FilterChainProxy is not the same object as a SecurityFilterChain bean. The container-facing DelegatingFilterProxy looks up springSecurityFilterChain (the FilterChainProxy).
> - Only the first matching chain runs. A catch-all chain with a low @Order starves every later chain.
