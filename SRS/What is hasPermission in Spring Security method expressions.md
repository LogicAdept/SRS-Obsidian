<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump ABAC path: SpEL hasPermission(target, 'WRITE') (and variants) delegates to a PermissionEvaluator bean. Register the evaluator; Security 6 dumps say the new method-security infrastructure auto-detects it — do not manually wire a second interceptor.
> [!warning] Unverified traps from the dump
> - Manual wiring of PermissionEvaluator plus auto-detect is the dump double-invocation case.
