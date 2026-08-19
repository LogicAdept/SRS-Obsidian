<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: securedEnabled = true turns on Spring’s @Secured (role names, no SpEL). It is false by default on both @EnableMethodSecurity and the old global annotation.
> [!warning] Unverified traps from the dump
> - @Secured({"ROLE_A", "ROLE_B"}) is OR in dumps. AND of two roles needs @PreAuthorize hasRole and hasRole.
