<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: @RolesAllowed is JSR-250 (Jakarta). Role-based only, same power class as @Secured, not Spring-specific. Enable with jsr250Enabled = true on @EnableMethodSecurity.

@PreAuthorize is more powerful (SpEL). @RolesAllowed is the Java-standard spelling interviewers contrast with Spring’s annotations.
> [!warning] Unverified traps from the dump
> - jsr250Enabled defaults to false. The annotation compiling on the method is not enough.
