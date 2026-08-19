<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: put @EnableMethodSecurity on a @Configuration class. That is enough for @PreAuthorize / @PostAuthorize.

For @RolesAllowed and @Secured: @EnableMethodSecurity(jsr250Enabled = true, securedEnabled = true).
> [!warning] Unverified traps from the dump
> - @EnableWebSecurity does not turn on method security. URL rules and method annotations are separate switches.
