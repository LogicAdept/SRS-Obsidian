<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

AbstractSecurityInterceptor is the dump’s authorization core. It reads Authentication from SecurityContextHolder and asks AccessDecisionManager whether the call is allowed; otherwise AccessDeniedException.

Two concrete types in dumps: FilterSecurityInterceptor (HTTP URIs) and MethodSecurityInterceptor (method security). Later Spring Security replaced the filter interceptor with AuthorizationFilter / AuthorizationManager, but dumps still name AbstractSecurityInterceptor.
> [!warning] Unverified traps from the dump
> - This is authorization, not authentication. It assumes an Authentication is already present (or anonymous).
> - AccessDecisionManager is the old voter model; Security 6 prefers AuthorizationManager.
