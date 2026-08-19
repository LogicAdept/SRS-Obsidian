<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: AccessDeniedException when the SpEL / role check fails. For @PreAuthorize the method body never runs. For @PostAuthorize the body already ran.

On the web stack, ExceptionTranslationFilter still translates that to HTTP 403 for an authenticated user (401 if the caller is anonymous).
> [!warning] Unverified traps from the dump
> - Catching Exception around a service call can swallow AccessDeniedException and hide the 403 (same dump family as swallowing JWT validation errors).
