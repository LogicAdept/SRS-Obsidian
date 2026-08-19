<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

ExceptionTranslationFilter sits above the authorization interceptor in dump filter lists. It does not enforce rules; it catches AuthenticationException and AccessDeniedException and turns them into HTTP behavior: commence the AuthenticationEntryPoint (login or 401) or the AccessDeniedHandler (403 / denied page).

Nearby dump names: SecurityContextPersistenceFilter (load/clear context), UsernamePasswordAuthenticationFilter (form login), FilterSecurityInterceptor (old URI enforcer).
> [!warning] Unverified traps from the dump
> - If this filter is missing or ordered wrong, AccessDeniedException becomes a 500 instead of 401/403.
> - FilterSecurityInterceptor is the legacy enforcer; Security 6 dumps may say AuthorizationFilter instead.
