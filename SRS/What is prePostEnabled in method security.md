<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: prePostEnabled turns on @PreAuthorize, @PostAuthorize, @PreFilter, and @PostFilter.

On @EnableGlobalMethodSecurity it defaulted to false. On @EnableMethodSecurity it defaults to true.
> [!warning] Unverified traps from the dump
> - Copy-paste @EnableGlobalMethodSecurity() with no attributes is why @PreAuthorize is a no-op in older dumps.
