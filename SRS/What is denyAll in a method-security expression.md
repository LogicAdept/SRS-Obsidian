<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump SpEL: denyAll() always refuses the call (AccessDeniedException), matching the HTTP denyAll() rule. Used to lock a type or to fail a test that should never be callable.
> [!warning] Unverified traps from the dump
> - HTTP denyAll() is AuthorizationFilter. Method denyAll() is the AOP interceptor. You can lock URLs and still call the service from a job unless the method is denied too.
