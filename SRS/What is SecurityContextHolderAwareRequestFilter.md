<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump default order (~1200): wraps HttpServletRequest so getRemoteUser(), isUserInRole(), and getUserPrincipal() read Spring Security’s Authentication instead of the raw servlet principal.
> [!warning] Unverified traps from the dump
> - isUserInRole('ADMIN') typically looks for ROLE_ADMIN, same ROLE_ prefix rule as hasRole.
