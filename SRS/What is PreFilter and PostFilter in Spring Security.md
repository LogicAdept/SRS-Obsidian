<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

@PreFilter and @PostFilter are SpEL method-security annotations that filter collections (and maps), not just allow/deny the call.

@PreFilter removes arguments the user may not submit. @PostFilter removes elements from the return value the user may not see. They share EnableMethodSecurity / prePostEnabled with @PreAuthorize. @Secured cannot do this.
> [!warning] Unverified traps from the dump
> - PostFilter loads the full collection first, then drops rows — a dump performance trap versus query-level filtering.
> - The default filter object name is filterObject in SpEL.
