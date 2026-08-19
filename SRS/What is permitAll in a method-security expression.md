<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump SpEL vocabulary: permitAll() in @PreAuthorize always allows the call (same name as the HTTP rule). Used on a class-level default you then override on sensitive methods, or in tests.
> [!warning] Unverified traps from the dump
> - Class-level @PreAuthorize("permitAll()") plus a method @PreAuthorize("hasRole('ADMIN')") — the method annotation wins in dumps, but forgetting the method annotation leaves the class wide open.
