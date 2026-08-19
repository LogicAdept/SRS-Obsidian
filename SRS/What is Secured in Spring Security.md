<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: @Secured is Spring’s role-only method annotation. No SpEL, no method-argument access. Enable with securedEnabled = true.

Multiple roles on @Secured are treated as OR. Prefer @PreAuthorize when you need AND, hasRole, or #param checks.
> [!warning] Unverified traps from the dump
> - You cannot write @Secured("hasRole('ADMIN')"). That string is not SpEL here; it is looked up as a literal authority.
