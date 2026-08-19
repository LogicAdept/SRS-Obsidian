<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump upgrade smoking gun: @PreAuthorize compiles and sits on the method, but no interceptor bean means the annotation is decorative. Check the context for MethodSecurityInterceptor / the AuthorizationManager method interceptor after switching to @EnableMethodSecurity.
> [!warning] Unverified traps from the dump
> - Missing interceptor is silent — no startup error in the dump story, just open admin methods.
