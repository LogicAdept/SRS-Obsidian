<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump defense-in-depth: authorizeHttpRequests only guards HTTP. Service methods can be called from MVC, a scheduled job, or a listener. Method annotations protect the business method regardless of entry point.
> [!warning] Unverified traps from the dump
> - Method security is not a substitute for URL rules on the web layer. Dumps want both.
