<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: yes. SpEL #paramName is the method argument. Example: @PreAuthorize("hasRole('ADMIN') or #userId == authentication.name"). @Secured and @RolesAllowed cannot see arguments.
> [!warning] Unverified traps from the dump
> - The SpEL name is the Java parameter name. Without -parameters / a name, #userId may not bind.
