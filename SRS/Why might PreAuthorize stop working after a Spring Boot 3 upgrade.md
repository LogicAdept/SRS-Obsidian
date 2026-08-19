<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: Boot 3 / Security 6 wants @EnableMethodSecurity. Keeping @EnableGlobalMethodSecurity compiles, but dumps say it does not wire the new AOP infrastructure, so role checks are silently skipped.

Fix: replace the annotation, grep out the old import, confirm the method-security interceptor bean exists.
> [!warning] Unverified traps from the dump
> - prePostEnabled false on leftover GlobalMethodSecurity is the other silent no-op, even without mixing.
