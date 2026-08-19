<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: @PreAuthorize("hasRole('ADMIN')") is SpEL and adds ROLE_ (same as HTTP hasRole). @Secured("ROLE_ADMIN") is a literal authority string, no SpEL, no hasRole() function. @Secured({"A","B"}) is OR; AND needs @PreAuthorize.
> [!warning] Unverified traps from the dump
> - @Secured("hasRole('ADMIN')") looks up an authority named hasRole('ADMIN'), which never matches.
