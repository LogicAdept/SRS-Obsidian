<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Security expressions are SpEL used in URL rules and method security: hasRole, hasAuthority, hasAnyRole, permitAll, denyAll, isAnonymous, isAuthenticated, authentication, principal, and custom beans.

@PreAuthorize / @PostAuthorize / @PreFilter / @PostFilter are the annotation forms. @Secured cannot use SpEL. Dumps also mention a custom PermissionEvaluator for hasPermission(...).
> [!warning] Unverified traps from the dump
> - @Secured({ROLE_A, ROLE_B}) is OR. @PreAuthorize with and is AND.
> - Enable method security (prePostEnabled / @EnableMethodSecurity) or the annotations are no-ops.
