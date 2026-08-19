<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: @EnableMethodSecurity on a @Configuration class turns on method-level authorization in Spring Security 6. It replaces @EnableGlobalMethodSecurity. prePostEnabled defaults to true (@PreAuthorize / @PostAuthorize / @PreFilter / @PostFilter).

securedEnabled and jsr250Enabled still default false — set them if you need @Secured or @RolesAllowed.
> [!warning] Unverified traps from the dump
> - The old annotation defaulted prePostEnabled to false. Forgetting that left @PreAuthorize as a no-op even before Boot 3.
