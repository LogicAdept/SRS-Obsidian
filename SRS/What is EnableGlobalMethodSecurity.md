<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Old dump switch: @EnableGlobalMethodSecurity(prePostEnabled = true) (and securedEnabled / jsr250Enabled). It turns on @PreAuthorize / @Secured / @RolesAllowed via AOP.

Spring Security 6 dumps replace it with @EnableMethodSecurity. Mixing both, or keeping only the old annotation on Boot 3, is why @PreAuthorize ‘stops working’ after upgrade.
> [!warning] Unverified traps from the dump
> - prePostEnabled defaulted to false on the old annotation. Forgetting it leaves @PreAuthorize as a no-op even before Boot 3.
