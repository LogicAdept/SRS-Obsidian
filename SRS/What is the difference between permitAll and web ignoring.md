<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: permitAll() is an authorizeHttpRequests rule inside a chain. Filters still run (CORS, headers, CSRF, ExceptionTranslationFilter).

web.ignoring() / WebSecurityCustomizer skips the whole chain. Public API that still needs CORS belongs on permitAll, not ignoring.
> [!warning] Unverified traps from the dump
> - Copy-paste requestMatchers("/admin/**").permitAll() meant for health checks is a dump breach story. ignoring() on an API path is worse: no headers either.
