<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

ABAC decides on user, resource, and environment attributes, not only roles. Dumps implement PermissionEvaluator.hasPermission(...) and call it from SpEL: hasPermission(#id, 'Employee', 'READ') or a @bean method.

Register the evaluator on the method-security expression handler. @PreAuthorize then runs your attribute logic at the method boundary.
> [!warning] Unverified traps from the dump
> - A PermissionEvaluator that always returns true is not ABAC.
> - URL hasRole rules cannot see domain-object fields; dumps put ABAC on methods for that reason.
