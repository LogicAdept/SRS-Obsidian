<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: do not mix. The old annotation creates a separate interceptor chain that conflicts with the new one. Some @PreAuthorize methods work, most do not, often with no error.

Pick @EnableMethodSecurity. Remove the old annotation and its import. Check that a MethodSecurityInterceptor (or the new AuthorizationManager method interceptor) is actually in the context.
> [!warning] Unverified traps from the dump
> - Silent ignore after a Boot 3 upgrade is the dump signature of this mix, not a SpEL typo.
