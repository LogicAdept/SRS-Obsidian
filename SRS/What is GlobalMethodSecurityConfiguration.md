<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: old method-security stack. You extended GlobalMethodSecurityConfiguration with @EnableGlobalMethodSecurity. Security 6 dumps replace it with segmented AuthorizationManager beans and @EnableMethodSecurity — no base class.
> [!warning] Unverified traps from the dump
> - A custom GlobalMethodSecurityConfiguration plus @EnableMethodSecurity is the two-interceptor conflict dump.
