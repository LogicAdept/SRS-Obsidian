<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: jsr250Enabled = true (on @EnableGlobalMethodSecurity or @EnableMethodSecurity) turns on JSR-250 @RolesAllowed.

XML: global-method-security jsr250-annotations="enabled". @RolesAllowed is role-only; it has no SpEL.
> [!warning] Unverified traps from the dump
> - prePostEnabled / @EnableMethodSecurity defaults do not enable @RolesAllowed. You must flip jsr250Enabled.
