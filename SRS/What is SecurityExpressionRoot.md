<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump comparison: @PreAuthorize can call methods and properties on SecurityExpressionRoot (hasRole, hasAuthority, isAuthenticated, principal, authentication, …). @Secured cannot.

That is why SpEL method security is more powerful than a role list.
> [!warning] Unverified traps from the dump
> - Custom methods on the root need a custom SecurityExpressionHandler. hasRole still applies the ROLE_ prefix convention.
