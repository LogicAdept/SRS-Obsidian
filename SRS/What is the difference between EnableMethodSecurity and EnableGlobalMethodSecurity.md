<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: @EnableGlobalMethodSecurity is the old switch (prePostEnabled default false, GlobalMethodSecurityConfiguration). @EnableMethodSecurity is the Security 6 / Boot 3 replacement: pre/post on by default, bean-based AuthorizationManager interceptors instead of the old global config class.

Mixing both, or keeping only the old annotation on Boot 3, is why @PreAuthorize ‘stops working’ after upgrade.
> [!warning] Unverified traps from the dump
> - TheCodeForge-style dumps: the old annotation still compiles on Boot 3 but may not wire MethodSecurityInterceptor. Annotations become decorative.
