<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: four annotations take SpEL — @PreAuthorize, @PostAuthorize, @PreFilter, @PostFilter.

@Secured and @RolesAllowed do not. That is the trick question: you cannot write @Secured("hasRole('ADMIN')").
> [!warning] Unverified traps from the dump
> - @EnableMethodSecurity turns pre/post (SpEL) on by default; jsr250Enabled / securedEnabled are extra flags.
