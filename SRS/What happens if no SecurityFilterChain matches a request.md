<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: FilterChainProxy iterates chains; if none match, it calls the servlet FilterChain with no Spring Security filters. The request is effectively unsecured — no CSRF, no headers, no AuthorizationFilter.
> [!warning] Unverified traps from the dump
> - @EnableWebSecurity / Boot auto-config usually installs a default chain that matches everything, so this only shows up if you replaced that and left a hole.
