<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump one-liner: AuthorizationFilter (6.x) uses AuthorizationManager instead of AccessDecisionManager + voters. Same pattern as method security. FilterSecurityInterceptor is the old URL interceptor; ExceptionTranslationFilter still wraps whichever enforcer you have.
> [!warning] Unverified traps from the dump
> - Seeing both in one app is a migration leftover. New authorizeHttpRequests wires AuthorizationFilter.
