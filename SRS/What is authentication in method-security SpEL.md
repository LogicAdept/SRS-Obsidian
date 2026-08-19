<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump expressions: authentication is the current Authentication. authentication.name is the username; principal is authentication.principal (often UserDetails). Used in @PreAuthorize / @PostAuthorize / filters.
> [!warning] Unverified traps from the dump
> - AnonymousAuthenticationFilter still supplies an authentication object. Check isAuthenticated() / isAnonymous(), not null.
