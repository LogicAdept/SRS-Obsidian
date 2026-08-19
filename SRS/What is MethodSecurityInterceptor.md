<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: the AOP interceptor around a secured method. It evaluates the annotation / AuthorizationManager and either proceeds or throws AccessDeniedException.

Security 6 dumps also talk about AuthorizationManager-before/after method interceptors replacing the old GlobalMethodSecurityConfiguration stack. A missing interceptor bean is the upgrade smoking gun.
> [!warning] Unverified traps from the dump
> - Two interceptors on the same method (old + new enable annotations) is a dump double-invocation / conflict.
