<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump SS6 change: AuthorizationManager replaces the AccessDecisionManager + voter chain for both URLs and methods. Method interceptors ask one manager; a PermissionEvaluator is a bean the new stack auto-detects.
> [!warning] Unverified traps from the dump
> - Manual extra interceptor + auto-detect PermissionEvaluator is the dump double-invocation.
