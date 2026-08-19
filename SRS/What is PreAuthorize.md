<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: @PreAuthorize runs a SpEL check before the method. Typical: @PreAuthorize("hasRole('ADMIN')") or ownership with #userId == authentication.name.

It needs @EnableMethodSecurity (pre/post on). Denial is AccessDeniedException; the method never runs. @Secured / @RolesAllowed cannot use SpEL.
> [!warning] Unverified traps from the dump
> - Self-invocation and private methods skip the AOP proxy, so @PreAuthorize never fires.
