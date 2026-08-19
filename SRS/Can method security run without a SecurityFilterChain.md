<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: yes. Method security is AOP on the service bean. Tests use @EnableMethodSecurity without replacing SecurityFilterChain. Scheduled jobs and listeners have no filter chain at all.
> [!warning] Unverified traps from the dump
> - Without a web chain, there is no ExceptionTranslationFilter. AccessDeniedException stays an exception, not an HTTP 403, unless you translate it.
